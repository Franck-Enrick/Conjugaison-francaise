"""
Application de conjugaison automatique des verbes français.
Interface graphique réalisée avec la bibliothèque TKinter.
"""

import tkinter as tk
from tkinter import ttk, messagebox, font
from conjugation_engine import (
    conjuguer,
    conjuguer_tous_les_temps,
    detecter_groupe,
    TEMPS_DISPONIBLES,
    LABELS_TEMPS,
    IRREGULIERS,
)

# ─────────────────────────────────────────────
#  PALETTE DE COULEURS
# ─────────────────────────────────────────────

COULEURS = {
    "bg_principal":   "#1e1e2e",
    "bg_panneau":     "#2a2a3e",
    "bg_entree":      "#313148",
    "accent":         "#7c6af7",
    "accent_hover":   "#9b8dff",
    "texte":          "#e0e0f0",
    "texte_doux":     "#a0a0c0",
    "succes":         "#50fa7b",
    "erreur":         "#ff5555",
    "bordure":        "#44446a",
    "pronom":         "#7c6af7",
    "forme":          "#e0e0f0",
    "titre_temps":    "#bd93f9",
}

# Verbes suggérés pour la barre de recherche rapide
VERBES_EXEMPLES = [
    "parler", "manger", "commencer", "finir", "choisir",
    "être", "avoir", "aller", "faire", "pouvoir",
    "vouloir", "savoir", "venir", "prendre", "mettre",
    "partir", "dire", "voir",
]


class AppConjugaison(tk.Tk):
    """Fenêtre principale de l'application."""

    def __init__(self):
        super().__init__()

        self.title("Conjugaison Française — Temps Simples")
        self.geometry("920x680")
        self.minsize(750, 550)
        self.configure(bg=COULEURS["bg_principal"])

        # Variables Tkinter
        self.var_verbe = tk.StringVar()
        self.var_temps = tk.StringVar(value="présent")
        self.var_tous  = tk.BooleanVar(value=False)

        self._construire_ui()
        self._bind_raccourcis()

    # ── Construction de l'interface ──────────────────────────────────────────

    def _construire_ui(self):
        self._construire_entete()
        self._construire_panneau_gauche()
        self._construire_panneau_droit()

    def _construire_entete(self):
        entete = tk.Frame(self, bg=COULEURS["bg_principal"], pady=18)
        entete.pack(fill="x", padx=30)

        tk.Label(
            entete,
            text="🇫🇷  Conjugueur Français",
            font=("Helvetica", 22, "bold"),
            fg=COULEURS["accent"],
            bg=COULEURS["bg_principal"],
        ).pack(side="left")

        tk.Label(
            entete,
            text="Temps simples — 1er, 2ème & 3ème groupes",
            font=("Helvetica", 11),
            fg=COULEURS["texte_doux"],
            bg=COULEURS["bg_principal"],
        ).pack(side="left", padx=16, pady=6)

    def _construire_panneau_gauche(self):
        """Panneau de saisie et de configuration."""
        conteneur = tk.Frame(self, bg=COULEURS["bg_principal"])
        conteneur.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        gauche = tk.Frame(conteneur, bg=COULEURS["bg_panneau"],
                          relief="flat", bd=0, padx=20, pady=20)
        gauche.pack(side="left", fill="y", padx=(0, 10), ipadx=4)

        # ── Champ de saisie du verbe ──
        tk.Label(gauche, text="Verbe à conjuguer",
                 font=("Helvetica", 11, "bold"),
                 fg=COULEURS["texte"], bg=COULEURS["bg_panneau"]).pack(anchor="w")

        cadre_entree = tk.Frame(gauche, bg=COULEURS["bg_entree"],
                                highlightbackground=COULEURS["accent"],
                                highlightthickness=2)
        cadre_entree.pack(fill="x", pady=(6, 0))

        self.champ_verbe = tk.Entry(
            cadre_entree,
            textvariable=self.var_verbe,
            font=("Helvetica", 14),
            bg=COULEURS["bg_entree"],
            fg=COULEURS["texte"],
            insertbackground=COULEURS["accent"],
            relief="flat",
            bd=8,
            width=22,
        )
        self.champ_verbe.pack(fill="x")
        self.champ_verbe.bind("<Return>", lambda e: self._conjuguer())
        self.champ_verbe.bind("<KeyRelease>", self._mise_a_jour_autocomplete)

        # ── Exemples cliquables ──
        tk.Label(gauche, text="Exemples rapides",
                 font=("Helvetica", 9),
                 fg=COULEURS["texte_doux"], bg=COULEURS["bg_panneau"]
                 ).pack(anchor="w", pady=(14, 4))

        cadre_exemples = tk.Frame(gauche, bg=COULEURS["bg_panneau"])
        cadre_exemples.pack(fill="x")

        for i, verbe in enumerate(VERBES_EXEMPLES):
            btn = tk.Button(
                cadre_exemples,
                text=verbe,
                font=("Helvetica", 9),
                fg=COULEURS["accent"],
                bg=COULEURS["bg_entree"],
                activeforeground=COULEURS["accent_hover"],
                activebackground=COULEURS["bg_panneau"],
                relief="flat", bd=0, padx=6, pady=3, cursor="hand2",
                command=lambda v=verbe: self._choisir_exemple(v),
            )
            btn.grid(row=i // 3, column=i % 3, padx=3, pady=2, sticky="w")

        # ── Sélection du temps ──
        tk.Label(gauche, text="Temps verbal",
                 font=("Helvetica", 11, "bold"),
                 fg=COULEURS["texte"], bg=COULEURS["bg_panneau"]
                 ).pack(anchor="w", pady=(18, 6))

        self.var_tous.trace_add("write", self._toggle_temps)
        for temps in TEMPS_DISPONIBLES:
            rb = tk.Radiobutton(
                gauche,
                text=LABELS_TEMPS[temps],
                variable=self.var_temps,
                value=temps,
                font=("Helvetica", 10),
                fg=COULEURS["texte"],
                bg=COULEURS["bg_panneau"],
                selectcolor=COULEURS["accent"],
                activeforeground=COULEURS["accent"],
                activebackground=COULEURS["bg_panneau"],
                relief="flat",
            )
            rb.pack(anchor="w", pady=1)
            setattr(self, f"rb_{temps}", rb)

        # ── Case "Tous les temps" ──
        tk.Checkbutton(
            gauche,
            text="Tous les temps",
            variable=self.var_tous,
            font=("Helvetica", 10, "bold"),
            fg=COULEURS["succes"],
            bg=COULEURS["bg_panneau"],
            selectcolor=COULEURS["bg_entree"],
            activeforeground=COULEURS["succes"],
            activebackground=COULEURS["bg_panneau"],
        ).pack(anchor="w", pady=(10, 16))

        # ── Bouton conjuguer ──
        self.btn_conjuguer = tk.Button(
            gauche,
            text="  Conjuguer  →",
            font=("Helvetica", 12, "bold"),
            fg="#ffffff",
            bg=COULEURS["accent"],
            activeforeground="#ffffff",
            activebackground=COULEURS["accent_hover"],
            relief="flat", bd=0, padx=14, pady=10, cursor="hand2",
            command=self._conjuguer,
        )
        self.btn_conjuguer.pack(fill="x")

        # ── Bouton effacer ──
        tk.Button(
            gauche,
            text="Effacer",
            font=("Helvetica", 10),
            fg=COULEURS["texte_doux"],
            bg=COULEURS["bg_entree"],
            relief="flat", bd=0, padx=8, pady=6, cursor="hand2",
            command=self._effacer,
        ).pack(fill="x", pady=(6, 0))

        # ── Étiquette groupe ──
        self.label_groupe = tk.Label(
            gauche, text="",
            font=("Helvetica", 9, "italic"),
            fg=COULEURS["texte_doux"], bg=COULEURS["bg_panneau"],
        )
        self.label_groupe.pack(anchor="w", pady=(12, 0))

        # Stocker référence pour la zone droite
        self._conteneur_principal = conteneur

    def _construire_panneau_droit(self):
        """Zone d'affichage des résultats avec scrollbar."""
        droit = tk.Frame(
            self._conteneur_principal,
            bg=COULEURS["bg_panneau"],
        )
        droit.pack(side="left", fill="both", expand=True)

        # Canvas + scrollbar pour gérer le défilement
        self.canvas = tk.Canvas(droit, bg=COULEURS["bg_panneau"],
                                highlightthickness=0)
        scrollbar = ttk.Scrollbar(droit, orient="vertical",
                                  command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.zone_resultats = tk.Frame(self.canvas, bg=COULEURS["bg_panneau"])
        self._fenetre_canvas = self.canvas.create_window(
            (0, 0), window=self.zone_resultats, anchor="nw"
        )

        self.zone_resultats.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Message d'accueil
        tk.Label(
            self.zone_resultats,
            text="Saisissez un verbe et cliquez sur\n« Conjuguer » pour voir les formes.",
            font=("Helvetica", 13),
            fg=COULEURS["texte_doux"],
            bg=COULEURS["bg_panneau"],
            justify="center",
        ).pack(expand=True, pady=80)

    # ── Logique de conjugaison ──────────────────────────────────────────────

    def _conjuguer(self):
        verbe = self.var_verbe.get().strip().lower()
        if not verbe:
            messagebox.showwarning("Verbe manquant", "Veuillez entrer un verbe.")
            return

        self._vider_resultats()

        try:
            groupe = detecter_groupe(verbe)
            self.label_groupe.config(
                text=f"Groupe détecté : {groupe}",
                fg=COULEURS["succes"],
            )

            if self.var_tous.get():
                resultats = conjuguer_tous_les_temps(verbe)
                for temps, res in resultats.items():
                    self._afficher_tableau(res)
            else:
                temps = self.var_temps.get()
                res = conjuguer(verbe, temps)
                self._afficher_tableau(res)

        except ValueError as e:
            self.label_groupe.config(text="", fg=COULEURS["texte_doux"])
            tk.Label(
                self.zone_resultats,
                text=f"⚠  {e}",
                font=("Helvetica", 11),
                fg=COULEURS["erreur"],
                bg=COULEURS["bg_panneau"],
                wraplength=400,
            ).pack(pady=30)

    def _afficher_tableau(self, resultat: dict):
        """Affiche un bloc de conjugaison pour un temps donné."""
        verbe  = resultat["verbe"]
        temps  = resultat["temps"]
        formes = resultat["formes"]

        # ── En-tête du bloc ──
        cadre_titre = tk.Frame(self.zone_resultats, bg=COULEURS["bg_principal"],
                               pady=6, padx=14)
        cadre_titre.pack(fill="x", pady=(12, 0), padx=14)

        tk.Label(
            cadre_titre,
            text=f"{verbe.capitalize()}  —  {LABELS_TEMPS[temps]}",
            font=("Helvetica", 13, "bold"),
            fg=COULEURS["titre_temps"],
            bg=COULEURS["bg_principal"],
        ).pack(side="left")

        # ── Grille des formes ──
        cadre_formes = tk.Frame(self.zone_resultats, bg=COULEURS["bg_panneau"],
                                padx=20, pady=10)
        cadre_formes.pack(fill="x", padx=14, pady=(0, 4))

        for i, (pronom, forme) in enumerate(formes):
            row = i % 3
            col_p = (i // 3) * 2
            col_f = col_p + 1

            tk.Label(
                cadre_formes,
                text=pronom,
                font=("Helvetica", 11, "bold"),
                fg=COULEURS["pronom"],
                bg=COULEURS["bg_panneau"],
                width=12,
                anchor="e",
            ).grid(row=row, column=col_p, sticky="e", padx=(8, 4), pady=5)

            tk.Label(
                cadre_formes,
                text=forme,
                font=("Helvetica", 11),
                fg=COULEURS["forme"],
                bg=COULEURS["bg_panneau"],
                width=16,
                anchor="w",
            ).grid(row=row, column=col_f, sticky="w", padx=(0, 20), pady=5)

        # Séparateur
        sep = tk.Frame(self.zone_resultats, bg=COULEURS["bordure"], height=1)
        sep.pack(fill="x", padx=14, pady=4)

    # ── Utilitaires UI ──────────────────────────────────────────────────────

    def _vider_resultats(self):
        for widget in self.zone_resultats.winfo_children():
            widget.destroy()

    def _effacer(self):
        self.var_verbe.set("")
        self.label_groupe.config(text="")
        self._vider_resultats()
        self.champ_verbe.focus_set()

    def _choisir_exemple(self, verbe: str):
        self.var_verbe.set(verbe)
        self._conjuguer()

    def _toggle_temps(self, *args):
        state = "disabled" if self.var_tous.get() else "normal"
        for temps in TEMPS_DISPONIBLES:
            rb = getattr(self, f"rb_{temps}", None)
            if rb:
                rb.config(state=state)

    def _mise_a_jour_autocomplete(self, event):
        """Met à jour le label groupe en temps réel pendant la frappe."""
        verbe = self.var_verbe.get().strip().lower()
        if len(verbe) >= 3:
            try:
                groupe = detecter_groupe(verbe)
                self.label_groupe.config(
                    text=f"Groupe probable : {groupe}",
                    fg=COULEURS["texte_doux"],
                )
            except Exception:
                self.label_groupe.config(text="")
        else:
            self.label_groupe.config(text="")

    def _bind_raccourcis(self):
        self.bind("<Control-Return>", lambda e: self._conjuguer())
        self.bind("<Escape>", lambda e: self._effacer())
        self.champ_verbe.focus_set()

    # ── Gestion du scroll ──────────────────────────────────────────────────

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self._fenetre_canvas, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


# ─────────────────────────────────────────────
#  POINT D'ENTRÉE
# ─────────────────────────────────────────────

if __name__ == "__main__":
    app = AppConjugaison()
    app.mainloop()
