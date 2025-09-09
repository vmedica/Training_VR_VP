using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;
using UnityEngine.XR.Interaction.Toolkit.Interactables;

public class GrabVisualFeedback : MonoBehaviour
{
    private XRGrabInteractable grabInteractable;
    private Renderer objectRenderer;
    public Color normalColor = Color.white;
    public Color hoverColor = Color.cyan;
    public Color grabColor = Color.green;

    void Awake()
    {
        grabInteractable = GetComponent<XRGrabInteractable>();
        objectRenderer = GetComponent<Renderer>();
        objectRenderer.material.color = normalColor;

        grabInteractable.hoverEntered.AddListener(OnHoverEnter);
        grabInteractable.hoverExited.AddListener(OnHoverExit);
        grabInteractable.selectEntered.AddListener(OnGrab);
        grabInteractable.selectExited.AddListener(OnRelease);
    }

    void OnHoverEnter(HoverEnterEventArgs args)
    {
        objectRenderer.material.color = hoverColor;
    }

    void OnHoverExit(HoverExitEventArgs args)
    {
        objectRenderer.material.color = normalColor;
    }

    void OnGrab(SelectEnterEventArgs args)
    {
        objectRenderer.material.color = grabColor;
    }

    void OnRelease(SelectExitEventArgs args)
    {
        objectRenderer.material.color = normalColor;
    }
}
