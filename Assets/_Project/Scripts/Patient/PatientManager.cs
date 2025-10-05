using System;

public class PatientManager : MonoBehaviour{
    [SerializeField] private string datasetPath = "C:\Training_VR_VP\Assets\_Project\Resources\Dataset\Clean_filteredDataset.csv"
    [SerializeField] private string lmStudioUrl = "http://127.0.0.1:1234"

    async void Start(){
        Debug.Log("Creazione del paziente virtuale...");
        string patientPrompt = GetRandomPatientPrompt();

        string systemPrompt = "Sei un paziente virtuale. Rispondi come se fossi una persona reale con questi dati sanitari:\n";
        string fullPrompt = systemPrompt + patientPrompt + "\nSei pronto a rispondere alle domande del medico.";

        string response = await SendPromptToLM(fullPrompt);
        Debug.Log("LLM: " + response);
    }
    CONTINUA DA QUI...
}   