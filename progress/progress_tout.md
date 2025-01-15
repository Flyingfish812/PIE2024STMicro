#### Partie Donnée

- [x] Nettoyage des données (4 lignes non trouvés dans "features") (11.18)
- [x] Intégration 1 (Faire la "join" de "features" sur "xref") (11.18)
- [x] Numérisation des classes 1 (11.18)
   - A - $\mathcal{N}(0.96,0.0107)$
   - B - $\mathcal{N}(0.85,0.0249)$
   - C - $\mathcal{N}(0.72,0.01779)$
- [x] Equilibrer la taille de classe 1 (11.18)
   - Suréchantillonnage sur "A" et sous-échantillonnage sur "B", "C"
- [x] Numérisation des "paquets" 1 (11.18)
   - One-hot encoding : 1 si c'est bien ce paquet, 0 sinon
- [x] Numérisation des classes 2 (12.13)
   - Embedding / Encodage par fréquence ou statistique
   - A - $\mathcal{N}(0.96,0.0107)$
   - B - $\mathcal{N}(0.84,0.0249)$
   - C - $\mathcal{N}(0.65,0.01779)$
   - D - $\mathcal{N}(0.5,0.01779)$
- [ ] Numérisation des classes 3
   - Essayer différente distributions : Normale avec moyens plus séparé, Uniforme, ...
- [ ] Numérisation des "paquets" 2
   - One-hot encoding est bon mais pas suffisante
   - Trouver une façon de montrer quel paquet est plus proche
- [ ] Essayer produit cartésien, apprentissage semi-supervisé pour "xref"

Structure d'entrée actuel :

| Nom                                 | Type     | Exemple      |
| ----------------------------------- | -------- | ------------ |
| Cross Reference Type                | object   | A            |
| MPN                                 | object   | PN-1017602   |
| Manufacturer                        | object   | MN-1030      |
| Maximum Input Offset Voltage        | float64  | 0.004        |
| Maximum Single Supply Voltage       | float64  | 30           |
| Minimum Single Supply Voltage       | float64  | 3            |
| Number of Channels per Chip         | float64  | 1            |
| Supplier_Package                    | category | SOT-23       |
| Typical Gain Bandwidth Product      | float64  | 800000       |
| MPN_comp                            | object   | PN-1017600   |
| Manufacturer_comp                   | object   | MN-1036      |
| Maximum Input Offset Voltage_comp   | float64  | 0.004        |
| Maximum Single Supply Voltage_comp  | float64  | 30           |
| Minimum Single Supply Voltage_comp  | float64  | 3            |
| Number of Channels per Chip_comp    | float64  | 1            |
| Supplier_Package_comp               | category | SOT-23       |
| Typical Gain Bandwidth Product_comp | float64  | 800000       |
| Closeness                           | float64  | 0.9535367944 |
| Maximum Input Offset Voltage_diff   | float64  | 0.0005       |
| Maximum Single Supply Voltage_diff  | float64  | 0            |
| Minimum Single Supply Voltage       | float64  | 0            |
| Number of Channels per Chip_diff    | float64  | 0            |
| Typical Gain Bandwidth Product_diff | float64  | 0            |
| Supplier_Package_diff               | int      | 1            |

#### Partie Algo

- [x] Modèle d'essai 1 (11.18)
  - Forêt aléatoire : le meilleur modèle jusqu'à ici
  - Figures de comparaison (11.28)
  - Réseau de neurone simple
- [x] Modèle d'essai 2 (12.13)
  - Régression linéaire : classes confondu
  - Régresseur Adaboost : confondu, mais mieux que régression linéaire
  - Forêt aléatoire : Il peut séparer la classe A mais confondu sur les autres
  - Régresseur à gradient boostant : Il peut séparer la classe A mais plus confondu sur les autres
  - Régresseur XGB
- [x] Modèle d'essai 3 (12.13)
  - Embedding layer sur package : difficile à adapter sur forêt aléatoire, une performance proche de "One hot encoding"
- [ ] Modèle d'essai 4
  - Spécialiser le modèle pour une donnée moitié cachée (vue comme nouveau donnée reçu)
  - D'autres réseau de neurone
  - Réseau Siamese
  - Tester nouveau fonctions de coût : MSE, softmax, Binary cross Entropy, etc.
- [ ] Combiner les travail de deux équipes

#### Partie GdP 1

- [ ] Description d'enjeux et objectifs
- [ ] Périmètre
- [ ] Description de l'équipe
- [ ] Description de la répartition de rôle
- [ ] Description de la partie prenant (Lingyun)
- [ ] Matrice SWOT (Nicolas)
- [ ] Description de l'organisation projet (fréquence de réunion)
- [ ] Indication de budget (Naceur)
- [ ] Analyse de risque (Ameni)
- [ ] Diagramme de Gantt (Shuya)

#### Temps à venir

12.22 Rendu des parties de rapport GdP

12.31 Deadline pour rendu des parties de rapport GdP

1.10 Examen bilan carbone

1.17 Rapport GdP

