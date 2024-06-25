import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
import tkinter.colorchooser as cc
from tkinter import StringVar, IntVar, BooleanVar

from typing import TYPE_CHECKING
from PIL import Image, ImageDraw, ImageTk, ImageFont

from classes.tournament import Tournament

if TYPE_CHECKING:
    from main import App


class TournamentProperties(tk.Toplevel):
    """Fenêtre permettant d'ajouter une compétition à l'application.

    :param parent: Application à laquelle ajouter la compétition.
    :type parent: App
    :param tournament_heading: Titre de la compétition.
    :type tournament_heading: StringVar
    :param tournament_weapon: Arme de la compétition.
    :type tournament_weapon: StringVar
    :param tournament_gender: Sexe des tireurs de la compétition.
    :type tournament_gender: StringVar
    :param tournament_category: Catégorie de la compétition.
    :type tournament_category: StringVar
    :param tournament_score: Score maximum de la compétition.
    :type tournament_score: IntVar
    :param tournament_kind: Type de compétition : `Individuelle` ou `Équipe`.
    :type tournament_kind: StringVar
    :param tournament_licence: Exigence des licences des tireurs de la compétition.
    :type tournament_licence: BooleanVar
    :param tournament_draw: Autorisation des assauts nuls dans la compétition.
    :type tournament_draw: BooleanVar
    :param color_background: Couleur du titre de la compétition (fond).
    :type color_background: str
    :param color_foreground: Couleur du titre de la compétition (police).
    :type color_foreground: str
    """

    def __init__(self, parent: App) -> None:
        """Initialise une nouvelle fenêtre.

        :param parent: Application à laquelle ajouter la compétition.
        """
        # Application
        super().__init__(parent)
        self.parent = parent

        # Compétition
        self.tournament_heading = StringVar(value=None)
        self.tournament_weapon = StringVar()
        self.tournament_gender = StringVar()
        self.tournament_category = StringVar()
        self.tournament_score = IntVar(value=1)
        self.tournament_kind = StringVar(value="Individuelle")
        self.tournament_licence = BooleanVar(value=False)
        self.tournament_draw = BooleanVar(value=False)

        # Couleurs
        self.color_background = "#008000"
        self.color_foreground = "#FFFFFF"

        # Fenêtre
        self.title("Nouveau tournoi")
        self.iconbitmap(r"assets\images\ico\LeFunnyIcon.ico")
        self.geometry("600x600+70+70")
        self.resizable(False, False)

        # Widgets
        self.__create_header()
        self.__create_properties()
        self.__create_validation()

    def __create_header(self) -> None:
        """Une procédure pour créer les widgets permettant d'afficher et de sélectionner la couleur du titre de la
        compétition.
        """
        # Titre
        label = ttk.Label(self,
                          text="Nouveau tournoi",
                          anchor=tk.CENTER,
                          font="Arial 24",
                          background=self.color_background,
                          foreground=self.color_foreground)
        button = tk.Button(self,
                           bg=self.color_background,
                           fg=self.color_foreground)

        def change_color() -> None:
            """Une commande pour sélectionner une couleur.
            """
            colors = cc.askcolor()
            if colors[1]:
                self.color_background = colors[1]
                label.config(background=self.color_background)
                button.config(bg=self.color_background)
            if colors[0]:
                linear_color = []
                for c in colors[0]:
                    c_lin = c / 255
                    if c_lin <= 0.04045:
                        linear_color.append(c_lin / 12.92)
                    else:
                        linear_color.append(((c_lin + 0.055) / 1.055) ** 2.4)
                lightness = 0.2126 * linear_color[0] + 0.7152 * linear_color[1] + 0.0722 * linear_color[2]
                if lightness > 0.179:
                    self.color_foreground = "#000000"
                else:
                    self.color_foreground = "#FFFFFF"
                label.config(foreground=self.color_foreground)
                button.config(fg=self.color_foreground)

        # Bouton
        button.config(command=change_color)

        # Positionnements
        label.place(relx=0.03, rely=0.03, relwidth=0.8, relheight=0.1)
        button.place(anchor=tk.NE, relx=0.97, rely=0.03, relwidth=0.1, relheight=0.1)

    def __create_properties(self) -> None:
        """Une procédure pour créer les widgets permettant de définir les caractéristiques de la compétition.
        """
        # Style
        self.option_add("*Font", "Arial 16")
        ttk.Style().configure("TRadiobutton", font="Arial 16")
        ttk.Style().configure("TCheckbutton", font="Arial 16")

        # Titre
        heading_label = ttk.Label(self, text="Titre")
        heading_textbox = ttk.Entry(self,
                                    textvariable=self.tournament_heading,
                                    width=18)

        # Arme
        weapon_label = ttk.Label(self, text="Arme")
        weapon_combobox = ttk.Combobox(self,
                                       textvariable=self.tournament_weapon,
                                       values=("Fleuret", "Épée", "Sabre", "Laser", "Multi"),
                                       state="readonly",
                                       width=16)
        weapon_combobox.current(0)

        # Sexe
        gender_label = ttk.Label(self, text="Sexe")
        gender_combobox = ttk.Combobox(self,
                                       textvariable=self.tournament_gender,
                                       values=("Hommes", "Dames", "Mixte"),
                                       state="readonly",
                                       width=16)
        gender_combobox.current(0)

        # Catégorie
        category_label = ttk.Label(self, text="Catégorie")
        category_combobox = ttk.Combobox(self,
                                         textvariable=self.tournament_category,
                                         values=("M5", "M7", "M9", "M11", "M13", "M15", "M17", "M20", "M23", "Senior",
                                                 "Vétéran", "Vétéran 1", "Vétéran 2", "Vétéran 3", "Vétéran 4",
                                                 "Vétéran 5", "Vétéran 3 + 4", "Vétéran 4 + 5"),
                                         width=16)
        category_combobox.current(0)

        def validator(arg: str) -> bool:
            """Une fonction pour vérifier les caractères du score maximum de la compétition : numérique.

            :param arg: Le score maximum de la compétition.
            :return: `True` si les caractères sont vérifiés, sinon `False`.
            """
            return (arg.isnumeric() and 1 <= int(arg) <= 999) or arg == ""

        # Score maximum
        score_label = ttk.Label(self, text="Score victorieux")
        score_spinbox = ttk.Spinbox(self,
                                    textvariable=self.tournament_score,
                                    from_=1,
                                    to=999,
                                    validate="key",
                                    validatecommand=(self.register(validator), "%P"),
                                    width=15)

        # Type : Individuelle/Équipe
        individual_radiobutton = ttk.Radiobutton(self,
                                                 variable=self.tournament_kind,
                                                 text="Individuelle",
                                                 value="Individuelle")
        team_radiobutton = ttk.Radiobutton(self,
                                           variable=self.tournament_kind,
                                           text="Équipe",
                                           value="Équipe")

        # Licence
        licence_checkbox = ttk.Checkbutton(self,
                                           text="Compétition licenciée",
                                           variable=self.tournament_licence)

        # Assauts nuls
        draw_checkbox = ttk.Checkbutton(self,
                                        text="Assauts nuls",
                                        variable=self.tournament_draw)

        # Positionnements
        heading_label.place(anchor=tk.NE, relx=0.31, rely=0.23)
        heading_textbox.place(relx=0.33, rely=0.23)
        weapon_label.place(anchor=tk.NE, relx=0.31, rely=0.32)
        weapon_combobox.place(relx=0.33, rely=0.32)
        gender_label.place(anchor=tk.NE, relx=0.31, rely=0.41)
        gender_combobox.place(relx=0.33, rely=0.41)
        category_label.place(anchor=tk.NE, relx=0.31, rely=0.5)
        category_combobox.place(relx=0.33, rely=0.5)
        score_label.place(anchor=tk.NE, relx=0.31, rely=0.59)
        score_spinbox.place(relx=0.33, rely=0.59)
        individual_radiobutton.place(relx=0.16, rely=0.70)
        team_radiobutton.place(relx=0.16, rely=0.76)
        licence_checkbox.place(relx=0.53, rely=0.70)
        draw_checkbox.place(relx=0.53, rely=0.76)

    def __create_validation(self) -> None:
        """Une procédure pour créer le bouton permettant d'ajouter la compétition et fermer la fenêtre.
        """
        # Style
        ttk.Style().configure("TButton", font="Arial 16")

        # Bouton
        button = ttk.Button(self, command=self.add_tournament, text="OK")

        # Positionnement
        button.place(anchor=tk.SE, relx=0.96, rely=0.96, relwidth=0.14, relheight=0.11)

    def add_tournament(self) -> None:  # resolve some `#`
        """Une commande pour ajouter la compétition à l'application.
        """
        # Compétition
        tournament = {"heading": self.tournament_heading.get().strip(),
                      "weapon": self.tournament_weapon.get(),
                      "gender": self.tournament_gender.get(),
                      "category": self.tournament_category.get().strip(),
                      "kind": self.tournament_kind.get(),
                      "score": None,
                      "licence": self.tournament_licence.get(),
                      "draw": self.tournament_draw.get()}

        # Vérifications
        if tournament["category"] == "":
            mb.showerror(title="Erreur Saisie",
                         message="Veuillez renseigner la catégorie de la compétition.",
                         parent=self)
        else:
            try:
                tournament["score"] = self.tournament_score.get()
            except tk.TclError:
                mb.showerror(title="Erreur Saisie",
                             message="Veuillez renseigner le score maximum de la compétition.",
                             parent=self)
            else:
                if tournament["heading"] == "":
                    tournament["heading"] = f"{tournament['weapon']}{tournament['gender']}{tournament['category']}"

                # ...
                if not self.parent.is_notebook:  # if not self.parent.has_tournaments
                    self.parent.background_notebook = ttk.Notebook(self.parent)

                    self.parent.background_image.pack_forget()
                    self.parent.background_notebook.pack(fill="both", expand=True)

                    self.parent.is_notebook = True

                frame = Tournament(self.parent.background_notebook,
                                        len(self.parent.notebook_frames),
                                        self.color_background,
                                        self.color_foreground,
                                        **tournament)

                im = Image.new("RGB", (180, 40), self.color_background)
                im_draw = ImageDraw.Draw(im)
                im_draw.text((90, 20),
                             tournament["heading"],
                             fill=self.color_foreground,
                             anchor="mm",
                             font=ImageFont.truetype("arial", 20))
                frame.img = ImageTk.PhotoImage(im)

                self.parent.background_notebook.add(frame, image=frame.img)

                self.parent.notebook_frames.append(frame)
                self.destroy()
