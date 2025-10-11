using System;
using System.IO;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using UnityEngine;

public class TTSClient : MonoBehaviour
{
    [SerializeField] private string ttsUrl = "http://127.0.0.1:5003/tts";
    [SerializeField] private AudioSource audioSource;

    private static readonly HttpClient client = new HttpClient();

    public async Task RiproduciVoce(string testo)
    {
        if (string.IsNullOrWhiteSpace(testo))
        {
            Debug.LogWarning("Testo vuoto, impossibile generare TTS.");
            return;
        }

        try
        {
            var json = "{\"text\":\"" + testo + "\",\"speaker\":\"Eugenio Mataracı\"}";
            var content = new StringContent(json, Encoding.UTF8, "application/json");

            var response = await client.PostAsync(ttsUrl, content);

            if (!response.IsSuccessStatusCode)
            {
                Debug.LogError($"Errore TTS server: {response.StatusCode}");
                return;
            }

            var audioData = await response.Content.ReadAsByteArrayAsync();
            PlayAudioFromBytes(audioData);
        }
        catch (Exception ex)
        {
            Debug.LogError("Errore durante la richiesta a XTTS: " + ex.Message);
        }
    }

    private void PlayAudioFromBytes(byte[] wavData)
    {
        WAV wav = new WAV(wavData);
        AudioClip audioClip = AudioClip.Create("TTS_Audio", wav.SampleCount, 1, wav.Frequency, false);
        audioClip.SetData(wav.LeftChannel, 0);
        audioSource.clip = audioClip;
        audioSource.Play();
    }

    // Helper WAV reader
    public class WAV
    {
        public float[] LeftChannel;
        public int ChannelCount;
        public int SampleCount;
        public int Frequency;

        public WAV(byte[] wav)
        {
            ChannelCount = BitConverter.ToInt16(wav, 22);
            Frequency = BitConverter.ToInt32(wav, 24);
            int pos = 12;
            while (!(wav[pos] == 100 && wav[pos + 1] == 97 && wav[pos + 2] == 116 && wav[pos + 3] == 97)) pos += 4;
            pos += 8;
            SampleCount = (wav.Length - pos) / 2 / ChannelCount;
            LeftChannel = new float[SampleCount];
            int i = 0;
            while (pos < wav.Length)
            {
                LeftChannel[i] = BytesToFloat(wav[pos], wav[pos + 1]);
                pos += 2 * ChannelCount;
                i++;
            }
        }

        private static float BytesToFloat(byte first, byte second)
        {
            short s = (short)((second << 8) | first);
            return s / 32768.0f;
        }
    }
}
