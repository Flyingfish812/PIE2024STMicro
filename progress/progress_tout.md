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
- [ ] Numérisation des classes 2
   - Essayer différente distributions : Normale avec moyens plus séparé, Uniforme, ...
- [ ] Numérisation des "paquets" 2
   - One-hot encoding est bon mais pas suffisante
   - Trouver une façon de montrer quel paquet est plus proche
- [ ] Essayer produit cartésien, apprentissage semi-supervisé pour "xref"

Structure d'entrée actuel :

| Nom                                 | Type     | Exemple    |
| ----------------------------------- | -------- | ---------- |
| STMicro MPN                         | object   | PN-1017602 |
| STMicro Name                        | object   | MN-1030    |
| Competitor MPN                      | object   | PN-1017600 |
| Competitor Name                     | object   | MN-1036    |
| Cross Reference Type                | object   | A          |
| MPN                                 | object   | PN-1017602 |
| Manufacturer                        | object   | MN-1030    |
| Maximum Input Offset Voltage        | float64  | 0.004      |
| Maximum Single Supply Voltage       | float64  | 30         |
| Minimum Single Supply Voltage       | float64  | 3          |
| Number of Channels per Chip         | float64  | 1          |
| Supplier_Package                    | category | SOT-23     |
| Typical Gain Bandwidth Product      | float64  | 800000     |
| MPN_comp                            | object   | PN-1017600 |
| Manufacturer_comp                   | object   | MN-1036    |
| Maximum Input Offset Voltage_comp   | float64  | 0.004      |
| Maximum Single Supply Voltage_comp  | float64  | 30         |
| Minimum Single Supply Voltage_comp  | float64  | 3          |
| Number of Channels per Chip_comp    | float64  | 1          |
| Supplier_Package_comp               | category | SOT-23     |
| Typical Gain Bandwidth Product_comp | float64  | 800000     |



#### Partie Algo

- [x] Modèle d'essai 1 (11.18)
  - Forêt aléatoire : le meilleur modèle jusqu'à ici
  - Figures de comparaison (11.28)
  - Réseau de neurone simple
- [ ] Modèle d'essai 2
  - Spécialiser le modèle pour une donnée moitié cachée (vue comme nouveau donnée reçu)
  - D'autres réseau de neurone