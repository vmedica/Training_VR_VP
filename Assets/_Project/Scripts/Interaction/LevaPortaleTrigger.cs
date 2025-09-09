using UnityEngine;

public class LevaPortaleTrigger : MonoBehaviour
{
    [Header("Prefab e punto di spawn")]
    [SerializeField] private GameObject portalPrefab;
    [SerializeField] private Transform spawnPoint;

    [Header("Script spawn paziente")]
    [SerializeField] private SpawnPaziente spawnPazienteScript;

    [Header("Impostazioni leva")]
    [SerializeField] private float sogliaAccensione = 60f;
    [SerializeField] private float sogliaSpegnimento = 80f;
    [SerializeField] private Axis asseRotazione = Axis.X;

    private enum Axis { X, Y, Z }

    private bool portaleAttivo = false;
    private bool prontoPerRiattivare = true;
    private GameObject portaleCorrente;

    private void Update()
    {
        float angolo = GetAngolo();

        // Leva abbassata: nuovo portale e nuovo paziente
        if (!portaleAttivo && prontoPerRiattivare && angolo <= sogliaAccensione)
        {
            Debug.Log("[LevaPortaleTrigger] Leva abbassata - creo nuovo portale");

            // Distruggi vecchio portale
            if (portaleCorrente != null)
            {
                Destroy(portaleCorrente);
                Debug.Log("[LevaPortaleTrigger] Portale precedente distrutto");
            }

            // Istanzia nuovo portale
            Vector3 posizioneSpawn = spawnPoint != null ? spawnPoint.position : transform.position + transform.forward * 2f;
            portaleCorrente = Instantiate(portalPrefab, posizioneSpawn, Quaternion.identity);

            // Attiva animazione portale
            PortalRound_Controller controller = portaleCorrente.GetComponent<PortalRound_Controller>();
            if (controller != null)
            {
                controller.F_TogglePortalRound(true);
            }

            // Spawna paziente
            if (spawnPazienteScript != null)
            {
                spawnPazienteScript.AttivaPortale();
            }

            // Stato aggiornato
            portaleAttivo = true;
            prontoPerRiattivare = false;
        }

        // Leva risollevata: preparati a nuovo giro
        else if (portaleAttivo && angolo >= sogliaSpegnimento)
        {
            Debug.Log("[LevaPortaleTrigger] Leva risollevata - disattivo portale");

            // Spegni il portale se possibile
            if (portaleCorrente != null)
            {
                PortalRound_Controller controller = portaleCorrente.GetComponent<PortalRound_Controller>();
                if (controller != null)
                {
                    controller.F_TogglePortalRound(false);
                }

                // Spegni anche le luci (opzionale)
                Light[] luci = portaleCorrente.GetComponentsInChildren<Light>();
                foreach (Light luce in luci)
                {
                    luce.enabled = false;
                }
            }

            portaleAttivo = false;
            prontoPerRiattivare = true;
        }
    }

    private float GetAngolo()
    {
        Vector3 rot = transform.localEulerAngles;
        float rawAngle = asseRotazione switch
        {
            Axis.X => rot.x,
            Axis.Y => rot.y,
            Axis.Z => rot.z,
            _ => 0f
        };

        return rawAngle > 180f ? 360f - rawAngle : rawAngle;
    }
}
