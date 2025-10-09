# test_tts_request.py
import requests

URL = "http://127.0.0.1:5005/tts"
data = {"text": "Ciao, questo è un test del sintetizzatore vocale SpeechT5. CIAO VINCENZO"}

print("Invio testo al server...")
resp = requests.post(URL, json=data, timeout=60)

if resp.status_code == 200 and resp.headers.get("content-type", "").startswith("audio"):
    filename = "test_output.wav"
    with open(filename, "wb") as f:
        f.write(resp.content)
    print(f"File '{filename}' salvato. Riproducilo con un player (VLC o Windows Media Player).")
else:
    print(f"Errore: {resp.status_code}")
    print(resp.text)
