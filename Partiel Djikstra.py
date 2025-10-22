def trouver_min_distance(distances, visites):
    """
    Trouve le noeud non visité avec la plus petite distance
    - distances: dictionnaire des distances actuelles pour chaque noeud
    - visites: ensemble des noeuds déjà visités
    """
    min_distance = float('inf')  # Initialise avec l'infini pour trouver le minimum
    min_noeud = None
    for noeud in distances:
        # Si le noeud n'est pas visité et a une distance plus petite que le minimum actuel
        if noeud not in visites and distances[noeud] < min_distance:
            min_distance = distances[noeud]
            min_noeud = noeud
    return min_noeud, min_distance

def dijkstra(graphe, depart, arrivee):
    """
    Implémentation de l'algorithme de Dijkstra sans file de priorité
    - graphe: dictionnaire des noeuds et leurs connexions avec poids
    - depart: noeud de départ
    - arrivee: noeud d'arrivée
    """
    # Initialisation des distances à l'infini sauf pour le départ
    distances = {noeud: float("inf") for noeud in graphe}
    distances[depart] = 0
    predecesseurs = {}  # Pour reconstruire le chemin
    visites = set()    # Ensemble des noeuds déjà traités
    
    print(f"État initial - Distances: {distances}")
    print(f"Départ: {depart}, Arrivée: {arrivee}\n")

    iteration = 1
    while True:
        print(f"\nItération {iteration}-----------")
        # Trouve le noeud non visité le plus proche
        noeud_actuel, dist_actuelle = trouver_min_distance(distances, visites)
        print(f"Noeud sélectionné: {noeud_actuel} (distance: {dist_actuelle})")
        
        # Arrêt si plus de noeuds accessibles ou si on atteint l'arrivée
        if noeud_actuel is None or noeud_actuel == arrivee:
            print("Fin de l'algorithme - Arrivée atteinte ou plus de noeuds accessibles")
            break
            
        visites.add(noeud_actuel)  # Marque le noeud comme visité
        print(f"Noeuds visités: {visites}")
        
        # Examine tous les voisins du noeud actuel
        for voisin, poids in graphe[noeud_actuel]:
            if voisin in visites:  # Skip si déjà visité
                print(f"Voisin {voisin} déjà visité, on passe")
                continue
                
            # Calcule la nouvelle distance possible vers le voisin
            nouvelle_distance = dist_actuelle + poids
            print(f"Analyse du voisin {voisin} - Distance actuelle: {distances[voisin]}, Nouvelle distance possible: {nouvelle_distance}")
            
            # Si on trouve un chemin plus court
            if nouvelle_distance < distances[voisin]:
                distances[voisin] = nouvelle_distance      # Met à jour la distance
                predecesseurs[voisin] = noeud_actuel      # Met à jour le prédécesseur
                print(f"Mise à jour - Noeud: {voisin}, Nouvelle distance: {nouvelle_distance}, Prédécesseur: {noeud_actuel}")

        print(f"État des distances: {distances}")
        print(f"État des prédécesseurs: {predecesseurs}")
        iteration += 1

    # Reconstruit et retourne le chemin final
    chemin = reconstruire_chemin(predecesseurs, depart, arrivee)
    print("\n=== Résultat final ===")
    print(f"Distances finales: {distances}")
    print(f"Prédécesseurs finaux: {predecesseurs}")
    
    if chemin is None:
        return None, float("inf")
    return chemin, distances[arrivee]

def reconstruire_chemin(predecesseurs, depart, arrivee):
    """
    Reconstruit le chemin à partir des prédécesseurs
    - predecesseurs: dictionnaire des prédécesseurs pour chaque noeud
    - depart: noeud de départ
    - arrivee: noeud d'arrivée
    """
    # Vérifie si un chemin existe
    if arrivee not in predecesseurs and arrivee != depart:
        return None

    # Reconstruit le chemin en remontant les prédécesseurs
    chemin = []
    noeud = arrivee
    while noeud != depart:
        chemin.append(noeud)
        noeud = predecesseurs.get(noeud)
        if noeud is None:  # Chemin impossible
            return None
    chemin.append(depart)
    chemin.reverse()  # Inverse le chemin pour avoir départ -> arrivée
    return chemin




if __name__ == "__main__":
    # Exemple de graphe avec les connexions et leurs poids
    graphe = {
        "A": [("B", 4), ("C", 2)],  # A est connecté à B (poids 4) et C (poids 2)
        "B": [("C", 5), ("D", 10)], # B est connecté à C (poids 5) et D (poids 10)
        "C": [("E", 3)],            # C est connecté à E (poids 3)
        "D": [("F", 11)],           # D est connecté à F (poids 11)
        "E": [("D", 4)],            # E est connecté à D (poids 4)
        "F": []                      # F n'a pas de connexions sortantes
    }
    
    # Test de l'algorithme
    depart, arrivee = "A", "D"
    chemin, distance = dijkstra(graphe, depart, arrivee)

    # Affichage des résultats
    if chemin is None:
        print(f"Aucun chemin trouvé entre {depart} et {arrivee}.")
    else:
        print(f"Chemin le plus court de {depart} à {arrivee} : {' -> '.join(chemin)}")
        print(f"Distance totale : {distance}")
