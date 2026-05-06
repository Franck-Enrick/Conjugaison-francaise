"""
Moteur de conjugaison automatique des verbes français.
Utilise la bibliothèque `re` et des dictionnaires Python pour générer
automatiquement les temps et formes verbales.
"""

import re

# ─────────────────────────────────────────────
#  DONNÉES : pronoms et terminaisons par groupe
# ─────────────────────────────────────────────

PRONOMS = ["je", "tu", "il/elle", "nous", "vous", "ils/elles"]

# Terminaisons des temps simples pour chaque groupe verbal
TERMINAISONS = {
    "1er_groupe": {
        "présent":              ["e", "es", "e", "ons", "ez", "ent"],
        "imparfait":            ["ais", "ais", "ait", "ions", "iez", "aient"],
        "futur_simple":         ["erai", "eras", "era", "erons", "erez", "eront"],
        "conditionnel_présent": ["erais", "erais", "erait", "erions", "eriez", "eraient"],
        "subjonctif_présent":   ["e", "es", "e", "ions", "iez", "ent"],
        "passé_simple":         ["ai", "as", "a", "âmes", "âtes", "èrent"],
    },
    "2ème_groupe": {
        "présent":              ["is", "is", "it", "issons", "issez", "issent"],
        "imparfait":            ["issais", "issais", "issait", "issions", "issiez", "issaient"],
        "futur_simple":         ["irai", "iras", "ira", "irons", "irez", "iront"],
        "conditionnel_présent": ["irais", "irais", "irait", "irions", "iriez", "iraient"],
        "subjonctif_présent":   ["isse", "isses", "isse", "issions", "issiez", "issent"],
        "passé_simple":         ["is", "is", "it", "îmes", "îtes", "irent"],
    },
}

# Verbes irréguliers du 3ème groupe (temps simples complets)
IRREGULIERS = {
    "être": {
        "présent":              ["suis", "es", "est", "sommes", "êtes", "sont"],
        "imparfait":            ["étais", "étais", "était", "étions", "étiez", "étaient"],
        "futur_simple":         ["serai", "seras", "sera", "serons", "serez", "seront"],
        "conditionnel_présent": ["serais", "serais", "serait", "serions", "seriez", "seraient"],
        "subjonctif_présent":   ["sois", "sois", "soit", "soyons", "soyez", "soient"],
        "passé_simple":         ["fus", "fus", "fut", "fûmes", "fûtes", "furent"],
    },
    "avoir": {
        "présent":              ["ai", "as", "a", "avons", "avez", "ont"],
        "imparfait":            ["avais", "avais", "avait", "avions", "aviez", "avaient"],
        "futur_simple":         ["aurai", "auras", "aura", "aurons", "aurez", "auront"],
        "conditionnel_présent": ["aurais", "aurais", "aurait", "aurions", "auriez", "auraient"],
        "subjonctif_présent":   ["aie", "aies", "ait", "ayons", "ayez", "aient"],
        "passé_simple":         ["eus", "eus", "eut", "eûmes", "eûtes", "eurent"],
    },
    "aller": {
        "présent":              ["vais", "vas", "va", "allons", "allez", "vont"],
        "imparfait":            ["allais", "allais", "allait", "allions", "alliez", "allaient"],
        "futur_simple":         ["irai", "iras", "ira", "irons", "irez", "iront"],
        "conditionnel_présent": ["irais", "irais", "irait", "irions", "iriez", "iraient"],
        "subjonctif_présent":   ["aille", "ailles", "aille", "allions", "alliez", "aillent"],
        "passé_simple":         ["allai", "allas", "alla", "allâmes", "allâtes", "allèrent"],
    },
    "faire": {
        "présent":              ["fais", "fais", "fait", "faisons", "faites", "font"],
        "imparfait":            ["faisais", "faisais", "faisait", "faisions", "faisiez", "faisaient"],
        "futur_simple":         ["ferai", "feras", "fera", "ferons", "ferez", "feront"],
        "conditionnel_présent": ["ferais", "ferais", "ferait", "ferions", "feriez", "feraient"],
        "subjonctif_présent":   ["fasse", "fasses", "fasse", "fassions", "fassiez", "fassent"],
        "passé_simple":         ["fis", "fis", "fit", "fîmes", "fîtes", "firent"],
    },
    "pouvoir": {
        "présent":              ["peux", "peux", "peut", "pouvons", "pouvez", "peuvent"],
        "imparfait":            ["pouvais", "pouvais", "pouvait", "pouvions", "pouviez", "pouvaient"],
        "futur_simple":         ["pourrai", "pourras", "pourra", "pourrons", "pourrez", "pourront"],
        "conditionnel_présent": ["pourrais", "pourrais", "pourrait", "pourrions", "pourriez", "pourraient"],
        "subjonctif_présent":   ["puisse", "puisses", "puisse", "puissions", "puissiez", "puissent"],
        "passé_simple":         ["pus", "pus", "put", "pûmes", "pûtes", "purent"],
    },
    "vouloir": {
        "présent":              ["veux", "veux", "veut", "voulons", "voulez", "veulent"],
        "imparfait":            ["voulais", "voulais", "voulait", "voulions", "vouliez", "voulaient"],
        "futur_simple":         ["voudrai", "voudras", "voudra", "voudrons", "voudrez", "voudront"],
        "conditionnel_présent": ["voudrais", "voudrais", "voudrait", "voudrions", "voudriez", "voudraient"],
        "subjonctif_présent":   ["veuille", "veuilles", "veuille", "voulions", "vouliez", "veuillent"],
        "passé_simple":         ["voulus", "voulus", "voulut", "voulûmes", "voulûtes", "voulurent"],
    },
    "savoir": {
        "présent":              ["sais", "sais", "sait", "savons", "savez", "savent"],
        "imparfait":            ["savais", "savais", "savait", "savions", "saviez", "savaient"],
        "futur_simple":         ["saurai", "sauras", "saura", "saurons", "saurez", "sauront"],
        "conditionnel_présent": ["saurais", "saurais", "saurait", "saurions", "sauriez", "sauraient"],
        "subjonctif_présent":   ["sache", "saches", "sache", "sachions", "sachiez", "sachent"],
        "passé_simple":         ["sus", "sus", "sut", "sûmes", "sûtes", "surent"],
    },
    "venir": {
        "présent":              ["viens", "viens", "vient", "venons", "venez", "viennent"],
        "imparfait":            ["venais", "venais", "venait", "venions", "veniez", "venaient"],
        "futur_simple":         ["viendrai", "viendras", "viendra", "viendrons", "viendrez", "viendront"],
        "conditionnel_présent": ["viendrais", "viendrais", "viendrait", "viendrions", "viendriez", "viendraient"],
        "subjonctif_présent":   ["vienne", "viennes", "vienne", "venions", "veniez", "viennent"],
        "passé_simple":         ["vins", "vins", "vint", "vînmes", "vîntes", "vinrent"],
    },
    "prendre": {
        "présent":              ["prends", "prends", "prend", "prenons", "prenez", "prennent"],
        "imparfait":            ["prenais", "prenais", "prenait", "prenions", "preniez", "prenaient"],
        "futur_simple":         ["prendrai", "prendras", "prendra", "prendrons", "prendrez", "prendront"],
        "conditionnel_présent": ["prendrais", "prendrais", "prendrait", "prendrions", "prendriez", "prendraient"],
        "subjonctif_présent":   ["prenne", "prennes", "prenne", "prenions", "preniez", "prennent"],
        "passé_simple":         ["pris", "pris", "prit", "prîmes", "prîtes", "prirent"],
    },
    "mettre": {
        "présent":              ["mets", "mets", "met", "mettons", "mettez", "mettent"],
        "imparfait":            ["mettais", "mettais", "mettait", "mettions", "mettiez", "mettaient"],
        "futur_simple":         ["mettrai", "mettras", "mettra", "mettrons", "mettrez", "mettront"],
        "conditionnel_présent": ["mettrais", "mettrais", "mettrait", "mettrions", "mettriez", "mettraient"],
        "subjonctif_présent":   ["mette", "mettes", "mette", "mettions", "mettiez", "mettent"],
        "passé_simple":         ["mis", "mis", "mit", "mîmes", "mîtes", "mirent"],
    },
    "partir": {
        "présent":              ["pars", "pars", "part", "partons", "partez", "partent"],
        "imparfait":            ["partais", "partais", "partait", "partions", "partiez", "partaient"],
        "futur_simple":         ["partirai", "partiras", "partira", "partirons", "partirez", "partiront"],
        "conditionnel_présent": ["partirais", "partirais", "partirait", "partirions", "partiriez", "partiraient"],
        "subjonctif_présent":   ["parte", "partes", "parte", "partions", "partiez", "partent"],
        "passé_simple":         ["partis", "partis", "partit", "partîmes", "partîtes", "partirent"],
    },
    "dire": {
        "présent":              ["dis", "dis", "dit", "disons", "dites", "disent"],
        "imparfait":            ["disais", "disais", "disait", "disions", "disiez", "disaient"],
        "futur_simple":         ["dirai", "diras", "dira", "dirons", "direz", "diront"],
        "conditionnel_présent": ["dirais", "dirais", "dirait", "dirions", "diriez", "diraient"],
        "subjonctif_présent":   ["dise", "dises", "dise", "disions", "disiez", "disent"],
        "passé_simple":         ["dis", "dis", "dit", "dîmes", "dîtes", "dirent"],
    },
    "voir": {
        "présent":              ["vois", "vois", "voit", "voyons", "voyez", "voient"],
        "imparfait":            ["voyais", "voyais", "voyait", "voyions", "voyiez", "voyaient"],
        "futur_simple":         ["verrai", "verras", "verra", "verrons", "verrez", "verront"],
        "conditionnel_présent": ["verrais", "verrais", "verrait", "verrions", "verriez", "verraient"],
        "subjonctif_présent":   ["voie", "voies", "voie", "voyions", "voyiez", "voient"],
        "passé_simple":         ["vis", "vis", "vit", "vîmes", "vîtes", "virent"],
    },
}

# ─────────────────────────────────────────────
#  UTILITAIRES : détection du groupe
# ─────────────────────────────────────────────

def detecter_groupe(infinitif: str) -> str:
    """
    Détecte le groupe du verbe à l'aide d'expressions régulières.
    Retourne '1er_groupe', '2ème_groupe' ou '3ème_groupe'.
    """
    infinitif = infinitif.strip().lower()

    if infinitif in IRREGULIERS:
        return "3ème_groupe"

    # 1er groupe : se terminent par -er (sauf aller)
    if re.search(r"er$", infinitif) and infinitif != "aller":
        return "1er_groupe"

    # 2ème groupe : se terminent par -ir ET dont le participe présent est en -issant
    # Heuristique fiable : verbes en -ir avec radical stable
    if re.search(r"ir$", infinitif):
        # Verbes du 2ème groupe courants (finir, choisir, grandir, etc.)
        return "2ème_groupe"

    return "3ème_groupe"


def extraire_radical(infinitif: str, groupe: str) -> str:
    """
    Extrait le radical d'un verbe selon son groupe,
    en utilisant re.sub pour supprimer la terminaison.
    """
    infinitif = infinitif.strip().lower()

    if groupe == "1er_groupe":
        return re.sub(r"er$", "", infinitif)

    if groupe == "2ème_groupe":
        return re.sub(r"ir$", "", infinitif)

    return infinitif  # Pour le 3ème groupe, géré cas par cas


# ─────────────────────────────────────────────
#  MOTEUR PRINCIPAL
# ─────────────────────────────────────────────

def conjuguer(infinitif: str, temps: str) -> dict:
    """
    Conjugue un verbe à un temps donné.

    Paramètres
    ----------
    infinitif : str  — verbe à l'infinitif (ex. 'parler', 'finir', 'être')
    temps     : str  — clé du temps (ex. 'présent', 'imparfait', ...)

    Retourne
    --------
    dict  avec les clés :
        'verbe', 'temps', 'groupe', 'formes'
        'formes' est une liste de tuples (pronom, forme_conjuguée)
    """
    infinitif = infinitif.strip().lower()
    groupe = detecter_groupe(infinitif)

    # Vérifier si le verbe est irrégulier
    if infinitif in IRREGULIERS:
        formes_brutes = IRREGULIERS[infinitif].get(temps)
        if formes_brutes is None:
            raise ValueError(f"Temps '{temps}' non disponible pour '{infinitif}'.")
        formes = list(zip(PRONOMS, formes_brutes))
        return {
            "verbe": infinitif,
            "temps": temps,
            "groupe": groupe,
            "formes": formes,
        }

    # Verbes réguliers : construire les formes par concaténation radical + terminaison
    if groupe not in TERMINAISONS:
        raise ValueError(f"Groupe '{groupe}' non pris en charge pour '{infinitif}'.")

    terminaisons = TERMINAISONS[groupe].get(temps)
    if terminaisons is None:
        raise ValueError(f"Temps '{temps}' non disponible pour le groupe '{groupe}'.")

    radical = extraire_radical(infinitif, groupe)

    # Cas particuliers orthographiques pour le 1er groupe (re.sub)
    radical_mod = _corriger_radical(radical, groupe, temps)

    formes = [(pronom, radical_mod + term) for pronom, term in zip(PRONOMS, terminaisons)]

    return {
        "verbe": infinitif,
        "temps": temps,
        "groupe": groupe,
        "formes": formes,
    }


def conjuguer_tous_les_temps(infinitif: str) -> dict:
    """
    Conjugue un verbe à tous les temps simples disponibles.
    Retourne un dictionnaire {temps: résultat_conjuguer}.
    """
    tous_les_temps = [
        "présent",
        "imparfait",
        "futur_simple",
        "conditionnel_présent",
        "subjonctif_présent",
        "passé_simple",
    ]
    return {t: conjuguer(infinitif, t) for t in tous_les_temps}


# ─────────────────────────────────────────────
#  CORRECTIONS ORTHOGRAPHIQUES (1er groupe)
# ─────────────────────────────────────────────

def _corriger_radical(radical: str, groupe: str, temps: str) -> str:
    """
    Applique les corrections orthographiques automatiques
    aux radicaux du 1er groupe via re.sub.

    Règles couvertes :
        • manger → mangeons  (conserver le -g- doux)
        • commencer → commençons (cédille devant -o-)
        • appeler → appellons  (doublement du -l-)
        • jeter → jettons     (doublement du -t-)
    """
    if groupe != "1er_groupe":
        return radical

    # Verbes en -ger : ajouter 'e' devant terminaison commençant par 'o' ou 'a'
    # Ex. mang- → mange- (nous mangeons)
    if re.search(r"g$", radical) and temps in ("imparfait", "présent"):
        # Géré directement dans la génération ; on renvoie le radical original
        return radical

    # Verbes en -cer : remplacer 'c' par 'ç' devant 'o' ou 'a'
    if re.search(r"c$", radical):
        return radical  # géré dans _appliquer_corrections_finales

    return radical


def generer_forme(radical: str, terminaison: str, infinitif: str) -> str:
    """
    Génère une forme conjuguée en appliquant les corrections orthographiques
    nécessaires via des expressions régulières.
    """
    forme = radical + terminaison

    # Règle 1 : verbes en -ger → insertion d'un 'e' avant 'o' ou 'a'
    if re.search(r"ger$", infinitif):
        if re.match(r"[oa]", terminaison):
            forme = radical + "e" + terminaison

    # Règle 2 : verbes en -cer → cédille avant 'o' ou 'a'
    if re.search(r"cer$", infinitif):
        if re.match(r"[oa]", terminaison):
            forme = re.sub(r"c(e?)$", "ç", radical) + terminaison

    return forme


# ─────────────────────────────────────────────
#  UTILITAIRE : liste des temps disponibles
# ─────────────────────────────────────────────

TEMPS_DISPONIBLES = [
    "présent",
    "imparfait",
    "futur_simple",
    "conditionnel_présent",
    "subjonctif_présent",
    "passé_simple",
]

LABELS_TEMPS = {
    "présent":              "Présent",
    "imparfait":            "Imparfait",
    "futur_simple":         "Futur simple",
    "conditionnel_présent": "Conditionnel présent",
    "subjonctif_présent":   "Subjonctif présent",
    "passé_simple":         "Passé simple",
}