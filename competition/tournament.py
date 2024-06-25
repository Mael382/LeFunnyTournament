from assault.round import Round

from competition.fencer import Fencer
from competition.team import Team


class Tournament:
    """
    Classe représentant une compétition.

    :param name: Nom de la compétition.
    :param weapon: Arme de la compétition.
    :param gender: Sexe de la compétition.
    :param category: Catégorie de la compétition.
    :param kind: Type de compétition : `Individuelle` ou `Équipe`.
    :param maximum_score: Score maximum des matchs.
    :param licences_are_needed: Exigence des licences des tireurs.
    :param draws_are_allowed: Autorisation des matchs nuls.
    """
    #: Nom de la compétition
    _name: str
    #: Arme de la compétition
    _weapon: str
    #: Sexe de la compétition
    _gender: str
    #: Catégorie de la compétition
    _category: str
    #: Type de compétition : `Individuelle` ou `Équipe`
    _kind: str
    #: Score maximum des matchs
    _maximum_score: int
    #: Exigence des licences des tireurs
    _licences_are_needed: bool
    #: Autorisation des matchs nuls
    _draws_are_allowed: bool
    #: Tireurs/Équipes de la compétition
    _participants: set[Fencer] | set[Team]
    #: Rondes de la compétition
    _round: list[Round]

    def __init__(self,
                 name: str,
                 weapon: str,
                 gender: str,
                 category: str,
                 kind: str,
                 maximum_score: int,
                 licences_are_needed: bool,
                 draws_are_allowed: bool) -> None:
        """
        Initialise une nouvelle compétition.
        """
        # Nom
        if len(name) == 0:
            raise ValueError("Le paramètre `name` doit être non vide.")
        # TODO : conditions pour un nom valide (orthographe + insultes)
        self._name = name

        # Arme
        if weapon not in frozenset({"Fleuret", "Épée", "Sabre", "Laser", "Multi"}):
            raise ValueError("Le paramètre `weapon` doit être parmi `{'Fleuret', 'Épée', 'Sabre', 'Laser', 'Multi'}`.")
        self._weapon = weapon

        # Sexe
        if gender not in frozenset({"Hommes", "Dames", "Mixte"}):
            raise ValueError("Le paramètre `gender` doit être parmi `{'Hommes', 'Dames', 'Mixte'}`.")
        self._gender = gender

        # Catégorie
        if len(category) == 0:
            raise ValueError("Le paramètre `category` doit être non vide.")
        # TODO : conditions pour une catégorie valide (orthographe + insultes)
        self._category = category

        # Type : `Individuelle` ou `Équipe`
        if kind not in frozenset({"Individuelle", "Équipe"}):
            raise ValueError("Le paramètre `kind` doit être parmi `{'Individuelle', 'Équipe'}`.")
        self._kind = kind

        # Score maximum
        if maximum_score <= 0:
            raise ValueError("Le paramètre `maximum_score` doit être strictement supérieur à `0`.")
        self._maximum_score = maximum_score

        # Exigence des licences
        self._licences_are_needed = licences_are_needed

        # Autorisation des matchs nuls
        self._draws_are_allowed = draws_are_allowed

        # Tireurs/Équipes
        self._participants = set()

        # Rondes
        self._rounds = list()

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        if len(new_name) == 0:
            raise ValueError("Le paramètre `name` doit être non vide.")
        # TODO : conditions pour un nom valide (orthographe + insultes)
        self._name = new_name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self._name!r}, weapon={self._weapon!r}, gender={self._gender!r}, "\
               f"category={self._category!r}, kind={self._kind!r}, maximum_score={self._maximum_score}, "\
               f"licences_are_needed={self._licences_are_needed}, draws_are_allowed={self._draws_are_allowed}"

    def add_participant(self, participant: Fencer | Team) -> None:
        """
        Ajoute un participant à la compétition.

        :param participant: Participant entrant.
        """
        if isinstance(participant, Team) and (self._kind == "Individuelle"):
            raise TypeError("Le paramètre `participant` doit être une instance de `Fencer`.")
        elif isinstance(participant, Fencer) and (self._kind == "Équipe"):
            raise TypeError("Le paramètre `participant` doit être une instance de `Team`.")
        self._participants.add(participant)

    def remove_participant(self, participant: Fencer | Team) -> None:
        """
        Retire un participant de la compétition.

        :param participant: Participant sortant.
        """
        self._participants.discard(participant)






























'''
        # Widgets
        self.__create_actions()
        self.table = self.__create_table()


    def __create_actions(self) -> None:
        """Crée les widgets permettant d'exécuter les différentes opérations possibles sur la compétition.
        """
        # Style
        ttk.Style().configure("TButton", font="Arial 16")

        # Boutons
        adding_button = ttk.Button(self, command=self.adding_fencers_window, text="Ajouter tireurs")
        removing_button = ttk.Button(self, command=self.removing_fencers_selected, text="Supprimer tireurs")
        running_button = ttk.Button(self, command=self.running_round_window, text="Tour suivant")

        # Positionnements
        adding_button.pack(anchor=tk.NW)
        removing_button.pack(anchor=tk.NW)
        running_button.pack(anchor=tk.NE)

    def __create_table(self) -> ttk.Treeview:
        """Crée le tableau d'affichage de la compétition.

        :return: Le tableau d'affichage de la compétition.
        """
        # Styles
        custom_style_name = f"My{self.id}.Treeview"
        ttk.Style().configure(f"{custom_style_name}.Heading",
                              font="Consolas 16",
                              background=self.background_color,
                              foreground=self.foreground_color)
        ttk.Style().configure("Treeview", font="Consolas 14")

        # Columns
        columns = []
        if self.kind == "Équipe":
            columns.append("team")
        columns.extend(("lastname", "firstname", "age", "gender"))
        if self.licence_is_needed:
            columns.extend(("club", "licence"))
        columns.extend(("victories", "touches scored", "touches received", "indicator"))
        columns = tuple(columns)

        # Tree
        if self.kind == "Individuelle":
            tree = ttk.Treeview(self, columns=columns, show="headings", style=custom_style_name)
        elif self.kind == "Équipe":
            tree = ttk.Treeview(self, columns=columns, show="tree headings", style=custom_style_name)

        # Organisation
        if self.kind == "Équipe":
            tree.heading("#0", text="Équipe")
            tree.heading("team", text="Équipe")
        tree.heading("lastname", text="Nom")
        tree.heading("firstname", text="Prénom")
        tree.heading("age", text="Âge")
        tree.heading("gender", text="Sexe")
        if self.licence_is_needed:
            tree.heading("club", text="Club")
            tree.heading("licence", text="Licence")
        tree.heading("victories", text="Victoires")
        tree.heading("touches scored", text="Touches données")
        tree.heading("touches received", text="Touches reçues")
        tree.heading("indicator", text="Indice")

        # Configuration
        tree.tag_configure("1", background="#E8E8E8")

        # Positionnement
        tree.pack(fill="both", expand=True)

        # ...
        tree.bind("<Double-1>", lambda x: print("Hey !"))  # TO COMPLETE [modify function]

        return tree

    def adding_fencers_window(self) -> None:
        """...
        """
        window = FencerProperties(self)
        window.grab_set()

    def removing_fencers_selected(self) -> None:
        """...
        """
        selected_fencers_iid = self.table.selection()
        selected_fencers_idx = sorted([self.table.index(iid) for iid in selected_fencers_iid], reverse=True)

        self.table.delete(*selected_fencers_iid)
        for idx in selected_fencers_idx:
            self.tournament_fencers.pop(idx)

        left_fencers_iid = self.table.get_children()

        for idx, iid in enumerate(left_fencers_iid):
            self.table.item(iid, tags=(str(idx % 2),))

    def running_round_window(self) -> None:
        window = RoundProperties(self)
        window.grab_set()

        selected_fencers_iid = self.table.selection()
        selected_fencers_idx = [self.table.index(iid) for iid in selected_fencers_iid]
        for i in range(len(selected_fencers_iid)):
            self.table.set(selected_fencers_iid[i],
                           column="wins",
                           value=self.tournament_fencers[selected_fencers_idx[i]]["wins"])
            self.table.set(selected_fencers_iid[i],
                           column="indice",
                           value=self.tournament_fencers[selected_fencers_idx[i]]["indice"])
            self.table.set(selected_fencers_iid[i],
                           column="score",
                           value=self.tournament_fencers[selected_fencers_idx[i]]["score"])
'''

