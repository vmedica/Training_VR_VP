import torch
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech
import soundfile as sf

processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")

speaker_embedding = torch.zeros((1, 512))  # voce neutra
text = "Ciao, sto testando la voce"

inputs = processor(text=text, return_tensors="pt")
with torch.no_grad():
    speech = model.generate_speech(inputs["input_ids"], speaker_embedding)

print("Shape output:", speech.shape)  # controlla dimensioni
speech_np = speech.squeeze().cpu().numpy()
print("Min/Max:", speech_np.min(), speech_np.max())

sf.write("test.wav", speech_np, 16000)
