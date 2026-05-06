# Luna V2

Luna ist eine lokale, private und anpassbare KI-Assistentin mit Python, Gradio und lokalem LLM-Backend.

## Unterstützte Backends
- Ollama
- LM Studio

## Features
- lokale Web-UI mit Gradio
- Streaming-Antworten
- lokale Chat-Historie / Memory via SQLite
- einfache Tool-Befehle
- Chat-Export als JSON
- optionale TTS-Vorbereitung
- anpassbare Persona-Datei
- keine Cloud notwendig

---

## Schnellstart

### 1. Python-Umgebung
```bash
python -m venv .venv
```

#### Windows
```bash
.venv\\Scripts\\activate
```

#### Linux/macOS
```bash
source .venv/bin/activate
```

### 2. Abhängigkeiten installieren
```bash
pip install -r requirements.txt
```

### 3. Konfiguration
```bash
cp .env.example .env
```

### 4. Ollama installieren
Siehe: https://ollama.com/

Beispielmodell:
```bash
ollama pull llama3.1:8b
```

### 5. Starten
```bash
python app.py
```

Browser:
- http://127.0.0.1:7860

---

## LM Studio verwenden

1. LM Studio installieren
2. Modell laden
3. Local Server starten
4. `.env` anpassen:

```env
LLM_BACKEND=lmstudio
LMSTUDIO_BASE_URL=http://127.0.0.1:1234/v1
LMSTUDIO_MODEL=local-model
```

---

## Tool-Befehle

### Websuche
```text
/search lokale llm modelle für coding
```

### Dateien anzeigen
```text
/files
```

### Datei lesen
```text
/read notes/ideas.txt
```

### Datei schreiben
```text
/write notes/ideas.txt
Projekt Luna ausbauen
Voice-Features später aktivieren
```

---

## Modelle einbinden

### Ollama
Beispiele:
```bash
ollama pull llama3.1:8b
ollama pull llama3.1:70b
ollama pull command-r
ollama pull mistral
ollama pull dolphin-mistral
```

Dann in `.env`:
```env
OLLAMA_MODEL=command-r
```

### LM Studio
- GGUF-Modell herunterladen
- in LM Studio laden
- Server aktivieren
- Modellname in `.env` setzen

---

## Nächste Ausbaustufen
- semantisches Memory mit ChromaDB
- Dokumenten-Upload
- RAG
- lokaler Agent-Loop
- Modellumschalter in der UI
- Rollenprofile
- bessere Voice-Funktionen
- OpenWebUI-Anbindung
- SillyTavern-kompatible API-Schicht
