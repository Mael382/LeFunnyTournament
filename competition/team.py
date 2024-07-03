from competition.fencer import Fencer


class Team:
    """
    Classe représentant une équipe.

    :param str name: Nom de l'équipe.
    :param set[Fencer] fencers: Tireurs de l'équipe.
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
    #: Exemption de l'équipe
    _has_been_exempted: bool

    def __init__(self, name: str, *,
                 fencers: set[Fencer] | None = None) -> None:
        """
        Initialise une nouvelle équipe.
        """
        # Nom
        if len(name) == 0:
            raise ValueError("Le paramètre `name` doit être non vide.")
        self._name = name

        # Tireurs
        if not all(map(lambda x: x.has_team, fencers)):
            raise ValueError("La propriété `has_team` doit être `True` pour tous les éléments du paramètre `fencers`.")
        if fencers is None:
            self._fencers = set()
        else:
            self._fencers = fencers

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

    @property
    def fencers(self) -> set[Fencer]:
        return self._fencers

    @property
    def victories(self) -> float:
        return self._victories

    @property
    def touches_scored(self) -> int:
        return self._touches_scored

    @property
    def touches_received(self) -> int:
        return self._touches_received

    @property
    def opponents_encountered(self) -> set["Team"]:
        return self._opponents_encountered

    @property
    def has_been_exempted(self) -> bool:
        return self._has_been_exempted

    @property
    def size(self) -> int:
        """
        Nombre de tireurs dans l'équipe.
        """
        return len(self._fencers)

    @property
    def are_licensed(self) -> bool:
        """
        Titularisation des tireurs de l'équipe.
        """
        return all(map(lambda x: x.is_licensed, self._fencers))
    # TODO : Y a-t-il un meilleur terme que "titularisation" ?

    @property
    def indicator(self) -> int:
        """
        Indice de l'équipe.
        """
        return self._touches_scored - self._touches_received

    @property
    def score(self) -> tuple[float, int, int]:
        """
        Score global de l'équipe.
        """
        return self._victories, self.indicator, self._touches_scored

    @property
    def fencers_sorted_by_name(self) -> list[Fencer]:
        """
        Tireurs de l'équipe, triés par nom complet.
        """
        return sorted(self._fencers, key=lambda x: x.name)

    @property
    def fencers_sorted_by_gender(self) -> list[Fencer]:
        """
        Tireurs de l'équipe, triés par sexe.
        """
        return sorted(self._fencers, key=lambda x: x.gender, reverse=True)

    @property
    def fencers_sorted_by_age(self) -> list[Fencer]:
        """
        Tireurs de l'équipe, triés par âge.
        """
        return sorted(self._fencers, key=lambda x: x.age, reverse=True)

    @property
    def fencers_sorted_by_club(self) -> list[Fencer]:
        """
        Tireurs de l'équipe, triés par club.
        """
        if self.are_licensed:
            return sorted(self._fencers, key=lambda x: x.club)
        else:
            return list(self._fencers)

    @property
    def fencers_sorted_by_licence(self) -> list[Fencer]:
        """
        Tireurs de l'équipe, triés par licence.
        """
        if self.are_licensed:
            return sorted(self._fencers, key=lambda x: x.licence)
        else:
            return list(self._fencers)

    @property
    def names(self) -> set[tuple[str, str]]:
        """
        Noms complets des tireurs de l'équipe.
        """
        return set(map(lambda x: x.name, self._fencers))

    @property
    def names_sorted(self) -> list[tuple[str, str]]:
        """
        Noms complets triés des tireurs de l'équipe.
        """
        return sorted(self.names)

    @property
    def genders(self) -> set[str]:
        """
        Sexes des tireurs de l'équipe.
        """
        return set(map(lambda x: x.gender, self._fencers))

    @property
    def genders_sorted(self) -> list[str]:
        """
        Sexes triés des tireurs de l'équipe.
        """
        return sorted(self.genders, reverse=True)

    @property
    def ages(self) -> set[int]:
        """
        Âges des tireurs de l'équipe.
        """
        return set(map(lambda x: x.age, self._fencers))

    @property
    def ages_sorted(self) -> list[int]:
        """
        Âges triés des tireurs de l'équipe.
        """
        return sorted(self.ages, reverse=True)

    @property
    def clubs(self) -> set[str]:
        """
        Clubs des tireurs de l'équipe.
        """
        if self.are_licensed:
            return set(map(lambda x: x.club, self._fencers))
        else:
            return set()

    @property
    def clubs_sorted(self) -> list[str]:
        """
        Clubs triés des tireurs de l'équipe.
        """
        return sorted(self.clubs)

    @property
    def licences(self) -> set[int]:
        """
        Licences des tireurs de l'équipe.
        """
        if self.are_licensed:
            return set(map(lambda x: x.licence, self._fencers))
        else:
            return set()

    @property
    def licences_sorted(self) -> list[int]:
        """
        Licences triées des tireurs de l'équipe.
        """
        return sorted(self.licences)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self._name}, fencers={None if self.size == 0 else self._fencers})"

    def __hash__(self) -> int:
        return hash(self._name)

    def __eq__(self, other_team: "Team") -> bool:
        return self.score == other_team.score

    def __ne__(self, other_team: "Team") -> bool:
        return self.score != other_team.score

    def __lt__(self, other_team: "Team") -> bool:
        return self.score < other_team.score

    def __le__(self, other_team: "Team") -> bool:
        return self.score <= other_team.score

    def __gt__(self, other_team: "Team") -> bool:
        return self.score > other_team.score

    def __ge__(self, other_team: "Team") -> bool:
        return self.score >= other_team.score

    def add_fencer(self, fencer: Fencer) -> None:
        """
        Ajoute un tireur à l'équipe.

        :param fencer: Tireur entrant.
        """
        if fencer not in self._fencers:
            self._fencers.add(fencer)

    def remove_fencer(self, fencer: Fencer) -> None:
        """
        Retire un tireur de l'équipe.

        :param fencer: Tireur sortant.
        """
        if fencer in self._fencers:
            self._fencers.discard(fencer)

    def get_fencer_by_name(self, lastname: str, firstname: str) -> Fencer | None:
        """
        Cherche le tireur de l'équipe correspondant aux nom et prénom fournis.

        :param lastname: Nom du tireur.
        :param firstname: Prénom du tireur.
        :return: Tireur de l'équipe correspondant aux nom et prénom donnés.
        """
        return next((fencer for fencer in self._fencers if fencer.name == (lastname, firstname)), None)

    def get_fencer_by_licence(self, licence: int) -> Fencer | None:
        """
        Cherche le tireur de l'équipe correspondant à la licence fournie.

        :param licence: Licence du tireur.
        :return: Tireur de l'équipe correspondant à la licence fournie.
        """
        return next((fencer for fencer in self._fencers if fencer.licence == licence), None)

    def win(self, opponent: "Team", *,
            self_touches: int, opponent_touches: int) -> None:
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
        if opponent not in self._opponents_encountered:
            self._opponents_encountered.add(opponent)

        # Score de l'adversaire
        opponent._touches_scored += opponent_touches
        opponent._touches_received += self_touches

        # Mémoire de l'adversaire
        if self not in opponent._opponents_encountered:
            opponent._opponents_encountered.add(self)

    def draw(self, opponent: "Team", touches: int) -> None:
        """
        Ajoute un match nul à l'équipe et son adversaire.

        :param opponent: Adversaire de l'équipe.
        :param touches: Touches portées par les équipes, individuellement.
        """
        # Score de l'équipe
        self._victories += 0.5
        self._touches_scored += touches
        self._touches_received += touches

        # Mémoire de l'équipe
        if opponent not in self._opponents_encountered:
            self._opponents_encountered.add(opponent)

        # Score de l'adversaire
        opponent._victories += 0.5
        opponent._touches_scored += touches
        opponent._touches_received += touches

        # Mémoire de l'adversaire
        if self not in opponent._opponents_encountered:
            opponent._opponents_encountered.add(self)

    def bye(self) -> None:
        """
        Ajoute une ronde exemptée à l'équipe.
        """
        # Score de l'équipe
        self._victories += 1.0

        # Mémoire de l'équipe
        self._has_been_exempted = True
