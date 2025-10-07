using System;
using System.IO;
using UnityEngine;

public static class WavUtility
{
    // Converte i byte WAV in un AudioClip Unity
    public static AudioClip ToAudioClip(byte[] wavFile, string clipName = "GeneratedClip")
    {
        using (MemoryStream stream = new MemoryStream(wavFile))
        using (BinaryReader reader = new BinaryReader(stream))
        {
            // Skip header "RIFF"
            reader.ReadBytes(4);
            reader.ReadInt32();
            reader.ReadBytes(4); // "WAVE"
            reader.ReadBytes(4); // "fmt "
            int subChunk1 = reader.ReadInt32();
            reader.ReadInt16(); // audioFormat
            int channels = reader.ReadInt16();
            int sampleRate = reader.ReadInt32();
            reader.ReadInt32(); // byteRate
            reader.ReadInt16(); // blockAlign
            int bitsPerSample = reader.ReadInt16();

            reader.ReadBytes(subChunk1 - 16); // skip extra params
            reader.ReadBytes(4); // "data"
            int dataSize = reader.ReadInt32();

            byte[] data = reader.ReadBytes(dataSize);

            int bytesPerSample = bitsPerSample / 8;
            int sampleCount = dataSize / bytesPerSample;

            float[] samples = new float[sampleCount];

            // Converte i byte PCM in float normalizzati
            for (int i = 0; i < sampleCount; i++)
            {
                short sample = BitConverter.ToInt16(data, i * bytesPerSample);
                samples[i] = sample / 32768f;
            }

            AudioClip clip = AudioClip.Create(clipName, sampleCount / channels, channels, sampleRate, false);
            clip.SetData(samples, 0);

            return clip;
        }
    }
}
