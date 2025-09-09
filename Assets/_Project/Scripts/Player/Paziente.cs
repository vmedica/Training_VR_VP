using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

public class Paziente : MonoBehaviour
{
    private CartellaClinica cartella;

    public void Inizializza(CartellaClinica dati)
    {
        cartella = dati;
    }

    public void OnSelectEnter()
    {
        CartellaUI.Instance.Mostra(cartella);
    }
}

