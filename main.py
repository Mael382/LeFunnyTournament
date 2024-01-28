import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import tkinter.messagebox as mb
import tkinter.colorchooser as cc
from PIL import Image, ImageDraw, ImageTk, ImageFont


class FencerProperties(tk.Toplevel):
    """
    Fenêtre permettant d'ajouter des participants à un tournoi.

    Attributes
    ----------
    fencer_name: tkinter.StringVar
        Le nom du participant
    fencer_firstname: tkinter.StringVar
        Le prénom du participant
    fencer_team: tkinter.StringVar
        L'équipe du participant
    fencer_age: tkinter.StringVar
        L'âge du participant
    fencer_gender: tkinter.StringVar
        Le sexe du participant
    fencer_club: tkinter.StringVar
        Le club du participant
    fencer_licence: tkinter.StringVar
        La licence du participant
    """

    def __init__(self, parent):
        """
        Parameters
        ----------
        parent: TournamentFrame
        """
        super().__init__(parent)
        self.parent = parent

        # Caractéristiques des participants
        self.fencer_name = tk.StringVar(value=None)
        self.fencer_firstname = tk.StringVar(value=None)
        self.fencer_team = tk.StringVar(value=None)
        self.fencer_age = tk.StringVar(value=None)
        self.fencer_gender = tk.StringVar(value=None)
        self.fencer_club = tk.StringVar(value=None)
        self.fencer_licence = tk.StringVar(value=None)

        # Caractéristiques de la fenêtre
        self.title("Nouveau participant")
        self.iconbitmap(r"images\LeFunnyIcon.ico")
        self.geometry("600x600+70+70")
        self.resizable(False, False)

        # Contenu de la fenêtre
        self.__create_properties()
        self.__create_adder()
        self.__create_closer()

    def __create_properties(self):
        """
        Crée les widgets permettant de définir les caractéristiques d'un participant.
        """

        # Style des widgets
        self.option_add("*Font", "Arial 16")

        def name_upper(*args):
            """
            Convertit la casse du nom du participant en majuscule.

            Parameters
            ----------
            args: str
            """

            self.fencer_name.set(self.fencer_name.get().upper())

        def names_validator(arg):
            """
            Vérifie la nature des caractères du nom ou prénom du participant : alphabétique, espace, apostrophe ou
            tiret.

            Parameters
            ----------
            arg: str
                Le nom ou prénom du participant

            Returns
            -------
            bool
                True si la nature est vérifiée, sinon False
            """
            return arg == "" or all((i.isalpha() or i == " " or i == "'" or i == "-") for i in arg)

        # Nom du participant
        self.fencer_name.trace_add("write", name_upper)
        name_label = ttk.Label(self, text="Nom")
        name_textbox = ttk.Entry(self, textvariable=self.fencer_name, validate="key",
                                 validatecommand=(self.register(names_validator), "%P"), width=24)

        def firstname_title(*args):
            """
            Convertit la casse du prénom du participant en majuscule pour la première lettre de chaque mot et en
            minuscule pour le reste.

            Parameters
            ----------
            args: str
            """
            self.fencer_firstname.set(self.fencer_firstname.get().title())

        # Prénom du participant
        self.fencer_firstname.trace_add("write", firstname_title)
        firstname_label = ttk.Label(self, text="Prénom")
        firstname_textbox = ttk.Entry(self, textvariable=self.fencer_firstname, validate="key",
                                      validatecommand=(self.register(names_validator), "%P"), width=24)

        # Equipe du participant
        team_label = ttk.Label(self, text="Équipe")
        team_combobox = ttk.Combobox(self, textvariable=self.fencer_team, values=self.parent.tournament_teams, width=22)

        def numbers_validator(arg):
            """
            Vérifie la nature des caractères de l'âge du participant : numérique.

            Parameters
            ----------
            arg: str
                L'âge du participant

            Returns
            -------
            bool
                True si la nature est vérifiée, sinon False
            """
            return arg == "" or arg.isnumeric()

        # Age du participant
        age_label = ttk.Label(self, text="Âge")
        age_textbox = ttk.Entry(self, textvariable=self.fencer_age, validate="key",
                                validatecommand=(self.register(numbers_validator), "%P"), width=24)

        # Sexe du participant
        gender_label = ttk.Label(self, text="Sexe")
        gender_combobox = ttk.Combobox(self, textvariable=self.fencer_gender, values=("Masculin", "Féminin"),
                                       state="readonly", width=22)
        if self.parent.tournament_properties["gender"] == "Hommes":
            gender_combobox.current(0)
        elif self.parent.tournament_properties["gender"] == "Dames":
            gender_combobox.current(1)

        # Club du participant
        club_label = ttk.Label(self, text="Club")
        club_combobox = ttk.Combobox(self, textvariable=self.fencer_club, values=self.parent.tournament_clubs, width=22)

        # Licence du participant
        licence_label = ttk.Label(self, text="Licence")
        licence_textbox = ttk.Entry(self, textvariable=self.fencer_licence, validate="key",
                                    validatecommand=(self.register(numbers_validator), "%P"), width=24)

        # Placement des widgets
        name_label.place(anchor=tk.NE, relx=0.17, rely=0.07)
        name_textbox.place(relx=0.19, rely=0.07)
        firstname_label.place(anchor=tk.NE, relx=0.17, rely=0.14)
        firstname_textbox.place(relx=0.19, rely=0.14)
        if self.parent.tournament_properties["kind"] == "Individuel":
            age_label.place(anchor=tk.NE, relx=0.17, rely=0.21)
            age_textbox.place(relx=0.19, rely=0.21)
            gender_label.place(anchor=tk.NE, relx=0.17, rely=0.28)
            gender_combobox.place(relx=0.19, rely=0.28)
            if self.parent.tournament_properties["licence"]:
                club_label.place(anchor=tk.NE, relx=0.17, rely=0.35)
                club_combobox.place(relx=0.19, rely=0.35)
                licence_label.place(anchor=tk.NE, relx=0.17, rely=0.42)
                licence_textbox.place(relx=0.19, rely=0.42)
        elif self.parent.tournament_properties["kind"] == "Equipe":
            team_label.place(anchor=tk.NE, relx=0.17, rely=0.21)
            team_combobox.place(relx=0.19, rely=0.21)
            age_label.place(anchor=tk.NE, relx=0.17, rely=0.28)
            age_textbox.place(relx=0.19, rely=0.28)
            gender_label.place(anchor=tk.NE, relx=0.17, rely=0.35)
            gender_combobox.place(relx=0.19, rely=0.35)
            if self.parent.tournament_properties["licence"]:
                club_label.place(anchor=tk.NE, relx=0.17, rely=0.42)
                club_combobox.place(relx=0.19, rely=0.42)
                licence_label.place(anchor=tk.NE, relx=0.17, rely=0.49)
                licence_textbox.place(relx=0.19, rely=0.49)

    def __create_adder(self):
        """
        Crée le bouton permettant d'ajouter un participant.
        """

        # Style du widget
        ttk.Style().configure("TButton", font="Arial 16")

        # Bouton "Ajouter"
        button = ttk.Button(self, command=self.__add_fencer, text="Ajouter")

        # Placement du widget
        button.place(anchor=tk.SE, relx=0.73, rely=0.96, relwidth=0.14, relheight=0.11)

    def __create_closer(self):
        """
        Crée le bouton permettant de fermer la fenêtre.
        """

        # Style du widget
        ttk.Style().configure("TButton", font="Arial 16")

        # Bouton "Fermer"
        button = ttk.Button(self, command=self.destroy, text="Fermer")

        # Placement du widget
        button.place(anchor=tk.SE, relx=0.93, rely=0.96, relwidth=0.14, relheight=0.11)

    def __add_fencer(self):
        """
        Ajoute un participant au tournoi.
        """

        # Participant
        fencer = {"name": self.fencer_name.get().strip(),
                  "firstname": self.fencer_firstname.get().strip(),
                  "team": self.fencer_team.get().strip(),
                  "age": self.fencer_age.get().strip(),
                  "gender": self.fencer_gender.get(),
                  "club": self.fencer_club.get().strip(),
                  "licence": self.fencer_licence.get().strip()}

        # Vérification de la complétion des champs requis
        if fencer["name"] == "":
            mb.showerror(title="Erreur saisie", message="Veuillez renseigner le nom du participant.", parent=self)
        elif fencer["firstname"] == "":
            mb.showerror(title="Erreur saisie", message="Veuillez renseigner le prénom du participant.", parent=self)
        elif self.parent.tournament_properties["kind"] == "Equipe" and fencer["team"] == "":
            mb.showerror(title="Erreur saisie", message="Veuillez renseigner l'équipe du participant.", parent=self)
        elif self.parent.tournament_properties["licence"] and fencer["age"] == "":
            mb.showerror(title="Erreur saisie", message="Veuillez renseigner l'âge du participant.", parent=self)
        elif self.parent.tournament_properties["licence"] and fencer["gender"] == "":
            mb.showerror(title="Erreur saisie", message="Veuillez renseigner le sexe du participant.", parent=self)
        elif self.parent.tournament_properties["licence"] and fencer["club"] == "":
            mb.showerror(title="Erreur saisie", message="Veuillez renseigner le club du participant.", parent=self)
        elif self.parent.tournament_properties["licence"] and fencer["licence"] == "":
            mb.showerror(title="Erreur saisie", message="Veuillez renseigner la licence du participant.", parent=self)

        # Ajouts des nouvelles équipes et nouveaux clubs, et attribution des indices correspondants
        else:
            new_team = False
            team_index = None
            club_index = None
            if self.parent.tournament_properties["kind"] == "Equipe":
                try:
                    team_index = list(map(lambda x: x.casefold(), self.parent.tournament_teams)).index(
                        fencer["team"].casefold())
                except ValueError:
                    new_team = True
                    team_index = len(self.parent.tournament_teams)
                    self.parent.tournament_teams.append(fencer["team"])
                    self.parent.total_teams_added += 1
            if self.parent.tournament_properties["licence"]:
                try:
                    club_index = list(map(lambda x: x.casefold(), self.parent.tournament_clubs)).index(
                        fencer["club"].casefold())
                except ValueError:
                    club_index = len(self.parent.tournament_clubs)
                    self.parent.tournament_clubs.append(fencer["club"])
            self.parent.total_fencers_added += 1
            fencer["team"] = team_index
            fencer["club"] = club_index

            # ...
            tournament_fencer = []
            if fencer["team"] is not None:
                tournament_fencer.append(self.parent.tournament_teams[fencer["team"]])
            tournament_fencer.extend([fencer["name"], fencer["firstname"], fencer["age"], fencer["gender"]])
            if fencer["club"] is not None:
                tournament_fencer.append(self.parent.tournament_clubs[fencer["club"]])
            tournament_fencer.append(fencer["licence"])
            tournament_fencer = tuple(tournament_fencer)

            # ...
            if new_team and self.parent.tournament_properties["licence"]:
                self.parent.table.insert("", tk.END, values=(tournament_fencer[0], "", "", "", "", "", ""),
                                         iid=f"T{self.parent.total_teams_added}", open=True,
                                         tags=(str(len(self.parent.tournament_fencers) % 2),))
            elif new_team:
                self.parent.table.insert("", tk.END, values=(tournament_fencer[0], "", "", "", ""),
                                         iid=f"T{self.parent.total_teams_added}", open=True,
                                         tags=(str(len(self.parent.tournament_fencers) % 2),))

            if self.parent.tournament_properties["kind"] == "Equipe":
                self.parent.table.insert(f"T{team_index + 1}", tk.END, values=tournament_fencer,
                                         iid=f"F{self.parent.total_fencers_added}",
                                         tags=(str(len(self.parent.tournament_fencers) % 2),))
            else:
                self.parent.table.insert("", tk.END, values=tournament_fencer,
                                         iid=f"F{self.parent.total_fencers_added}",
                                         tags=(str(len(self.parent.tournament_fencers) % 2),))
            self.parent.tournament_fencers.append(tournament_fencer)

            # ...
            self.destroy()
            self.parent.add_fencer()


class TournamentFrame(ttk.Frame):

    def __init__(self, master, id_, background, foreground, heading, weapon, gender, category, score, kind, licence,
                 draw):
        super().__init__(master)

        # Caractéristiques du tableau
        self.frame_id = id_
        self.color_background = background
        self.color_foreground = foreground
        self.total_teams_added = 0
        self.total_fencers_added = 0

        # Caractéristiques du tournoi
        self.tournament_properties = {"heading": heading,
                                      "weapon": weapon,
                                      "gender": gender,
                                      "category": category,
                                      "score": score,
                                      "kind": kind,
                                      "licence": licence,
                                      "draw": draw}
        self.tournament_teams = []
        self.tournament_clubs = []
        self.tournament_fencers = []

        self.create_actions()
        self.table = self.create_table()

    def create_actions(self):
        ttk.Style().configure("TButton", font="Arial 16")

        add_button = ttk.Button(self, command=self.add_fencer, text="Ajouter")
        remove_button = ttk.Button(self, command=self.remove_fencers, text="Enlever")

        add_button.pack(anchor=tk.NW)
        remove_button.pack(anchor=tk.NW)

    def create_table(self):
        custom_style_name = f"My{self.frame_id}.Treeview"
        ttk.Style().configure(f"{custom_style_name}.Heading", font="Consolas 16", background=self.color_background,
                              foreground=self.color_foreground)
        ttk.Style().configure("Treeview", font="Consolas 14")

        if self.tournament_properties["kind"] == "Individuel" and self.tournament_properties["licence"]:
            columns = ("name", "firstname", "age", "gender", "club", "licence")
        elif self.tournament_properties["kind"] == "Individuel":
            columns = ("name", "firstname", "age", "gender")
        elif self.tournament_properties["kind"] == "Equipe" and self.tournament_properties["licence"]:
            columns = ("team", "name", "firstname", "age", "gender", "club", "licence")
        else:
            columns = ("team", "name", "firstname", "age", "gender")

        if self.tournament_properties["kind"] == "Individuel":
            tree = ttk.Treeview(self, columns=columns, show="headings", style=custom_style_name)
        else:
            tree = ttk.Treeview(self, columns=columns, show="tree headings", style=custom_style_name)

        if self.tournament_properties["kind"] == "Equipe":
            tree.heading("#0", text="Equipe")
            tree.heading("team", text="Equipe")
        tree.heading("name", text="Nom")
        tree.heading("firstname", text="Prénom")
        tree.heading("age", text="Age")
        tree.heading("gender", text="Sexe")
        if self.tournament_properties["licence"]:
            tree.heading("club", text="Club")
            tree.heading("licence", text="Licence")

        tree.tag_configure("1", background="#E8E8E8")

        tree.pack(fill="both", expand=True)

        tree.bind("<Double-1>", lambda x: print("Hey !"))  # to complete [modify function]

        return tree

    def add_fencer(self):
        window = FencerProperties(self)
        window.grab_set()

    def remove_fencers(self):
        selected_fencers_iid = self.table.selection()
        selected_fencers_idx = sorted([self.table.index(iid) for iid in selected_fencers_iid], reverse=True)

        self.table.delete(*selected_fencers_iid)
        for idx in selected_fencers_idx:
            del self.tournament_fencers[idx]

        left_fencers_iid = self.table.get_children()

        for idx, iid in enumerate(left_fencers_iid):
            self.table.item(iid, tags=(str(idx % 2),))


class TournamentProperties(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.color_background = "#008000"
        self.color_foreground = "#FFFFFF"
        self.tournament_heading = tk.StringVar(value=None)
        self.tournament_weapon = tk.StringVar()
        self.tournament_gender = tk.StringVar()
        self.tournament_category = tk.StringVar()
        self.tournament_score = tk.IntVar(value=1)
        self.tournament_kind = tk.StringVar(value="Individuel")
        self.tournament_licence = tk.BooleanVar(value=False)
        self.tournament_draw = tk.BooleanVar(value=False)

        # Caractéristiques de la fenêtre
        self.title("Nouveau tournoi")
        self.iconbitmap(r"images\LeFunnyIcon.ico")
        self.geometry("600x600+70+70")
        self.resizable(False, False)

        self.create_header()
        self.create_properties()
        self.create_validation()

    def create_header(self):
        label = ttk.Label(self, text="Nouveau tournoi", anchor=tk.CENTER, font="Arial 24",
                          background=self.color_background, foreground=self.color_foreground)
        button = tk.Button(self, bg=self.color_background, fg=self.color_foreground)

        def change_color():
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

        button.config(command=change_color)

        label.place(relx=0.03, rely=0.03, relwidth=0.8, relheight=0.1)
        button.place(anchor=tk.NE, relx=0.97, rely=0.03, relwidth=0.1, relheight=0.1)

    def create_properties(self):
        self.option_add("*Font", "Arial 16")
        ttk.Style().configure("TRadiobutton", font="Arial 16")
        ttk.Style().configure("TCheckbutton", font="Arial 16")

        heading_label = ttk.Label(self, text="Titre")
        heading_textbox = ttk.Entry(self, textvariable=self.tournament_heading, width=18)

        weapon_label = ttk.Label(self, text="Arme")
        weapon_combobox = ttk.Combobox(self, textvariable=self.tournament_weapon,
                                       values=("Fleuret", "Epée", "Sabre", "Laser", "Multi"), state="readonly",
                                       width=16)
        weapon_combobox.current(0)

        gender_label = ttk.Label(self, text="Sexe")
        gender_combobox = ttk.Combobox(self, textvariable=self.tournament_gender, values=("Hommes", "Dames", "Mixte"),
                                       state="readonly", width=16)
        gender_combobox.current(0)

        category_label = ttk.Label(self, text="Catégorie")
        category_combobox = ttk.Combobox(self, textvariable=self.tournament_category, values=(
            "M5", "M7", "M9", "M11", "M13", "M15", "M17", "M20", "M23", "Senior", "Vétéran", "Vétéran 1", "Vétéran 2",
            "Vétéran 3", "Vétéran 4", "Vétéran 5", "Vétéran 3 + 4", "Vétéran 4 + 5"), width=16)
        category_combobox.current(0)

        def validator(arg):
            return (arg.isnumeric() and 1 <= int(arg) <= 999) or arg == ""

        score_label = ttk.Label(self, text="Score victorieux")
        score_spinbox = ttk.Spinbox(self, textvariable=self.tournament_score, from_=1, to=999, validate="key",
                                    validatecommand=(self.register(validator), "%P"), width=15)

        individual_radiobutton = ttk.Radiobutton(self, variable=self.tournament_kind, text="Individuel",
                                                 value="Individuel")
        team_radiobutton = ttk.Radiobutton(self, variable=self.tournament_kind, text="Equipe", value="Equipe")

        licence_checkbox = ttk.Checkbutton(self, text="Tournoi licenciés", variable=self.tournament_licence)

        draw_checkbox = ttk.Checkbutton(self, text="Matchs nuls", variable=self.tournament_draw)

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

    def create_validation(self):
        ttk.Style().configure("TButton", font="Arial 16")

        button = ttk.Button(self, command=self.submit, text="OK")

        button.place(anchor=tk.SE, relx=0.96, rely=0.96, relwidth=0.14, relheight=0.11)

    def submit(self):
        tournament = {"heading": self.tournament_heading.get().strip(),
                      "weapon": self.tournament_weapon.get(),
                      "gender": self.tournament_gender.get(),
                      "category": self.tournament_category.get().strip(),
                      "kind": self.tournament_kind.get(),
                      "score": None,
                      "licence": self.tournament_licence.get(),
                      "draw": self.tournament_draw.get()}

        if tournament["category"] == "":
            mb.showerror(title="Erreur saisie", message="Veuillez renseigner la catégorie du tournoi.", parent=self)
        else:
            try:
                tournament["score"] = self.tournament_score.get()
            except tk.TclError:
                mb.showerror(title="Erreur saisie",
                             message="Veuillez renseigner la condition de victoire au score du tournoi.", parent=self)
            else:
                if tournament["heading"] == "":
                    tournament["heading"] = f"{tournament['weapon']}{tournament['gender']}{tournament['category']}"

                if not self.parent.is_notebook:
                    self.parent.background_notebook = ttk.Notebook(self.parent)

                    self.parent.background_image.pack_forget()
                    self.parent.background_notebook.pack(fill="both", expand=True)

                    self.parent.is_notebook = True

                frame = TournamentFrame(self.parent.background_notebook, len(self.parent.notebook_frames),
                                        self.color_background, self.color_foreground, **tournament)

                im = Image.new("RGB", (180, 40), self.color_background)
                im_draw = ImageDraw.Draw(im)
                im_draw.text((90, 20), tournament["heading"], fill=self.color_foreground, anchor="mm",
                             font=ImageFont.truetype("arial", 20))
                frame.img = ImageTk.PhotoImage(im)

                self.parent.background_notebook.add(frame, image=frame.img)

                self.parent.notebook_frames.append(frame)
                self.destroy()


class App(tk.Tk):

    def __init__(self):
        super().__init__()
        ttk.Style().theme_use("winnative")

        # Caractéristiques de la fenêtre
        self.title("LeFunnyTournament")
        self.iconbitmap(r"images\LeFunnyIcon.ico")
        self.geometry("1480x780+20+20")
        self.minsize(700, 550)  # 700 550

        self.background_image = None
        self.background_notebook = None
        self.notebook_frames = []
        self.is_notebook = False

        self.create_menu_bar()
        self.background_image = self.create_background()

    def create_menu_bar(self):
        self.option_add("*Menu*Font", "Arial 12")

        menu_bar = tk.Menu(self)

        menu_file = tk.Menu(menu_bar, tearoff=False)
        menu_file.add_command(command=self.new_file, label="Nouveau", underline=False, accelerator="Ctrl+N")
        menu_file.add_command(command=self.open_file, label="Ouvrir", underline=False, accelerator="Ctrl+O")

        menu_recent = tk.Menu(menu_file, tearoff=False)
        menu_recent.add_command(label="Fichier 1")
        menu_recent.add_command(label="Fichier 2")
        menu_recent.add_command(label="Fichier 3")
        menu_file.add_cascade(menu=menu_recent, label="Récemment ouverts", underline=False)

        menu_file.add_command(command=..., label="Enregistrer", underline=False, accelerator="Ctrl+S")
        menu_file.add_command(command=..., label="Enregistrer sous", underline=False, accelerator="Maj+Ctrl+S")
        menu_file.add_separator()
        menu_file.add_command(command=self.quit, label="Quitter", underline=True)
        menu_bar.add_cascade(menu=menu_file, label="Fichier", underline=False)

        self.config(menu=menu_bar)

        self.bind_all("<Control-n>", lambda x: self.new_file())
        self.bind_all("<Control-o>", lambda x: self.open_file())
        self.bind_all("<Control-s>", lambda x: ...)
        self.bind_all("<Control-Shift-S>", lambda x: ...)

    def create_background(self):
        canvas = tk.Canvas(self, width=700, height=550, bg="#FFFFFF")

        canvas.img = tk.PhotoImage(file=r"images\LeFunnyFencer.png")
        canvas.create_image((350, 275), image=canvas.img)

        canvas.pack(anchor=tk.CENTER, expand=True)

        return canvas

    def new_file(self):
        window = TournamentProperties(self)
        window.grab_set()

    def open_file(self):
        file = fd.askopenfilename(title="Ouvrir", filetypes=(("Fichiers TXT", "*.txt"), ("Tous les fichiers", "*.*")))
        print(file)


if __name__ == "__main__":
    app = App()
    try:
        from ctypes import windll

        windll.shcore.SetProcessDpiAwareness(1)

    finally:
        app.mainloop()