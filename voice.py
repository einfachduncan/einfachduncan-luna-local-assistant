def tts_speak(text: str) -> str:
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        return "TTS abgespielt."
    except Exception as e:
        return f"TTS-Fehler: {e}"
