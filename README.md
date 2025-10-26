# Partiel d'algorithmie - Axel Barbellion & Fritzi Frois

## Description du projet

L'algorithme présente deux méthodes qui permettent de calculer le chemin le plus court entre deux noeuds d'un graphe pondéré. Chaque méthode renvoie un couple composé du chemin trouvé et du poids(distance). Des logs sont affichés avec des prints afin de suivre le déroulé des étapes et des itérations.

## Lancement de l'algorithme

Afin de lancer l'algorithme, il faut se mettre dans le dossier `Partiel_Algo` puis exécuter le fichier avec :

```txt
python Partiel_Djikstra
```

Au lancement, l'algorithme proposera de choisir la méthode utilisée pour parcourir le graphe en écrivant 1 ou 2.

Des graphes d'exemples sont utilisé, celui du sujet et un graphe avec des villes. Le graphe peut être choisi en changeant la variable graphe :

```txt
graphe = graphe_demo
```

Les deux graphes proposés sont :

```txt
graphe_demo = {
        "A": [("B", 4), ("C", 2)],
        "B": [("C", 5), ("D", 10)],
        "C": [("E", 3)],
        "D": [("F", 11)],
        "E": [("D", 4)],
        "F": [],
        "G": [("A", 1), ("F", 2)],
    }
```

```txt
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
```

Des graphes peuvent être rajoutés.

# Explication du code

## Représentation des données

Les graphes sont des dictionnaires où chaque noeud pointe vers une liste de paires `(voisin, poids)`. Pour A\*, on génère un dictionnaire `coordonnees` qui associe à chaque noeud un couple `(x, y)` ; ces coordonnées servent à estimer la distance restante jusqu’à l’arrivée via une heuristique.

## dijkstra(graphe, depart, arrivee)

La fonction initialise plusieurs variables : `distances` qui attribue `inf` comme distance pour tous les noeuds, sauf le départ qui est fixé à `0`. Cela permet de définir leur distance comme inconnu au début et garantit qu’une première valeur calculée sera forcément plus petite que +inf , ce qui simplifie les mises à jour et permet d’identifier les noeuds inaccessibles. Le dictionnaire `predecesseurs` commence vide et mémorise à chaque noeud le chemin parcouru pour atteindre la plus courte distance. L’ensemble `visites` démarre vide puis ajoute les noeuds dont la distance devient définitive.

À chaque tour, on choisit le noeud non visité avec la plus petite distance actuelle grâce à `trouver_min_distance`. Si aucun noeud atteignable n’existe ou si le noeud choisi est la destination, on s’arrête. Sinon, on marque ce noeud comme visité, puis on essaie d'améliorer la distance de chacun de ses voisins : on évalue `nouvelle_distance = distances[noeud_actuel] + poids` et, si c’est mieux que la valeur stockée, on remplace et on note le prédécesseur. Les logs affichent le nœud choisi, l’état de `visites`, les comparaisons de distances, les mises à jour et les états globaux des dictionnaires, ce qui permet de suivre l’algorithme sans annoter le code.

## generer_coordonnees(graphe):

La fonction `generer_coordonnees(graphe)` génère automatiquement des positions pour chaqye noeud qui permet à **l'heuristique de A\*** de fonctionner même si ce ne sont pas de vrais coordonnées. Ici, la fonction génère des coordonnées différentes à chaque noeud du type `(i, 0.0)`selon l'ordre des noeuds.
Cette solution n'est pas liée aux **poids réelles** des noeuds du graphe mais utilise des coordonnées aléatoires pour qu'elle ne soit pas **nulle**. Pour que l'heuristique soit optimale et plus utile, il faudrait utiliser de vraies coordonnées comme des positions pour des villes par exemple. Si l'heuristique est nulle alors l'alogithme se comporte comme **Dijkstra**.

## Astar (graphe, coordonnees, depart, arrivee)

A\* a le même but mais ajoute une estimation du “reste à parcourir” grâce à une **heuristique**. La fonction interne `h(noeud1, noeud2)` calcule ici la distance euclidienne entre les coordonnées générées des noeuds. Le coût réel depuis le départ est stocké dans `g_score`. La structure `distances` contient la valeur **f** courante, c’est-à-dire `f = g_score + h`, utilisée pour sélectionner le prochain nœud à explorer.

Au démarrage, `g_score` vaut `+inf` partout sauf le départ, définit à `0`. La file de sélection s’appuie sur `distances`, initialisée à `+inf` avec, pour le départ, `h(depart, arrivee)`. À chaque tour, on prend le noeud non visité avec le plus petit `f`. Si c’est l’arrivée, on s’arrête. Sinon, on tente d’améliorer les voisins en calculant un `tentative_g_score = g_score[noeud_actuel] + poids`, puis un `tentative_f = tentative_g_score + h(voisin, arrivee)`. Si le `tentative_g_score` est meilleur, on met à jour `g_score`, `distances` et `predecesseurs`. Les logs détaillent ces valeurs (`g_score`, heuristique, `f`) pour rendre le rôle de l’heuristique lisible.

Lorsque l’heuristique **n’exagère jamais** la vraie distance restante, A\* trouve un plus court chemin tout en explorant généralement **moins** de noeuds que Dijkstra.

## min_distance(distances, visites)

Cette fonction cherche, parmi tous les noeuds, celui qui n’a pas encore été visité et dont la valeur suivie (pour Dijkstra, la distance ; pour A\*, la valeur `f`) est la plus petite. Elle démarre avec `min_distance = +inf` pour que la première valeur utile la remplace naturellement ; si rien n’est atteignable, elle renvoie `(None, +inf)`.

## reconstruire_chemin(predecesseurs, depart, arrivee)

La reconstruction commence à l’arrivée et remonte de prédécesseur en prédécesseur jusqu’au départ. Si l’arrivée n’a pas de prédécesseur et qu’elle n’est pas le départ, il n’existe pas de chemin et la fonction renvoie `None`. Sinon, on récupère les noeuds trouvés, on ajoute ensuite le départ et on inverse la liste pour obtenir le bon chemin dans le bon sens.
