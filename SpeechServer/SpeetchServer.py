# Crea un server Flask che offre due API:
# 1. /tts: Converte testo in voce
# 2. /stt: Converte la voce in testo

from flask import Flask, request, jsonify, send_file
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5ForSpeechToText
import torch
import io
import soundfile as sf

app = Flask(__name__)

# ===== TTS (Text → Audio) =====
tts_processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
tts_model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
speaker_embedding = torch.zeros((1, 512))

@app.route("/tts", methods=["POST"])
def text_to_speech():
    text = request.json["text"]
    
    # Generazione audio
    inputs = tts_processor(text=text, return_tensors="pt")
    with torch.no_grad():
        speech = tts_model.generate_speech(inputs["input_ids"], speaker_embedding)
    
    # ===== Normalizzazione audio =====
    speech_np = speech.squeeze().cpu().numpy()
    max_val = max(abs(speech_np.max()), abs(speech_np.min()))
    if max_val > 0:
        speech_np = speech_np / max_val  # valori tra -1 e 1
    
    # Salvataggio su buffer per send_file
    buffer = io.BytesIO()
    sf.write(buffer, speech_np, 16000, format="WAV")
    buffer.seek(0)
    
    # Salvataggio file test.wav per ascolto esterno
    with open("test.wav", "wb") as f:
        f.write(buffer.getbuffer())
    
    return send_file(buffer, mimetype="audio/wav")


# ===== STT (Audio → Testo) =====
stt_processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_asr")
stt_model = SpeechT5ForSpeechToText.from_pretrained("microsoft/speecht5_asr")

@app.route("/stt", methods=["POST"])
def speech_to_text():
    audio_file = request.files["audio"]
    waveform, sr = torchaudio.load(audio_file)
    inputs = stt_processor(waveform.squeeze(), sampling_rate=sr, return_tensors="pt")
    
    with torch.no_grad():
        predicted_ids = stt_model.generate(**inputs)
    
    transcription = stt_processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    return jsonify({"text": transcription})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
