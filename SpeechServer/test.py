# test_tts_request.py
import requests

URL = "http://127.0.0.1:5005/tts"
data = {"text": "Ciao! Mi chiamo Tom e oggi voglio raccontarti una breve storia. Oggi sono arrivato a Londra e la città è davvero affascinante. Le strade sono piene di persone e ci sono molti monumenti famosi. Ho visitato il Big Ben e ho scattato molte foto. Domani pianifico di fare un giro lungo il Tamigi e vedere il Tower Bridge."}
#data = {"text": " Hi My name is Tom, and today I want to tell you a short story. I just arrived in London, and the city is really fascinating. The streets are full of people, and there are many famous landmarks. I visited Big Ben and took a lot of pictures. Tomorrow, I plan to take a walk along the Thames and see the Tower Bridge."}
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
