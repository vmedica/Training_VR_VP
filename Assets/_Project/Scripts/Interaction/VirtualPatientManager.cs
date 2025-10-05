using System;
using System.IO;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using UnityEngine;

public class VirtualPatientManager : MonoBehaviour
{
    [Header("Percorso Dataset CSV")]
    [SerializeField] private string datasetPath = "Assets/_Project/Resources/Dataset/Clean_filteredDataset.csv";

    [Header("LM Studio API")]
    [SerializeField] private string lmStudioUrl = "http://127.0.0.1:1234/v1/chat/completions";
    [SerializeField] private string modelName = "meta-llama-3-8b-instruct";

    public async void CreaPazienteVirtuale()
    {
        Debug.Log(" Creazione paziente virtuale in corso...");

        try
        {
            // 1️⃣ Estrai tupla casuale dal CSV
            string patientData = EstraiTuplaCasuale();

            // 2️⃣ Crea prompt completo
            string fullPrompt = CreaPromptCompleto(patientData);

            // 3️⃣ Invia al modello
            string risposta = await InviaPromptALM(fullPrompt);

            Debug.Log($" LLM Studio: {risposta}");
        }
        catch (Exception ex)
        {
            Debug.LogError(" Errore durante la creazione del paziente virtuale: " + ex.Message);
        }
    }

    private string EstraiTuplaCasuale()
    {
        if (!File.Exists(datasetPath))
            throw new FileNotFoundException($"File non trovato: {datasetPath}");

        var lines = File.ReadAllLines(datasetPath);
        if (lines.Length < 2)
            throw new Exception("Dataset vuoto o invalido.");

        var random = new System.Random();
        string[] headers = lines[0].Split(',');
        string[] values = lines[random.Next(1, lines.Length)].Split(',');

        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < headers.Length; i++)
            sb.AppendLine($"{headers[i]}: {values[i]}");

        return sb.ToString();
    }

    private string CreaPromptCompleto(string patientData)
    {
        StringBuilder sb = new StringBuilder();

        sb.AppendLine("SYSTEM PROMPT:");
        sb.AppendLine("Sei un paziente virtuale all’interno di una simulazione medica.");
        sb.AppendLine("Il tuo compito è simulare un paziente realistico basato sui seguenti dati clinici.");
        sb.AppendLine("Rispondi come una persona reale, con coerenza e umanità.");
        sb.AppendLine();

        sb.AppendLine(" DATI CLINICI:");
        sb.AppendLine(patientData);
        sb.AppendLine();

        sb.AppendLine("ROLE-PLAY:");
        sb.AppendLine("Comportati come un paziente vero. Rispondi in prima persona come se fossi il paziente.");
        sb.AppendLine();

        sb.AppendLine("ILLNESS SCRIPT:");
        sb.AppendLine("- Interpreta i dati per rappresentare la tua condizione medica.");
        sb.AppendLine("- Descrivi sintomi, storia e percezione personale.");
        sb.AppendLine();

        sb.AppendLine("Alla fine di questo messaggio, rispondi con: \"Sono pronto a rispondere alle domande del medico.\"");

        return sb.ToString();
    }

    private async Task<string> InviaPromptALM(string prompt)
    {
        using (HttpClient client = new HttpClient())
        {
            var json = $@"
{{
    ""model"": ""{modelName}"",
    ""messages"": [
        {{""role"": ""system"", ""content"": ""{prompt.Replace("\"", "\\\"")}""}}
    ]
}}";

            var content = new StringContent(json, Encoding.UTF8, "application/json");
            var response = await client.PostAsync(lmStudioUrl, content);

            string result = await response.Content.ReadAsStringAsync();
            return result;
        }
    }
}
