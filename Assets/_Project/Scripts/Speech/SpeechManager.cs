using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using System.Text;

public class SpeechManager : MonoBehaviour
{
    private string serverUrl = "http://localhost:5005";

    public IEnumerator TextToSpeech(string text, AudioSource audioSource)
    {
        string jsonData = JsonUtility.ToJson(new TextData(text));
        using (UnityWebRequest www = UnityWebRequest.PostWwwForm($"{serverUrl}/tts", "POST"))
        {
            byte[] bodyRaw = Encoding.UTF8.GetBytes(jsonData);
            www.uploadHandler = new UploadHandlerRaw(bodyRaw);
            www.downloadHandler = new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type", "application/json");

            yield return www.SendWebRequest();

            if (www.result == UnityWebRequest.Result.Success)
            {
                AudioClip clip = WavUtility.ToAudioClip(www.downloadHandler.data, "speech");
                audioSource.clip = clip;
                audioSource.Play();
            }
            else
            {
                Debug.LogError($"Errore TTS: {www.error}");
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
