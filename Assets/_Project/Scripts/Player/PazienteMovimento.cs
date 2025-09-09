using UnityEngine;
using UnityEngine.AI;

public class PazienteMovimento : MonoBehaviour
{
    public Transform destinazione;
    private NavMeshAgent agente;
    private Animator animator;
    private float sogliaArrivo = 0.1f;
    private bool destinazioneImpostata = false;

    void Start()
    {
        agente = GetComponent<NavMeshAgent>();
        animator = GetComponent<Animator>();
    }

    void Update()
    {
        if (destinazione != null && !destinazioneImpostata)
        {
            agente.SetDestination(destinazione.position);
            destinazioneImpostata = true;
        }

        if (!agente.pathPending && agente.remainingDistance <= sogliaArrivo)
        {
            animator.SetBool("isWalking", false);
            agente.isStopped = true;
        }
        else if (agente.velocity.magnitude > 0.1f)
        {
            animator.SetBool("isWalking", true);
        }
        else
        {
            animator.SetBool("isWalking", false);
        }
    }
}
