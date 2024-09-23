import tkinter as tk
from tkinter import simpledialog
from tkinter import Toplevel
from Library.BataillonList import bataillon_list

class DivisionEditor(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Division Designer")
        self.geometry("600x400")

        # Nom initial de la division
        self.division_name = "Division Name"

        # Structure du tableau avec "Support Company" et "Regiments" comme en-têtes de colonnes
        self.grid_structure = [
            ["Company", "Battalion", "Battalion", "Battalion", "Battalion", "Battalion"],
            ["Company", "Battalion", "Battalion", "Battalion", "Battalion", "Battalion"],
            ["Company", "Battalion", "Battalion", "Battalion", "Battalion", "Battalion"],
            ["Company", "Battalion", "Battalion", "Battalion", "Battalion", "Battalion"],
            ["Company", "Battalion", "Battalion", "Battalion", "Battalion", "Battalion"],
            ["Company", "Battalion", "Battalion", "Battalion", "Battalion", "Battalion"],
        ]

        self.create_grid()

    def create_grid(self):
        # Créer un cadre pour contenir le tableau
        grid_frame = tk.Frame(self)
        grid_frame.pack(padx=10, pady=10)

        # Titre de la division (bouton pour pouvoir le modifier)
        title_btn = tk.Button(grid_frame, text=self.division_name, command=self.change_division_name)
        title_btn.grid(row=0, column=0, columnspan=6, pady=10, sticky="nsew")  # S'étend sur toutes les colonnes

        # Ajout des en-têtes de colonne
        headers = ["Support Company", "Regiment", "Regiment", "Regiment", "Regiment", "Regiment"]
        for col_idx, header in enumerate(headers):
            header_label = tk.Label(grid_frame, text=header, font=("Arial", 10, "bold"))
            header_label.grid(row=1, column=col_idx, padx=5, pady=5)

        # Ajout des boutons de la grille en dessous des en-têtes
        for row_idx, row in enumerate(self.grid_structure):
            for col_idx, element in enumerate(row):
                btn = tk.Button(grid_frame, text=element, command=lambda r=row_idx, c=col_idx: self.add_unit(r, c))
                btn.grid(row=row_idx + 2, column=col_idx, padx=5, pady=5, sticky="nsew")  # Décalage pour les en-têtes

                # Configuration des poids de la grille pour un affichage flexible
                grid_frame.grid_rowconfigure(row_idx + 2, weight=1)
                grid_frame.grid_columnconfigure(col_idx, weight=1)

    def add_unit(self, row, col):
        # Si c'est un emplacement pour bataillon, ouvre une fenêtre de sélection
        if self.grid_structure[row][col] == "Battalion":
            self.open_battalion_selector(row, col)
        else:
            unit_type = simpledialog.askstring("Add Unit", "Choose unit type (e.g., Infantry, Artillery, etc.):")
            if unit_type:
                self.grid_structure[row][col] = unit_type
                self.update_buttons()

    def open_battalion_selector(self, row, col):
        # Créer une nouvelle fenêtre pour la sélection des bataillons
        selector_window = Toplevel(self)
        selector_window.title("Select a Battalion")

        # Ajouter un bouton pour chaque bataillon disponible
        for battalion in bataillon_list:
            btn = tk.Button(selector_window, text=battalion.Name,
                            command=lambda b=battalion: self.select_battalion(row, col, b, selector_window))
            btn.pack(pady=5, padx=10)

    def select_battalion(self, row, col, battalion, selector_window):
        # Mettre à jour la structure avec le nom du bataillon sélectionné
        self.grid_structure[row][col] = battalion.Name
        # Fermer la fenêtre de sélection
        selector_window.destroy()
        # Mettre à jour les boutons
        self.update_buttons()

    def update_buttons(self):
        # Mise à jour de la grille avec le texte des unités mis à jour
        for widget in self.winfo_children():
            widget.destroy()

        self.create_grid()

    def change_division_name(self):
        # Changer le nom de la division via une boîte de dialogue
        new_name = simpledialog.askstring("Change Division Name", "Enter new division name:")
        if new_name:
            self.division_name = new_name
            self.update_buttons()


if __name__ == "__main__":
    app = DivisionEditor()
    app.mainloop()
