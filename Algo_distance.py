import math
import sys

def trouver_min_distance(distances, visites):

    min_distance = float("inf")
    min_noeud = None
    for noeud in distances:
        if noeud not in visites and distances[noeud] < min_distance:
            min_distance = distances[noeud]
            min_noeud = noeud
    return min_noeud, min_distance

def generer_coordonnees(graphe):
    return {
        noeud: (i , 0.0)
        for i, noeud in enumerate(sorted(graphe.keys()))
    }

def dijkstra(graphe, depart, arrivee):

    distances = {noeud: float("inf") for noeud in graphe}
    distances[depart] = 0
    predecesseurs = {}
    visites = set()

    print(f"Début - Distances: {distances}")
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
                print(f"Voisin {voisin} déjà visité")
                continue

            nouvelle_distance = dist_actuelle + poids
            print(
                f"Analyse du voisin {voisin} - Distance actuelle: "
                f"{distances[voisin]}, Nouvelle distance possible: {nouvelle_distance}"
            )

            if nouvelle_distance < distances[voisin]:
                distances[voisin] = nouvelle_distance
                predecesseurs[voisin] = noeud_actuel
                print(
                    f"Mise à jour - Noeud: {voisin}, Nouvelle distance: {nouvelle_distance}, "
                    f"Prédécesseur: {noeud_actuel}"
                )

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


def a_star(graphe, depart, arrivee):
    coordonnees = generer_coordonnees(graphe)
    def h(noeud1, noeud2):
        (x1, y1) = coordonnees[noeud1]
        (x2, y2) = coordonnees[noeud2]
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    g_score = {noeud: float("inf") for noeud in graphe}
    g_score[depart] = 0

    distances = {noeud: float("inf") for noeud in graphe}
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

        print(
            f"Noeud sélectionné: {noeud_actuel} (distances: {dist_actuelle:.2f}, "
            f"g_score: {g_score[noeud_actuel]:.2f})"
        )

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

            print(
                f"Analyse du voisin {voisin} - g_score actuel: {g_score[voisin]:.2f}, "
                f"tentative g_score: {tentative_g_score:.2f}, heuristique: {heuristique:.2f}"
            )

            if tentative_g_score < g_score[voisin]:
                predecesseurs[voisin] = noeud_actuel
                g_score[voisin] = tentative_g_score
                distances[voisin] = tentative_distance
                print(
                    f"Mise à jour - Noeud: {voisin}, g_score: {tentative_g_score:.2f}, "
                    f"distance: {tentative_distance:.2f}, Prédécesseur: {noeud_actuel}"
                )

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
        return None, float("inf")
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
    graphe_demo = {
        "A": [("B", 4), ("C", 2)],
        "B": [("C", 5), ("D", 10)],
        "C": [("E", 3)],
        "D": [("F", 11)],
        "E": [("D", 4)],
        "F": [],
        "G": [("A", 1), ("F", 2)],
    }

    graphe_villes = {
        "Paris": [("Lyon", 465), ("Lille", 225)],
        "Lyon": [("Marseille", 315)],
        "Lille": [("Paris", 225), ("Nantes", 600)],
        "Marseille": [("Nice", 200), ("Toulouse", 400)],
        "Nantes": [("Bordeaux", 350), ("Lyon", 600)],
        "Bordeaux": [("Toulouse", 245)],
        "Nice": [("Lyon", 470)],
        "Toulouse": [("Montpellier", 240)],
        "Montpellier": [("Marseille", 165)],
    }

    graphe = graphe_villes

    print("=" * 60)
    print("MENU")
    print("=" * 60)
    print("1. Dijkstra")
    print("2. A*")
    print("=" * 60)

    choix = input("Choisissez une option (1 ou 2) : ").strip()
    if choix not in {"1", "2"}:
        print("\nChoix invalide. Veuillez relancer le programme et choisir 1 ou 2.")
        sys.exit(1)

    noeuds_disponibles = sorted(graphe.keys())
    print(f"\nNoeuds disponibles dans le graphe : {', '.join(noeuds_disponibles)}")

    correspondance_noeuds = {nom.upper(): nom for nom in noeuds_disponibles}
    depart_saisi = input("Choisissez le noeud de départ : ").strip().upper()
    arrivee_saisi = input("Choisissez le noeud d'arrivée : ").strip().upper()

    depart = correspondance_noeuds.get(depart_saisi)
    arrivee = correspondance_noeuds.get(arrivee_saisi)

    if depart is None or arrivee is None:
        print(f"\nErreur : Les noeuds doivent être parmi {', '.join(noeuds_disponibles)}")
        sys.exit(1)

    if choix == "1":
        print("\n" + "=" * 60)
        print("ALGORITHME DE DIJKSTRA")
        print("=" * 60 + "\n")

        chemin, distance = dijkstra(graphe, depart, arrivee)

        if chemin is None:
            print(f"\nAucun chemin trouvé entre {depart} et {arrivee}.")
        else:
            print(f"\nChemin le plus court de {depart} à {arrivee} : {' -> '.join(chemin)}")
            print(f"Distance totale : {distance}")

    else:
        print("\n" + "=" * 60)
        print("ALGORITHME A*")
        print("=" * 60 + "\n")

        chemin, cout = a_star(graphe, depart, arrivee)

        if chemin is None:
            print(f"\nAucun chemin trouvé entre {depart} et {arrivee}.")
        else:
            print(f"\nChemin trouvé par A* : {' -> '.join(chemin)}")
            print(f"Coût total : {cout}")
