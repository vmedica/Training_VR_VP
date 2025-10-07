#Crea un server Flask che offre due API:
# 1. /tts: Converte testo in voce
# 2. /sst: COnverte la voce in testo

from flask import Flask, request, jsonify, send_file
'''
Importa Flask e alcune funzioni utili:
Flask: per creare l’app web
request: per accedere ai dati delle richieste HTTP
jsonify: per restituire risposte in formato JSON
send_file: per inviare file binari (es. audio WAV)
'''

from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5ForSpeechToText
import torchaudio
import soundfile as sf
import torch
import io
'''
Importa le librerie:
SpeechT5Processor: serve a preparare testo o audio per i modelli SpeechT5.
SpeechT5ForTextToSpeech: modello per generare voce da testo.
SpeechT5ForSpeechToText: modello per trascrivere voce in testo.
torchaudio: per leggere file audio.
soundfile: per scrivere audio in vari formati (es. WAV).
torch: libreria PyTorch (necessaria per i modelli).
io: per gestire file in memoria (senza salvarli su disco).
'''

app = Flask(__name__)   #Crea un’app Flask, che diventa il server web.



# ===== TTS (Text → Audio) =====

tts_processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")  #converte il testo in un formato leggibile dal modello.
tts_model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")  #il modello vero e proprio che genera l’audio.
speaker_embedding = torch.zeros((1, 512)) #voce neuta predefinita. speaker_embedding: un vettore che definisce la voce del parlante.

@app.route("/tts", methods=["POST"])    #Definisce un endpoint Flask chiamato /tts a cui si può inviare una richiesta POST.
def text_to_speech():
    text = request.json["text"] #Legge il testo che arriva in formato JSON.
    
    inputs = tts_processors(text = text, return_tensors="pt") #Converte il testo in tensori PyTorch pronti per il modello.
    #"pt" sta per PyTorch tensors.
    #Il processore restituisce tensori, cioè strutture di dati ottimizzate per essere elaborate dal modello PyTorch.

    speech = tts_model.generate_speeech(inputs["input_ids"], speaker_embedding) #Genera il segnale audio corrispondente al testo.

    buffer = io.BytesIO()       #crea un buffer temporaneo in RAM.
    sf.write(buffer, speech.numpy(), 16000, format="WAV")   #scrive l’audio nel buffer come WAV con frequenza 16 kHz.
    buffer.seek(0)  #riporta il puntatore all’inizio del file per poterlo leggere.

    return send_file(buffer, mimetype="audio/wav")      #Restituisce il file audio WAV come risposta HTTP.



# ===== STT (Audio → Testo) =====
stt_model = SpeechT5ForSpeechToText.from_pretrained("microsoft/speecht5_asr")   #Carica il modello Automatic Speech Recognition (ASR) per la trascrizione.

@app.route("/stt", methods=["POST"])    #Definisce l’endpoint /stt per convertire audio -> testo.
def speech_to_text():
    audio_file = request.files["audio"]
    waveform, sr = torchaudio.load(audio_file)
    # Carica il file audio e ne ottiene:
    # waveform: i dati del suono come tensore.
    # sr: la frequenza di campionamento.

    #Prepara l’audio per il modello, convertendolo in tensori PyTorch.
    inputs = tts_processor(waveform.squeeze(), sampling_rate=sr, return_tensors="pt")

    #Usa il modello per predire la trascrizione (senza calcolare gradienti, quindi più veloce).
    with torch.no_grad():
        predicted_ids = stt_model.generate(**inputs)
    transcription = tts_processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]  #Converte gli ID predetti in testo leggibile.
    return jsonify({"text": transcription})    #Restituisce la trascrizione come JSON.
    
if __name__ == "__main__":  #Fa partire il server Flask sulla porta 5005, accessibile anche da altre macchine nella rete locale (0.0.0.0).
    app.run(host="0.0.0.0", port=5005)







