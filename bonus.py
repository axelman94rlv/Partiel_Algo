import math

def trouver_min_distance(distances, visites):

    min_distance = float('inf')
    min_noeud = None
    for noeud in distances:
        if noeud not in visites and distances[noeud] < min_distance:
            min_distance = distances[noeud]
            min_noeud = noeud
    return min_noeud, min_distance

def dijkstra(graphe, depart, arrivee):

    distances = {noeud: float("inf") for noeud in graphe}
    distances[depart] = 0
    predecesseurs = {} 
    visites = set()
    
    print(f"État initial - Distances: {distances}")
    print(f"Départ: {depart}, Arrivée: {arrivee}\n")

    iteration = 1
    while True:
        print(f"\nItération {iteration}-----------")
        noeud_actuel, dist_actuelle = trouver_min_distance(distances, visites)
        print(f"Noeud sélectionné: {noeud_actuel} (distance: {dist_actuelle})")
        
        if noeud_actuel is None or noeud_actuel == arrivee:
            print("Fin de l'algorithme - Arrivée atteinte ou plus de noeuds accessibles")
            break
            
        visites.add(noeud_actuel)
        print(f"Noeuds visités: {visites}")
        
        for voisin, poids in graphe[noeud_actuel]:
            if voisin in visites:
                print(f"Voisin {voisin} déjà visité, on passe")
                continue
                
            nouvelle_distance = dist_actuelle + poids
            print(f"Analyse du voisin {voisin} - Distance actuelle: {distances[voisin]}, Nouvelle distance possible: {nouvelle_distance}")
            
            if nouvelle_distance < distances[voisin]:
                distances[voisin] = nouvelle_distance
                predecesseurs[voisin] = noeud_actuel 
                print(f"Mise à jour - Noeud: {voisin}, Nouvelle distance: {nouvelle_distance}, Prédécesseur: {noeud_actuel}")

        print(f"État des distances: {distances}")
        print(f"État des prédécesseurs: {predecesseurs}")
        iteration += 1

    chemin = reconstruire_chemin(predecesseurs, depart, arrivee)
    print("\n=== Résultat final ===")
    print(f"Distances finales: {distances}")
    print(f"Prédécesseurs finaux: {predecesseurs}")
    
    if chemin is None:
        return None, float("inf")
    return chemin, distances[arrivee]

def a_star(graphe, coordonnees, depart, arrivee):
    def h(noeud1, noeud2):
        (x1, y1) = coordonnees[noeud1]
        (x2, y2) = coordonnees[noeud2]
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    
    g_score = {noeud: float('inf') for noeud in graphe}
    g_score[depart] = 0
    
    distances = {noeud: float('inf') for noeud in graphe}
    distances[depart] = h(depart, arrivee)
    
    predecesseurs = {}
    visites = set()
    
    print(f"État initial - g_score: {g_score}")
    print(f"État initial - distances: {distances}")
    print(f"Départ: {depart}, Arrivée: {arrivee}\n")
    
    iteration = 1
    while True:
        print(f"\nItération {iteration}-----------")
        noeud_actuel, dist_actuelle = trouver_min_distance(distances, visites)
        
        if noeud_actuel is None:
            print("Fin de l'algorithme - Plus de noeuds accessibles")
            break
        
        print(f"Noeud sélectionné: {noeud_actuel} (distances: {dist_actuelle:.2f}, g_score: {g_score[noeud_actuel]:.2f})")
        
        if noeud_actuel == arrivee:
            print("Fin de l'algorithme - Arrivée atteinte")
            break
        
        visites.add(noeud_actuel)
        print(f"Noeuds visités: {visites}") 

        for voisin, poids in graphe[noeud_actuel]:
            if voisin in visites:
                print(f"Voisin {voisin} déjà visité, on passe")
                continue
            
            tentative_g_score = g_score[noeud_actuel] + poids
            heuristique = h(voisin, arrivee)
            tentative_distance = tentative_g_score + heuristique
            
            print(f"Analyse du voisin {voisin} - g_score actuel: {g_score[voisin]:.2f}, tentative g_score: {tentative_g_score:.2f}, heuristique: {heuristique:.2f}")
            
            if tentative_g_score < g_score[voisin]:
                predecesseurs[voisin] = noeud_actuel
                g_score[voisin] = tentative_g_score
                distances[voisin] = tentative_distance
                print(f"Mise à jour - Noeud: {voisin}, g_score: {tentative_g_score:.2f}, distance: {tentative_distance:.2f}, Prédécesseur: {noeud_actuel}")
        
        print(f"État des g_scores: {g_score}")
        print(f"État des distances: {distances}")
        print(f"État des prédécesseurs: {predecesseurs}")
        iteration += 1
    
    chemin = reconstruire_chemin(predecesseurs, depart, arrivee)
    print("\n=== Résultat final ===")
    print(f"g_scores finaux: {g_score}")
    print(f"distances finaux: {distances}")
    print(f"Prédécesseurs finaux: {predecesseurs}")
    
    if chemin is None:
        return None, float('inf')
    return chemin, g_score[arrivee]

def reconstruire_chemin(predecesseurs, depart, arrivee):

    if arrivee not in predecesseurs and arrivee != depart:
        return None

    chemin = []
    noeud = arrivee
    while noeud != depart:
        chemin.append(noeud)
        noeud = predecesseurs.get(noeud)
        if noeud is None:
            return None
    chemin.append(depart)
    chemin.reverse() 
    return chemin


if __name__ == "__main__":
    # Définition unique du graphe pour les deux algorithmes
    graphe = {
        "A": [("B", 4), ("C", 2)],  
        "B": [("C", 5), ("D", 10)], 
        "C": [("E", 3)],            
        "D": [("F", 11)],           
        "E": [("D", 4)],           
        "F": []                    
    }
    
    # Coordonnées pour A* (définies une seule fois)
    coordonnees = {
        "A": (0, 0),
        "B": (4, 0),
        "C": (2, 2),
        "D": (8, 3),
        "E": (4, 4),
        "F": (10, 5)
    }
    
    print("=" * 60)
    print("MENU - ALGORITHMES DE RECHERCHE DE CHEMIN")
    print("=" * 60)
    print("1. Distance la plus courte (Dijkstra)")
    print("2. Transformation en A*")
    print("=" * 60)
    
    choix = input("Choisissez une option (1 ou 2) : ")
    
    print(f"\nNoeuds disponibles dans le graphe : {', '.join(sorted(graphe.keys()))}")
    depart = input("Choisissez le noeud de départ : ").upper()
    arrivee = input("Choisissez le noeud d'arrivée : ").upper()
    
    # Vérification unique de l'existence des noeuds
    if depart not in graphe or arrivee not in graphe:
        print(f"\nErreur : Les noeuds doivent être parmi {', '.join(sorted(graphe.keys()))}")
    else:
        if choix == "1":
            print("\n" + "=" * 60)
            print("ALGORITHME DE DIJKSTRA - DISTANCE LA PLUS COURTE")
            print("=" * 60 + "\n")
            
            chemin, distance = dijkstra(graphe, depart, arrivee)

            if chemin is None:
                print(f"\nAucun chemin trouvé entre {depart} et {arrivee}.")
            else:
                print(f"\nChemin le plus court de {depart} à {arrivee} : {' -> '.join(chemin)}")
                print(f"Distance totale : {distance}")
        
        elif choix == "2":
            print("\n" + "=" * 60)
            print("ALGORITHME A* - TRANSFORMATION")
            print("=" * 60 + "\n")
            
            chemin, cout = a_star(graphe, coordonnees, depart, arrivee)
            
            if chemin is None:
                print(f"\nAucun chemin trouvé entre {depart} et {arrivee}.")
            else:
                print(f"\nChemin trouvé par A* : {' -> '.join(chemin)}")
                print(f"Coût total : {cout}")
        
        else:
            print("\nChoix invalide. Veuillez relancer le programme et choisir 1 ou 2.")
            