using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using System.Text;

public class SpeechT5Manager : MonoBehaviour
{
    [SerializeField] private string ttsUrl = "http://127.0.0.1:5005/tts";

    // Usa questo per riprodurre la voce
    public IEnumerator Speak(string text, AudioSource audioSource)
    {
        string jsonData = JsonUtility.ToJson(new TextData(text));

        using (UnityWebRequest www = new UnityWebRequest(ttsUrl, "POST"))
        {
            byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonData);
            www.uploadHandler = new UploadHandlerRaw(bodyRaw);
            www.downloadHandler = new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type", "application/json");

            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError("Errore SpeechT5: " + www.error);
            }
            else
            {
                // Converti WAV → AudioClip
                AudioClip clip = WavUtility.ToAudioClip(www.downloadHandler.data, "ttsClip");
                audioSource.clip = clip;
                audioSource.Play();
            }
        }
    }

    [System.Serializable]
    public class TextData
    {
        public string text;
        public TextData(string t) { text = t; }
    }
}
