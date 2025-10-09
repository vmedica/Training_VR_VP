# SpeechtServer.py
# Server Flask che espone /tts per generare audio WAV da testo usando SpeechT5 + HiFi-GAN.
# 1. /tts: Converte testo in voce

from flask import Flask, request, jsonify, send_file
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
import torch
import soundfile as sf
import io
import os
import numpy as np
import traceback
import librosa  # per resampling ad alta qualità

app = Flask(__name__)

# Scegli device (usa GPU se disponibile)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Caricamento modelli (processor, TTS e vocoder HiFi-GAN)
print("Caricamento SpeechT5 processor, modello TTS e vocoder HiFi-GAN (potrebbe richiedere tempo)...")
tts_processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
tts_model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts").to(device)
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan").to(device)

# Speaker embedding neutro (puoi sostituirlo con embedding realistici in futuro)
speaker_embedding = torch.zeros((1, 512), device=device)
print("Modelli caricati.")

@app.route("/tts", methods=["POST"])
def text_to_speech():
    """
    Endpoint /tts
    Request JSON: {"text": "il testo da sintetizzare"}
    Response: audio/wav (file WAV PCM16, samplerate 44100)
    """
    try:
        data = request.get_json(force=True)
        text = (data.get("text") or "").strip()
        if not text:
            return jsonify({"error": "Testo mancante"}), 400

        print(f"[TTS] testo ricevuto (len={len(text)}): {text[:80]!r}")

        # Prepara input (tokenizzazione / processor)
        inputs = tts_processor(text=text, return_tensors="pt")
        input_ids = inputs["input_ids"].to(device)

        # Genera parlato usando vocoder (ottieni direttamente waveform)
        with torch.no_grad():
            speech = tts_model.generate_speech(
                input_ids, speaker_embeddings=speaker_embedding, vocoder=vocoder
            )

        if speech is None:
            return jsonify({"error": "Modello non ha generato audio (speech is None)"}), 500

        # Converti in numpy e normalizza [-1,1]
        audio = speech.squeeze().cpu().numpy()
        print(f"[TTS] waveform shape: {audio.shape}, dtype: {audio.dtype}, max:{np.max(audio):.6f}")

        max_val = float(np.max(np.abs(audio))) if audio.size else 0.0
        if max_val > 0:
            audio = audio / max_val

        # Resample da 16kHz a 44100 Hz per miglior qualità
        audio_44k = librosa.resample(audio, orig_sr=16000, target_sr=44100)

        # Converti in PCM16 (int16)
        audio_int16 = (audio_44k * 32767).astype(np.int16)

        # Scrivi su buffer in memoria
        buffer = io.BytesIO()
        sf.write(buffer, audio_int16, 44100, format="WAV", subtype="PCM_16")
        buffer.seek(0)

        # Restituisci il WAV come risposta binaria
        return send_file(
            buffer,
            mimetype="audio/wav",
            as_attachment=True,
            download_name="tts_output.wav"
        )

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
