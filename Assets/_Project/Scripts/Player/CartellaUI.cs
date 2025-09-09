using TMPro;
using UnityEngine;

public class CartellaUI : MonoBehaviour
{
    public static CartellaUI Instance;

    public GameObject pannello;
    public TMP_Text txtID, txtEtà, txtSesso, txtBMI, txtGlucosio, txtInsulina;

    private void Awake()
    {
        Instance = this;
        pannello.SetActive(false);  // nascosta all'inizio
    }

    public void Mostra(CartellaClinica c)
    {
        pannello.SetActive(true);

        txtID.text = $"ID: {c.SEQN}";
        txtEtà.text = $"Età: {c.RIDAGEYR}";
        txtSesso.text = $"Sesso: {(c.RIAGENDR == 1 ? "Maschio" : "Femmina")}";
        txtBMI.text = $"BMI: {c.BMXBMI:F1}";
        txtGlucosio.text = $"Glucosio: {c.LBXGLU:F1} mg/dL";
        txtInsulina.text = $"Insulina: {c.LBXIN:F1} mg/dL";
    }

    public void Nascondi()
    {
        pannello.SetActive(false);
    }
}

