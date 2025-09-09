using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;
using UnityEngine.XR.Interaction.Toolkit.Interactors;

public class SimpleLever : MonoBehaviour
{
    public Transform pivotBraccio;
    public XRBaseInteractor interactor;

    public float maxDownAngle = 70f; // max rotazione verso il basso
    public float maxUpAngle = 0f;    // max rotazione verso l'alto (posizione neutra)

    private Quaternion initialRotation;

    void Start()
    {
        initialRotation = pivotBraccio.localRotation;
    }

    void Update()
    {
        if (interactor != null)
        {
            Vector3 direction = interactor.transform.position - pivotBraccio.position;
            // Angolo tra l'up vector (verso l'alto) e la direzione mano-pivot rispetto asse Z
            float angle = Vector3.SignedAngle(Vector3.up, direction, Vector3.forward);
            angle = Mathf.Clamp(angle, -maxDownAngle, maxUpAngle);

            pivotBraccio.localRotation = Quaternion.Euler(0, 0, angle);
        }
        else
        {
            pivotBraccio.localRotation = initialRotation;
        }
    }

    public void OnGrab(XRBaseInteractor grabInteractor)
    {
        interactor = grabInteractor;
    }

    public void OnRelease(XRBaseInteractor grabInteractor)
    {
        if (interactor == grabInteractor)
            interactor = null;
    }
}