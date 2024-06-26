import tkinter as tk
import tkinter.messagebox as mb
import tkinter.colorchooser as cc
from tkinter import BooleanVar, IntVar, StringVar
from tkinter.ttk import Style, Label, Button, Radiobutton, Checkbutton, Entry, Combobox, Spinbox, Notebook
from tkinter import Button as TkButton

from random import randbytes
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageTk import PhotoImage

from competition.tournament import Tournament

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import App


def get_color_font(color_background: str | tuple[int, int, int]) -> str:
    """
    Obtient la couleur hexadécimale de police appropriée, par rapport à la couleur de fond.

    :param color_background: Couleur de fond.
    :return: Couleur de police
    """
    # RGB de fond
    colors: tuple[int, int, int]
    if isinstance(color_background, str):
        colors = (int(color_background[1:3], 16), int(color_background[3:5], 16), int(color_background[5:], 16))
    else:
        colors = color_background

    # Luminosité de fond
    lightness: float = 0
    lightness_factors: tuple[float, float, float] = (0.2126, 0.7152, 0.0722)
    for i, color in enumerate(colors):
        color /= 255
        if color <= 0.04045:
            color /= 12.92
        else:
            color = ((color + 0.055) / 1.055) ** 2.4
        lightness += lightness_factors[i] * color

    # Police
    color_font: str
    if lightness > 0.179:
        color_font = "#000000"
    else:
        color_font = "#ffffff"

    return color_font


class TournamentProperties(tk.Toplevel):
    """
    Fenêtre permettant d'ajouter une compétition à l'application.

    :param parent: Application à laquelle ajouter la compétition.
    :type parent: App
    """
    #: Application à laquelle ajouter la compétition
    _parent: "App"
    #: Nom de la compétition
    _tournament_name: StringVar
    #: Arme de la compétition
    _tournament_weapon: StringVar
    #: Sexe de la compétition
    _tournament_gender: StringVar
    #: Catégorie de la compétition
    _tournament_category: StringVar
    #: Type de compétition : `Individuelle` ou `Équipe`
    _tournament_kind: StringVar
    #: Score maximum des matchs
    _tournament_score: IntVar
    #: Exigence des licences des tireurs
    _tournament_licences: BooleanVar
    #: Autorisation des matchs nuls
    _tournament_draws: BooleanVar
    #: Couleur de fond
    _color_background: str
    #: Couleur de police
    _color_font: str

    def __init__(self, parent: "App") -> None:
        """
        Initialise une nouvelle fenêtre.
        """
        # Application
        super().__init__(parent)
        self._parent = parent

        # Compétition
        self._tournament_name = StringVar(value=None)
        self._tournament_weapon = StringVar()
        self._tournament_gender = StringVar()
        self._tournament_category = StringVar()
        self._tournament_kind = StringVar(value="Individuelle")
        self._tournament_score = IntVar(value=1)
        self._tournament_licences = BooleanVar(value=False)
        self._tournament_draws = BooleanVar(value=False)

        # Couleurs
        self._color_background = f"#{randbytes(3).hex()}"
        self._color_font = get_color_font(self._color_background)

        # Fenêtre
        self.title("Nouveau tournoi")
        self.iconbitmap(r"assets\images\ico\LeFunnyIcon.ico")
        self.geometry("600x600+70+70")
        self.resizable(False, False)

        # Widgets
        self._create_header()
        self._create_properties()
        self._create_validation()

    @property
    def parent(self):
        return self._parent

    def _create_header(self) -> None:
        """
        Créé les widgets permettant d'afficher et de sélectionner les couleurs de la compétition.
        """
        # Nom
        label: Label = Label(self, text="Nouveau tournoi",
                             anchor=tk.CENTER, font="Arial 24", background=self._color_background,
                             foreground=self._color_font)
        button: TkButton = TkButton(self, bg=self._color_background, fg=self._color_font)

        def change_color() -> None:
            """
            Commande pour sélectionner une couleur.
            """
            colors: tuple[tuple[int, int, int], str] | tuple[None, None] = cc.askcolor()
            if colors[0] and colors[1]:

                # Fond
                self._color_background = colors[1]
                label.config(background=self._color_background)
                button.config(bg=self._color_background)

                # Police
                self.color_foreground = get_color_font(colors[0])
                label.config(foreground=self._color_font)
                button.config(fg=self._color_font)

        # Bouton
        button.config(command=change_color)

        # Positionnements
        label.place(relx=0.03, rely=0.03, relwidth=0.8, relheight=0.1)
        button.place(anchor=tk.NE, relx=0.97, rely=0.03, relwidth=0.1, relheight=0.1)

    def _create_properties(self) -> None:
        """
        Créé les widgets permettant de définir les caractéristiques de la compétition.
        """
        # Style
        self.option_add("*Font", "Arial 16")
        Style().configure("TRadiobutton", font="Arial 16")
        Style().configure("TCheckbutton", font="Arial 16")

        # Nom
        name_label: Label = Label(self, text="Nom")
        name_textbox = Entry(self, textvariable=self._tournament_name,
                             width=18)

        # Arme
        weapon_label: Label = Label(self, text="Arme")
        weapon_combobox: Combobox = Combobox(self, textvariable=self._tournament_weapon,
                                             values=("Fleuret", "Épée", "Sabre", "Laser", "Multi"), state="readonly",
                                             width=16)
        weapon_combobox.current(0)

        # Sexe
        gender_label: Label = Label(self, text="Sexe")
        gender_combobox: Combobox = Combobox(self, textvariable=self._tournament_gender,
                                             values=("Hommes", "Dames", "Mixte"), state="readonly", width=16)
        gender_combobox.current(0)

        # Catégorie
        category_label: Label = Label(self, text="Catégorie")
        category_combobox: Combobox = Combobox(self, textvariable=self._tournament_category,
                                               values=("M5", "M7", "M9", "M11", "M13", "M15", "M17", "M20", "M23",
                                                       "Senior", "Vétéran", "Vétéran 1", "Vétéran 2", "Vétéran 3",
                                                       "Vétéran 4", "Vétéran 5", "Vétéran 3 + 4", "Vétéran 4 + 5"),
                                               width=16)
        category_combobox.current(0)

        def validator(arg: str) -> bool:
            """
            Vérifie les caractères du score maximum des matchs : numériques.

            :param arg: Le score maximum des matchs.
            :return: `True` si les caractères sont vérifiés, sinon `False`.
            """
            return (arg.isnumeric() and (1 <= int(arg) <= 999)) or arg == ""

        # Score maximum
        score_label: Label = Label(self, text="Score maximum")
        score_spinbox: Spinbox = Spinbox(self, textvariable=self._tournament_score,
                                         from_=1, to=999, validate="key",
                                         validatecommand=(self.register(validator), "%P"), width=15)

        # Type : Individuelle ou Équipe
        individual_radiobutton: Radiobutton = Radiobutton(self, variable=self._tournament_kind,
                                                          text="Individuelle", value="Individuelle")
        team_radiobutton: Radiobutton = Radiobutton(self, variable=self._tournament_kind,
                                                    text="Équipe", value="Équipe")

        # Licences
        licences_checkbutton: Checkbutton = Checkbutton(self, variable=self._tournament_licences,
                                                        text="Compétition licenciée")

        # Matchs nuls
        draws_checkbutton: Checkbutton = Checkbutton(self, variable=self._tournament_draws,
                                                     text="Matchs nuls")

        # Positionnements
        name_label.place(anchor=tk.NE, relx=0.31, rely=0.23)
        name_textbox.place(relx=0.33, rely=0.23)
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
        licences_checkbutton.place(relx=0.53, rely=0.70)
        draws_checkbutton.place(relx=0.53, rely=0.76)

    def _create_validation(self) -> None:
        """
        Créé le bouton permettant d'ajouter la compétition et fermer la fenêtre.
        """
        # Style
        Style().configure("TButton", font="Arial 16")

        # Bouton
        button: Button = Button(self, command=self.add_tournament,
                                text="OK")

        # Positionnement
        button.place(anchor=tk.SE, relx=0.96, rely=0.96, relwidth=0.14, relheight=0.11)

    def add_tournament(self) -> None:
        """
        Commande pour ajouter la compétition à l'application.
        """
        # Compétition
        kargs: dict[str, str | int | bool | None] = {"name": self._tournament_name.get().strip(),
                                                     "weapon": self._tournament_weapon.get(),
                                                     "gender": self._tournament_gender.get(),
                                                     "category": self._tournament_category.get().strip(),
                                                     "kind": self._tournament_kind.get(),
                                                     "maximum_score": None,
                                                     "licences_are_needed": self._tournament_licences.get(),
                                                     "draws_are_allowed": self._tournament_draws.get()}

        # Vérifications
        if kargs["category"] == "":
            mb.showerror(title="Erreur Saisie", message="Veuillez renseigner la catégorie de la compétition.",
                         parent=self)
        else:
            try:
                kargs["maximum_score"] = self._tournament_score.get()
            except tk.TclError:
                mb.showerror(title="Erreur Saisie", message="Veuillez renseigner le score maximum de la compétition.",
                             parent=self)
            else:
                if kargs["name"] == "":
                    kargs["name"] = f"{kargs['weapon']}{kargs['gender']}{kargs['category']}"

                # Compétition
                tournament: Tournament = Tournament(**kargs)

                # Étiquette
                im: Image = Image.new("RGB", (180, 40), self._color_background)
                draw: ImageDraw = ImageDraw.Draw(im)
                draw.text((90, 20), tournament.name,
                          anchor="mm", fill=self._color_font, font=ImageFont.truetype("arial", 20))
                tag: PhotoImage = PhotoImage(im)

                # Ajout
                self._parent.add_tournament(tournament, tag)
                self.destroy()
