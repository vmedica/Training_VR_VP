from TTS.utils.audio import AudioProcessor
from TTS.utils.speakers import Speakers

speakers = Speakers.load("C:/Users/vince/AppData/Local/tts/tts_models--multilingual--multi-dataset--xtts_v2/speakers_xtts.pth")
print(speakers.speaker_ids)
