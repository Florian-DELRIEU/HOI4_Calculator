# Simulateur de bataille terrestre HOI4

Calculette de bataille isolée reproduisant fidèlement le moteur de combat
terrestre de *Hearts of Iron IV* : deux camps (attaquant / défenseur), un
déroulé **tour par tour (1 tour = 1 heure de jeu)**, les formules et tables
officielles du wiki ([Land battle](https://hoi4.paradoxwikis.com/Land_battle),
[Combat tactics](https://hoi4.paradoxwikis.com/Combat_tactics),
[Land units](https://hoi4.paradoxwikis.com/Land_units),
[Terrain](https://hoi4.paradoxwikis.com/Terrain),
[Weather](https://hoi4.paradoxwikis.com/Weather)).

Ce n'est **pas** un jeu de stratégie : pas de carte, pas de recherche, pas de
production. Les systèmes hors périmètre (aviation, ravitaillement,
renseignement…) sont exposés comme des **curseurs manuels** appliqués en
modificateurs de combat.

## Lancer en développement

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows  (source .venv/bin/activate sur macOS)
pip install -r requirements.txt
python main.py
```

Tests du moteur :

```bash
python -m pytest tests
```

## Architecture

| Dossier | Rôle |
|---|---|
| `engine/` | Moteur de combat pur Python, **aucune dépendance UI**, testé unitairement. `rng.py` (arrondi probabiliste, dés), `division.py`, `combat.py` (ciblage §8.3, dégâts §8.4), `modifiers.py` (cumul multiplicatif §8.5, plancher 1 %), `tactics.py` (initiative déterministe §9.2, tirage pondéré, contres, phases), `composition.py` (agrégation bataillons §6.1), `battle.py` (camps, front/réserves, tours), `params.py`, `logs.py`, `paths.py`. |
| `data/` | Tables de référence JSON, séparées du code : `terrains.json`, `weather.json`, `battalions.json`, `tactics.json` (54 tactiques officielles, 6 phases), `experience.json`, `leader_traits.json`. |
| `gui/` | PySide6 : fenêtre de bataille, éditeur de divisions (composition **ou** stats manuelles), éditeur de leaders, éditeur de tactiques personnalisées, gestionnaire de sauvegardes, thème clair/sombre. |
| `persistence/` | Lecture/écriture JSON : templates de division (compatibles avec l'ancien format `Nom de Template`/`PV`/`Attaque`…), leaders, sauvegardes de bataille nommées, export CSV des logs. |
| `saves/` | Données utilisateur : `divisions/` (rangeables en sous-dossiers), `battles/`, `leaders.json`, `tactics_custom.json`. |

### Pourquoi PySide6 ?

Richesse des widgets (tableaux, dialogues, tooltips riches sur les logs),
theming clair/sombre natif via `Fusion` + palettes, et licence **LGPL**
compatible avec la distribution d'un exécutable. Un seul framework, pas de
mélange.

## Fidélité au jeu — points clés

- **Dégâts** (§8.4) : nb d'attaques = arrondi *probabiliste* de
  (attaque modifiée / 10) ; toucher 10 % tant que la cible a des défenses,
  40 % ensuite ; PV = 1d2 × 0,06 ; organisation = 1d4 (1d6 si le blindage de
  l'attaquant n'est pas percé) × 0,053.
- **Paliers piercing/armor** : ≥100 % → ×1 ; ≥75 % → ×0,8 ; ≥50 % → ×0,65 ;
  <50 % → ×0,5.
- **Force** : dégâts mis à l'échelle par paliers de 10 % des PV restants.
- **Ciblage** : largeur d'engagement 2×, part coordonnée
  min(35 % + coordination × (1 + initiative), 90 %) vers la cible prioritaire.
- **Tactiques** : re-sélection toutes les 12 h ; l'Initiative est
  **déterministe** (compétences des généraux, +5 si avantage de recon,
  égalité → défenseur) ; le perdant choisit en premier, le gagnant a +35 %
  de poids par point d'avantage sur les tactiques qui contrent ; une tactique
  contrée perd tous ses effets. Override manuel possible par camp, et
  tactiques personnalisées via l'éditeur.
- **Fort** : −15 %/niveau, chaque direction d'attaque supplémentaire annule
  un niveau (jamais le dernier) ; érosion progressive par dégâts collatéraux
  (5 % par attaque).
- **Largeur** : pénalité de dépassement plafonnée à −33 % ; empilement
  −2 %/division au-delà de 5 + 3 par direction supplémentaire ; réserves à
  2 %/heure.

### Écarts assumés / choix d'interprétation

- **Dé d'organisation 1d6** : le CDC dit « son piercing dépasse l'armor de la
  cible » ; le moteur applique la règle réelle du jeu (« armor de l'attaquant
  > piercing de la cible », l'unité *bouge plus librement* car non percée).
- **Largeur par direction supplémentaire** : le bonus **par terrain** (§7.1,
  ex. +35 en plaine) est utilisé, plus précis que le « +40 » générique du §8.1.
- **Limite d'empilement** : appliquée aux deux camps (comme dans le projet de
  référence), le CDC ne distinguant pas les camps.
- **Stats des bataillons** : équipement de **base** (table « Unit types » du
  wiki). La dureté des châssis super-lourds n'est pas affichée sur le wiki et
  est approximée depuis le palier lourd (voir `data/battalions.json`).
- Débarquement amphibie : version simplifiée −50 % fixe (§7.2).

## Empaqueter un exécutable

### Windows

```powershell
.venv\Scripts\pyinstaller --noconfirm --windowed --name "SimulateurHOI4" --add-data "data;data" main.py
```

L'application est générée dans `dist/SimulateurHOI4/SimulateurHOI4.exe`.
Le dossier `saves/` est créé **à côté de l'exécutable** au premier lancement
(avec deux templates d'exemple). Pour un fichier unique, ajouter `--onefile`
(démarrage plus lent).

### macOS

À exécuter **sur un Mac** (PyInstaller ne cross-compile pas) :

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pyinstaller --noconfirm --windowed --name "SimulateurHOI4" --add-data "data:data" main.py
```

Attention au séparateur `--add-data` : `;` sous Windows, `:` sous macOS/Linux.
Le bundle `.app` est généré dans `dist/`. Pour distribuer hors de votre
machine, signez/notarisez le bundle ou demandez aux utilisateurs d'autoriser
l'app dans *Réglages > Confidentialité et sécurité*.

## Format des sauvegardes

- **Templates de division** : un JSON par template dans `saves/divisions/`
  (sous-dossiers libres), clés héritées de l'ancien format (`Nom de Template`,
  `PV`, `Organisation`, `Soft Attack`, `Hard Attack`, `Defense`,
  `Attaque` = percée, `Piercing`, `Armor`, `Hardness`, `Width`, `Initiative`)
  étendues (`Experience`, `Recon`, `Bataillons`, `Compagnies de soutien`).
  Les anciens fichiers « liste » sont lus tels quels et importables.
- **Batailles** : `saves/battles/<nom>.json` — état complet (§12), y compris
  l'état du générateur aléatoire : recharger puis rejouer donne exactement
  la même suite de bataille.
- **Logs** : export CSV (`;` comme séparateur, UTF-8 BOM pour Excel) avec
  tour, camp, divisions, tactique, attaques/défenses, coups, dégâts PV/org,
  facteurs cumulés et détail des bonus.
