import pysmile
import pysmile_license
from pathlib import Path
import random

NUM_ISTANTI = 5

def run_autopilot():
    # Caricamento rete
    percorso_file = Path(__file__).parent / "network2_rev3.xdsl" 
    net = pysmile.Network()
    net.read_file(str(percorso_file))
    
    net.clear_all_evidence()

    # net.set_evidence("Posizione_Iniziale", random.choices(net.get_outcome_ids("Posizione_Iniziale"),net.get_node_definition("Posizione_Iniziale"), k=1)[0])
    # print(f"Posizione Iniziale campionata: {net.get_evidence_id('Posizione_Iniziale')}")
    net.update_beliefs()
    

    for t in range(0, NUM_ISTANTI):
        print(f"\n--- ISTANTE {t} ---")
        # autochoose_outcome(net, "Meteo", t)
        # autochoose_outcome(net, "Terreno", t)
        # autochoose_outcome(net, "Stato_Sensore", t)
        # autochoose_outcome(net, "Accuratezza_Sensore", t)
        autochoose_outcome(net, "Rilevamento_Sensore", t)
        ask_user_decision(net, "Comando_Sterzo", t)

        # autochoose_outcome(net, "Sterzo", t)
        # autochoose_outcome(net, "Posizione_Veicolo", t)

    



def update_and_show_temporal_results(net):
    net.update_beliefs()
    slice_count = net.get_slice_count()
    for h in net.get_all_nodes():
        if net.get_node_temporal_type(h) == pysmile.NodeTemporalType.PLATE:
            outcome_count = net.get_outcome_count(h)
            v = net.get_node_value(h)
            print(f"Temporal beliefs for {net.get_node_id(h)}:")
            for slice_idx in range(0, slice_count):
                print(f"\tt={slice_idx}:", end="")
                for i in range(0, outcome_count):
                    print(f" {v[slice_idx * outcome_count + i]}", end="")
                print()    



def autochoose_outcome(net, node_id, time_slice):
    if net.get_node_temporal_type(node_id) != pysmile.NodeTemporalType.PLATE:
        raise TypeError(f"'{node_id}' non è un nodo temporale (PLATE).")

    outcome_count = net.get_outcome_count(node_id)
    probs = net.get_node_value(node_id)[time_slice*outcome_count:(time_slice+1)*outcome_count]
    # print(f"Probabilità per nodo {net.get_node_name(node_id)}: {probs}")
    outcomes = [net.get_outcome_id(node_id, i) for i in range(outcome_count)]
    chosen_outcome = random.choices(outcomes, weights=probs)[0]
    net.set_temporal_evidence(node_id, time_slice, chosen_outcome)
    net.update_beliefs()
    print(f"Il risultato di {net.get_node_name(node_id)} è stato campionato come: {chosen_outcome}")
    return None


def ask_user_decision(net, node_id, time_slice):
    if net.get_node_type(node_id) != pysmile.NodeType.DECISION:
        raise TypeError(f"'{node_id}' non è un nodo decisione.")
    
    print(f"Vuoi effettuare {net.get_node_name(node_id)}:")
    outcome_count = net.get_outcome_count(node_id)
    for i in range(outcome_count):
        outcome = net.get_outcome_id(node_id, i)
        outcome_EU = net.get_node_value(node_id)[time_slice*outcome_count+i]
        print(f"{i}: {outcome} (EU: {outcome_EU:.2f})")
    
    while True:
        try:
            choice = int(input("Inserisci il numero dell'opzione scelta: "))
            if 0 <= choice < net.get_outcome_count(node_id):
                chosen_outcome = net.get_outcome_id(node_id, choice)
                net.set_temporal_evidence(node_id, time_slice, chosen_outcome)
                net.update_beliefs()
                print(f"Hai scelto: {chosen_outcome}")
                return
            else:
                print("Scelta non valida. Riprova.")
        except ValueError:
            print("Input non valido. Inserisci un numero.")

def print_node(net, node_id):
    node_name = net.get_node_name(node_id)

    # Tipo di nodo
    node_type = net.get_node_type(node_id)
    if node_type == pysmile.NodeType.CPT:
        tipo = "Chance"
    elif node_type == pysmile.NodeType.DECISION:
        tipo = "Decision"
    elif node_type == pysmile.NodeType.UTILITY:
        tipo = "Utility"
    else:
        tipo = "Altro"

    node_value = net.get_node_value(node_id)
    print(f"Nodo: {node_id}, {node_name}, Tipo: {tipo}")

    if node_type == pysmile.NodeType.DECISION:
        for i in range(net.get_outcome_count(node_id)):
            outcome = net.get_outcome_id(node_id, i)
            print(f"   {outcome}: {node_value[i]:.2f} numero {i}")






if __name__ == "__main__":
    run_autopilot()
