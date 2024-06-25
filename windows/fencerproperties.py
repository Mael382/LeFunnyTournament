import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb

from tkinter import StringVar
from classes.fencer import IndividualFencer, TeamFencer

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classes.tournament import Tournament


class FencerProperties(tk.Toplevel):
    """Fenêtre permettant d'ajouter un tireur à une compétition.

    :param parent: Compétition du tireur.
    :type parent: Tournament
    :param lastname: Nom du tireur.
    :type lastname: StringVar
    :param firstname: Prénom du tireur.
    :type firstname: StringVar
    :param team: Nom de l'équipe du tireur.
    :type team: StringVar
    :param age: Âge du tireur.
    :type age: StringVar
    :param gender: Sexe du tireur.
    :type gender: StringVar
    :param club: Nom du club du tireur.
    :type club: StringVar
    :param licence: Licence du tireur.
    :type licence: StringVar
    """

    def __init__(self, parent: Tournament):
        """Initialise une nouvelle fenêtre.

        :param parent: Compétition du tireur.
        """
        # Compétition
        super().__init__(parent)
        self.parent = parent

        # Tireur
        self.lastname = StringVar(value=None)
        self.firstname = StringVar(value=None)
        self.team = StringVar(value=None)
        self.age = StringVar(value=None)
        self.gender = StringVar(value=None)
        self.club = StringVar(value=None)
        self.licence = StringVar(value=None)

        # Fenêtre
        self.title("Nouveau tireur")
        self.iconbitmap(r"assets\images\ico\LeFunnyIcon.ico")
        self.geometry("600x600+70+70")
        self.resizable(False, False)

        # Widgets
        self.__create_properties()
        self.__create_adder()
        self.__create_closer()

    def __create_properties(self) -> None:
        """Crée les widgets permettant de définir les caractéristiques du tireur.
        """
        # Style
        self.option_add("*Font", "Arial 16")

        def name_upper(*args: str) -> None:
            """Convertit la casse du nom du tireur en majuscule.
            """
            self.lastname.set(self.lastname.get().upper())

        def names_validator(arg: str) -> bool:
            """Vérifie les caractères du nom ou prénom du tireur : alphabétique, espace, apostrophe ou tiret.

            :param arg: Le nom ou prénom du tireur.
            :return: `True` si les caractères sont vérifiés, sinon `False`.
            """
            return arg == "" or all((i.isalpha() or i == " " or i == "'" or i == "-") for i in arg)

        # Nom
        self.lastname.trace_add("write", name_upper)
        name_label = ttk.Label(self, text="Nom")
        name_textbox = ttk.Entry(self,
                                 textvariable=self.lastname,
                                 validate="key",
                                 validatecommand=(self.register(names_validator), "%P"),
                                 width=24)

        def firstname_title(*args: str):
            """Convertit la casse du prénom du tireur en majuscule pour la première lettre de chaque mot et en minuscule
            pour le reste.
            """
            self.firstname.set(self.firstname.get().title())

        # Prénom
        self.firstname.trace_add("write", firstname_title)
        firstname_label = ttk.Label(self, text="Prénom")
        firstname_textbox = ttk.Entry(self,
                                      textvariable=self.firstname,
                                      validate="key",
                                      validatecommand=(self.register(names_validator), "%P"),
                                      width=24)

        # Équipe
        team_label = ttk.Label(self, text="Équipe")
        team_combobox = ttk.Combobox(self,
                                     textvariable=self.team,
                                     values=tuple(self.parent.teams),  # ORDER BY NAME
                                     width=22)

        def numbers_validator(arg: str) -> bool:
            """Vérifie les caractères de l'âge du participant : numérique.

            :param arg: L'âge du participant.
            :return: `True` si les caractères sont vérifiés, sinon `False`.
            """
            return arg == "" or arg.isnumeric()

        # Âge
        age_label = ttk.Label(self, text="Âge")
        age_textbox = ttk.Entry(self,
                                textvariable=self.age,
                                validate="key",
                                validatecommand=(self.register(numbers_validator), "%P"),
                                width=24)

        # Sexe
        gender_label = ttk.Label(self, text="Sexe")
        gender_combobox = ttk.Combobox(self,
                                       textvariable=self.gender,
                                       values=("Masculin", "Féminin"),
                                       state="readonly",
                                       width=22)
        if self.parent.gender == "Hommes":
            gender_combobox.current(0)
        elif self.parent.gender == "Dames":
            gender_combobox.current(1)

        # Club
        club_label = ttk.Label(self, text="Club")
        club_combobox = ttk.Combobox(self,
                                     textvariable=self.club,
                                     values=tuple(self.parent.clubs),  # ORDER BY NAME
                                     width=22)

        # Licence
        licence_label = ttk.Label(self, text="Licence")
        licence_textbox = ttk.Entry(self,
                                    textvariable=self.licence,
                                    validate="key",
                                    validatecommand=(self.register(numbers_validator), "%P"),
                                    width=24)

        # Positionnements
        name_label.place(anchor=tk.NE, relx=0.17, rely=0.07)
        name_textbox.place(relx=0.19, rely=0.07)
        firstname_label.place(anchor=tk.NE, relx=0.17, rely=0.14)
        firstname_textbox.place(relx=0.19, rely=0.14)
        if self.parent.kind == "Individuelle":
            age_label.place(anchor=tk.NE, relx=0.17, rely=0.21)
            age_textbox.place(relx=0.19, rely=0.21)
            gender_label.place(anchor=tk.NE, relx=0.17, rely=0.28)
            gender_combobox.place(relx=0.19, rely=0.28)
            if self.parent.licence_is_needed:
                club_label.place(anchor=tk.NE, relx=0.17, rely=0.35)
                club_combobox.place(relx=0.19, rely=0.35)
                licence_label.place(anchor=tk.NE, relx=0.17, rely=0.42)
                licence_textbox.place(relx=0.19, rely=0.42)
        elif self.parent.kind == "Équipe":
            team_label.place(anchor=tk.NE, relx=0.17, rely=0.21)
            team_combobox.place(relx=0.19, rely=0.21)
            age_label.place(anchor=tk.NE, relx=0.17, rely=0.28)
            age_textbox.place(relx=0.19, rely=0.28)
            gender_label.place(anchor=tk.NE, relx=0.17, rely=0.35)
            gender_combobox.place(relx=0.19, rely=0.35)
            if self.parent.licence_is_needed:
                club_label.place(anchor=tk.NE, relx=0.17, rely=0.42)
                club_combobox.place(relx=0.19, rely=0.42)
                licence_label.place(anchor=tk.NE, relx=0.17, rely=0.49)
                licence_textbox.place(relx=0.19, rely=0.49)

    def __create_adder(self) -> None:
        """Crée le bouton permettant d'ajouter le tireur.
        """
        # Style
        ttk.Style().configure("TButton", font="Arial 16")

        # Bouton
        button = ttk.Button(self, command=self.add_fencer, text="Ajouter")

        # Positionnement
        button.place(anchor=tk.SE, relx=0.73, rely=0.96, relwidth=0.14, relheight=0.11)

    def __create_closer(self) -> None:
        """Crée le bouton permettant de fermer la fenêtre.
        """
        # Style
        ttk.Style().configure("TButton", font="Arial 16")

        # Bouton
        button = ttk.Button(self, command=self.destroy, text="Fermer")

        # Positionnement
        button.place(anchor=tk.SE, relx=0.93, rely=0.96, relwidth=0.14, relheight=0.11)

    def add_fencer(self) -> None:
        """Commande pour ajouter le tireur à la compétition.
        """
        # Caractéristiques
        lastname = self.lastname.get().strip()
        firstname = self.firstname.get().strip()
        team = self.team.get().strip(),
        age = self.age.get().strip(),
        gender = self.gender.get(),
        club = self.club.get().strip(),
        licence = self.licence.get().strip()

        # Vérifications
        if lastname == "":
            mb.showerror(title="Erreur Saisie",
                         message="Veuillez renseigner le nom du tireur.",
                         parent=self)
        elif firstname == "":
            mb.showerror(title="Erreur Saisie",
                         message="Veuillez renseigner le prénom du tireur.",
                         parent=self)
        elif age == "" and self.parent.licence_is_needed:
            mb.showerror(title="Erreur Saisie",
                         message="Veuillez renseigner l'âge du tireur.",
                         parent=self)
        elif gender == "" and self.parent.licence_is_needed:
            mb.showerror(title="Erreur Saisie",
                         message="Veuillez renseigner le sexe du tireur.",
                         parent=self)
        elif club == "" and self.parent.licence_is_needed:
            mb.showerror(title="Erreur Saisie",
                         message="Veuillez renseigner le club du tireur.",
                         parent=self)
        elif licence == "" and self.parent.licence_is_needed:
            mb.showerror(title="Erreur Saisie",
                         message="Veuillez renseigner la licence du tireur.",
                         parent=self)
        elif team == "" and self.parent.kind == "Équipe":
            mb.showerror(title="Erreur Saisie",
                         message="Veuillez renseigner l'équipe du tireur.",
                         parent=self)
        else:

            # Tireur
            if self.parent.kind == "Individuelle":
                self.parent.add_fencer(IndividualFencer(lastname, firstname, age, gender, club, licence, self.parent))
            elif self.parent.kind == "Équipe":
                self.parent.add_fencer(TeamFencer(lastname, firstname, team, age, gender, club, licence, self.parent))

            # Réinitialisation
            self.destroy()
            self.parent.adding_fencers_window()














            # Insertion équipe
            if self.parent.tournament_kind == "Équipe":
                self.parent.table.insert("",
                                         tk.END,
                                         values=table_team,
                                         iid=f"T{self.parent.tournament_teams_added}",
                                         open=True,
                                         tags=(str(len(self.parent.tournament_fencers) % 2),))

            # Insertion tireur
            if self.parent.tournament_kind == "Équipe":
                self.parent.table.insert(f"T{team_index + 1}",
                                         tk.END,
                                         values=table_fencer,
                                         iid=f"F{self.parent.tournament_fencers_added}",
                                         tags=(str(len(self.parent.tournament_fencers) % 2),))
            elif self.parent.tournament_kind == "Individuelle":
                self.parent.table.insert("",
                                         tk.END,
                                         values=table_fencer,
                                         iid=f"F{self.parent.tournament_fencers_added}",
                                         tags=(str(len(self.parent.tournament_fencers) % 2),))