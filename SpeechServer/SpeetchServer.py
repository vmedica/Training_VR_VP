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

tts_processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
tts_model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts")
speaker_embedding = torch.zeros((1, 512)) #voce neuta predefinita

##