from competition.fencer import Fencer


class Team:
    """
    Classe représentant une équipe.

    :param str name: Nom de l'équipe.
    """
    #: Nom de l'équipe
    _name: str
    #: Tireurs de l'équipe.
    _fencers: set[Fencer]
    #: Victoires de l'équipe
    _victories: float
    #: Touches portées par l'équipe
    _touches_scored: int
    #: Touches reçues par l'équipe
    _touches_received: int
    #: Équipes adverses rencontrées
    _opponents_encountered: set["Team"]
    #: Une ronde exemptée dans la compétition
    _has_been_exempted: bool

    def __init__(self, name: str) -> None:
        """
        Initialise une nouvelle équipe.
        """
        # Nom
        if len(name) == 0:
            raise ValueError("Le paramètre `name` doit être non vide.")
        # TODO : conditions pour un nom valide (orthographe + insultes)
        self._name = name

        # Tireurs
        self._fencers = set()

        # Score
        self._victories = 0.0
        self._touches_scored = 0
        self._touches_received = 0

        # Mémoire
        self._opponents_encountered = set()
        self._has_been_exempted = False

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        if len(new_name) == 0:
            raise ValueError("L'attribut `name` doit être non vide.")
        # TODO : conditions pour un nom valide (orthographe + insultes)
        self._name = new_name

    @property
    def victories(self) -> float:
        return self._victories

    @property
    def indicator(self) -> int:
        """
        Indice de l'équipe.
        """
        return self._touches_scored - self._touches_received

    @property
    def opponents_encountered(self) -> set["Team"]:
        return self._opponents_encountered

    @property
    def has_been_exempted(self) -> bool:
        return self._has_been_exempted

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self._name})"

    def __eq__(self, other_team: "Team") -> bool:
        return (self._victories, self.indicator, self._touches_scored) == (other_team._victories, other_team.indicator, other_team._touches_scored)

    def __ne__(self, other_team: "Team") -> bool:
        return (self._victories, self.indicator, self._touches_scored) != (other_team._victories, other_team.indicator, other_team._touches_scored)

    def __lt__(self, other_team: "Team") -> bool:
        return (self._victories, self.indicator, self._touches_scored) < (other_team._victories, other_team.indicator, other_team._touches_scored)

    def __le__(self, other_team: "Team") -> bool:
        return (self._victories, self.indicator, self._touches_scored) <= (other_team._victories, other_team.indicator, other_team._touches_scored)

    def __gt__(self, other_team: "Team") -> bool:
        return (self._victories, self.indicator, self._touches_scored) > (other_team._victories, other_team.indicator, other_team._touches_scored)

    def __ge__(self, other_team: "Team") -> bool:
        return (self._victories, self.indicator, self._touches_scored) >= (other_team._victories, other_team.indicator, other_team._touches_scored)

    def add_fencer(self, fencer: Fencer) -> None:
        """
        Ajoute un tireur à l'équipe.

        :param fencer: Tireur entrant.
        """
        self._fencers.add(fencer)

    def remove_fencer(self, fencer: Fencer) -> None:
        """
        Retire un tireur de l'équipe.

        :param fencer: Tireur sortant.
        """
        self._fencers.discard(fencer)

    def win(self, opponent: "Team", *, self_touches: int, opponent_touches: int) -> None:
        """
        Ajoute une victoire à l'équipe sur son adversaire.

        :param opponent: Adversaire de l'équipe.
        :param self_touches: Touches portées par l'équipe.
        :param opponent_touches: Touches portées par l'adversaire.
        """
        # Score de l'équipe
        self._victories += 1.0
        self._touches_scored += self_touches
        self._touches_received += opponent_touches

        # Mémoire de l'équipe
        self._opponents_encountered.add(opponent)

        # Score de l'adversaire
        opponent._touches_scored += opponent_touches
        opponent._touches_received += self_touches

        # Mémoire de l'adversaire
        opponent._opponents_encountered.add(self)

    def draw(self, opponent: "Team", touches: int) -> None:
        """
        Ajoute un match nul à l'équipe et son adversaire.

        :param opponent: Adversaire de l'équipe.
        :param touches: Touches portées par les équipes.
        """
        # Score de l'équipe
        self._victories += 0.5
        self._touches_scored += touches
        self._touches_received += touches

        # Mémoire de l'équipe
        self._opponents_encountered.add(opponent)

        # Score de l'adversaire
        opponent._victories += 0.5
        opponent._touches_scored += touches
        opponent._touches_received += touches

        # Mémoire de l'adversaire
        opponent._opponents_encountered.add(self)

    def bye(self) -> None:
        """
        Ajoute une ronde exemptée à l'équipe.
        """
        # Score de l'équipe
        self._victories += 1.0

        # Mémoire de l'équipe
        self._has_been_exempted = True












'''
    def as_table_entry(self) -> tuple[tuple[str, ...], ...]:
        """Renvoie l'équipe sous la forme d'une entrée de tableau.

        :return: L'entrée de tableau correspondant à l'équipe.
        """
        table_entry = []
        team_table_entry = [self.name, "", "", "", ""]
        if self.tournament.licence_is_needed:
            team_table_entry.extend(("", ""))
        team_table_entry.extend((str(self.victories),
                                 str(self.touches_scored),
                                 str(self.touches_received),
                                 str(self.indicator)))
        table_entry.append(tuple(team_table_entry))
        for fencer in self.fencers:
            table_entry.append(fencer.as_table_entry())
        return tuple(table_entry)
'''
