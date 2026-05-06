import os
import gradio as gr

from config import (
    APP_NAME,
    HOST,
    PORT,
    ENABLE_MEMORY,
    ENABLE_WEB_SEARCH,
    ENABLE_FILE_TOOLS,
    ENABLE_VOICE,
    MAX_CONTEXT_MESSAGES,
    MAX_CONTEXT_MEMORIES,
    CUSTOM_CSS,
)
from llm_client import stream_chat_completion
from system_prompt import build_system_prompt
from memory import MemoryStore
from tools import web_search, list_files, read_file, write_file
from utils import export_chat
from voice import tts_speak

memory = MemoryStore() if ENABLE_MEMORY else None


def get_css():
    if os.path.exists(CUSTOM_CSS):
        with open(CUSTOM_CSS, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def build_memory_block(user_message: str) -> str:
    if not memory:
        return ""

    items = []
    seen = set()

    for m in memory.recent(MAX_CONTEXT_MEMORIES):
        if m["id"] not in seen:
            seen.add(m["id"])
            items.append(m)

    for m in memory.search(user_message, MAX_CONTEXT_MEMORIES):
        if m["id"] not in seen:
            seen.add(m["id"])
            items.append(m)

    if not items:
        return ""

    lines = []
    for item in items[:MAX_CONTEXT_MEMORIES]:
        lines.append(f"- ({item['kind']}) {item['content'][:300]}")

    return "Relevante Erinnerungen:\n" + "\n".join(lines)


def parse_tool_command(message: str):
    text = message.strip()

    if ENABLE_WEB_SEARCH and text.startswith("/search "):
        query = text[len("/search "):].strip()
        return ("search", query)

    if ENABLE_FILE_TOOLS and text == "/files":
        return ("files", None)

    if ENABLE_FILE_TOOLS and text.startswith("/read "):
        path = text[len("/read "):].strip()
        return ("read", path)

    if ENABLE_FILE_TOOLS and text.startswith("/write "):
        parts = text.split("\n", 1)
        path = parts[0][len("/write "):].strip()
        content = parts[1] if len(parts) > 1 else ""
        return ("write", (path, content))

    return None


def run_tool(command):
    kind, payload = command

    if kind == "search":
        return web_search(payload)
    if kind == "files":
        return list_files()
    if kind == "read":
        return read_file(payload)
    if kind == "write":
        path, content = payload
        return write_file(path, content)

    return "Unbekanntes Tool."


def respond(user_message, history, extra_persona, auto_tts):
    history = history or []

    tool_cmd = parse_tool_command(user_message)
    if tool_cmd:
        tool_result = run_tool(tool_cmd)
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": f"[Tool]\n\n{tool_result}"})

        if memory:
            memory.add("tool", f"{user_message} -> {tool_result[:500]}", "tool interaction")

        yield history, history, "Tool ausgeführt."
        return

    system_prompt = build_system_prompt(extra_persona)
    memory_block = build_memory_block(user_message)

    messages = [{"role": "system", "content": system_prompt}]
    if memory_block:
        messages.append({"role": "system", "content": memory_block})

    for msg in history[-MAX_CONTEXT_MESSAGES:]:
        messages.append(msg)

    messages.append({"role": "user", "content": user_message})

    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": ""})

    partial = ""
    try:
        for chunk in stream_chat_completion(messages):
            partial = chunk
            history[-1]["content"] = partial
            yield history, history, "Antwort wird generiert..."
    except Exception as e:
        history[-1]["content"] = f"Fehler beim Modellaufruf: {e}"
        yield history, history, "Fehler."
        return

    if memory:
        memory.add("chat", f"User: {user_message}\nAssistant: {partial[:1000]}", "chat turn")

    status = "Fertig."
    if ENABLE_VOICE and auto_tts:
        status = tts_speak(partial)

    yield history, history, status


def clear_chat():
    return [], [], "Chat geleert."


def export_current_chat(history):
    if not history:
        return None, "Nichts zu exportieren."
    path = export_chat(history)
    return path, f"Exportiert: {path}"


with gr.Blocks(title=APP_NAME, css=get_css()) as demo:
    gr.Markdown(f"# {APP_NAME} V2\nLokale, private KI-Assistentin")

    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(type="messages", height=620)
            message = gr.Textbox(
                label="Nachricht",
                placeholder="Schreibe etwas oder nutze /search, /files, /read, /write",
                lines=4
            )

            with gr.Row():
                send_btn = gr.Button("Senden", variant="primary")
                clear_btn = gr.Button("Leeren")
                export_btn = gr.Button("Chat exportieren")

            status = gr.Textbox(label="Status", interactive=False)

        with gr.Column(scale=2):
            extra_persona = gr.Textbox(
                label="Zusätzliche Persona",
                placeholder="z.B. antworte technischer, kürzer, humorvoller ...",
                lines=10
            )

            auto_tts = gr.Checkbox(label="Antworten vorlesen (TTS)", value=False)

            gr.Markdown(
                """
### Befehle
- `/search <frage>` → Websuche
- `/files` → Dateien auflisten
- `/read <pfad>` → Datei lesen
- `/write <pfad>` + neue Zeile + Inhalt → Datei speichern

### Hinweise
- Läuft lokal mit Ollama oder LM Studio
- Chat-Memory wird lokal gespeichert
- Export als JSON möglich
                """
            )

            export_file = gr.File(label="Letzter Export")

    state = gr.State([])

    send_btn.click(
        respond,
        inputs=[message, state, extra_persona, auto_tts],
        outputs=[chatbot, state, status],
    )
    message.submit(
        respond,
        inputs=[message, state, extra_persona, auto_tts],
        outputs=[chatbot, state, status],
    )

    clear_btn.click(clear_chat, outputs=[chatbot, state, status])
    export_btn.click(export_current_chat, inputs=[state], outputs=[export_file, status])

if __name__ == "__main__":
    os.makedirs("data/files", exist_ok=True)
    os.makedirs("data/chat_exports", exist_ok=True)
    demo.launch(server_name=HOST, server_port=PORT, share=False)
