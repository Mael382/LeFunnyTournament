class Fencer:
    """
    Classe représentant un tireur.

    :param str lastname: Nom du tireur.
    :param str firstname: Prénom du tireur.
    :param int age: Âge du tireur.
    :param str gender: Sexe du tireur.
    :param str club: Club du tireur.
    :param int licence: Licence du tireur.
    :param bool in_team: Tireur en équipe.
    """
    #: Nom du tireur
    _lastname: str
    #: Prénom du tireur
    _firstname: str
    #: Âge du tireur
    _age: int
    #: Sexe du tireur
    _gender: str
    #: Club du tireur
    _club: str
    #: Licence du tireur
    _licence: int
    #: Victoires du tireur
    _victories: float | None
    #: Touches portées par le tireur
    _touches_scored: int | None
    #: Touches reçues par le tireur
    _touches_received: int | None
    #: Tireurs adverses rencontrés
    _opponents_encountered: set["Fencer"] | None
    #: Une ronde exemptée dans la compétition
    _has_been_exempted: bool | None

    def __init__(self,
                 lastname: str,
                 firstname: str,
                 age: int,
                 gender: str,
                 club: str,
                 licence: int,
                 in_team: bool = False) -> None:
        """
        Initialise un nouveau tireur.
        """

        # Nom
        if len(lastname) == 0:
            raise ValueError("Le paramètre `lastname` doit être non vide.")
        # TODO : conditions pour un nom valide (orthographe + insultes)
        self._lastname = lastname

        # Prénom
        if len(firstname) == 0:
            raise ValueError("Le paramètre `firstname` doit être non vide.")
        # TODO : conditions pour un prénom valide (orthographe + insultes)
        self._firstname = firstname

        # Âge
        if age <= 0:
            raise ValueError("Le paramètre `age` doit être strictement supérieur à `0`.")
        self._age = age

        # Sexe
        if gender not in frozenset({"H", "F", "A"}):
            raise ValueError("Le paramètre `gender` doit être parmi `{'H', 'F', 'A'}`.")
        self._gender = gender

        # Club
        if len(club) == 0:
            raise ValueError("Le paramètre `club` doit être non vide.")
        # TODO : conditions pour un club valide (orthographe + insultes)
        self._club = club

        # Licence
        if licence <= 0:
            raise ValueError("Le paramètre `licence` doit être strictement supérieur à `0`.")
        self._licence = licence

        # Tireur en équipe
        if in_team:

            # Score
            self._victories = None
            self._touches_scored = None
            self._touches_received = None

            # Mémoire
            self._opponents_encountered = None
            self._has_been_exempted = None

        # Tireur individuel
        else:

            # Score
            self._victories = 0.0
            self._touches_scored = 0
            self._touches_received = 0

            # Mémoire
            self._opponents_encountered = set()
            self._has_been_exempted = False

    @property
    def lastname(self) -> str:
        return self._lastname

    @lastname.setter
    def lastname(self, new_lastname: str) -> None:
        if len(new_lastname) == 0:
            raise ValueError("L'attribut `lastname` doit être non vide.")
        # TODO : conditions pour un nom valide (orthographe + insultes)
        self._lastname = new_lastname

    @property
    def firstname(self) -> str:
        return self._firstname

    @firstname.setter
    def firstname(self, new_firstname: str) -> None:
        if len(new_firstname) == 0:
            raise ValueError("L'attribut `firstname` doit être non vide.")
        self._firstname = new_firstname

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, new_age: int) -> None:
        if new_age <= 0:
            raise ValueError("L'attribut `age` doit être strictement supérieur à `0`.")
        self._age = new_age

    @property
    def gender(self) -> str:
        return self._gender

    @gender.setter
    def gender(self, new_gender: str) -> None:
        if new_gender not in frozenset({"H", "F", "A"}):
            raise ValueError("L'attribut `gender` doit être parmi `{'H', 'F', 'A'}`.")
        self._gender = new_gender

    @property
    def club(self) -> str:
        return self._club

    @club.setter
    def club(self, new_club: str) -> None:
        if len(new_club) == 0:
            raise ValueError("L'attribut `club` doit être non vide.")
        # TODO : conditions pour un club valide (orthographe + insultes)
        self._club = new_club

    @property
    def licence(self) -> int:
        return self._licence

    @licence.setter
    def licence(self, new_licence: int) -> None:
        if new_licence <= 0:
            raise ValueError("L'attribut `licence` doit être strictement supérieur à `0`.")
        self._licence = new_licence

    @property
    def victories(self) -> float | None:
        return self._victories

    @property
    def indicator(self) -> int | None:
        """
        Indice du tireur.
        """
        if isinstance(self._touches_scored, int) and isinstance(self._touches_received, int):
            return self._touches_scored - self._touches_received

    @property
    def opponents_encountered(self) -> set["Fencer"] | None:
        return self._opponents_encountered

    @property
    def has_been_exempted(self) -> bool | None:
        return self._has_been_exempted

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(lastname={self._lastname!r}, firstname={self._firstname!r}, "\
               f"age={self._age}, gender={self._gender!r}, club={self._club!r}, licence={self._licence}, "\
               f"in_team={self._victories is None})"

    def __eq__(self, other_fencer: "Fencer") -> bool:
        return (self._victories, self.indicator, self._touches_scored) == (other_fencer._victories, other_fencer.indicator, other_fencer._touches_scored)

    def __ne__(self, other_fencer: "Fencer") -> bool:
        return (self._victories, self.indicator, self._touches_scored) != (other_fencer._victories, other_fencer.indicator, other_fencer._touches_scored)

    def __lt__(self, other_fencer: "Fencer") -> bool:
        return (self._victories, self.indicator, self._touches_scored) < (other_fencer._victories, other_fencer.indicator, other_fencer._touches_scored)

    def __le__(self, other_fencer: "Fencer") -> bool:
        return (self._victories, self.indicator, self._touches_scored) <= (other_fencer._victories, other_fencer.indicator, other_fencer._touches_scored)

    def __gt__(self, other_fencer: "Fencer") -> bool:
        return (self._victories, self.indicator, self._touches_scored) > (other_fencer._victories, other_fencer.indicator, other_fencer._touches_scored)

    def __ge__(self, other_fencer: "Fencer") -> bool:
        return (self._victories, self.indicator, self._touches_scored) >= (other_fencer._victories, other_fencer.indicator, other_fencer._touches_scored)

    def win(self, opponent: "Fencer", *, self_touches: int, opponent_touches: int) -> None:
        """
        Ajoute une victoire au tireur sur son adversaire.

        :param opponent: Adversaire du tireur.
        :param self_touches: Touches portées par le tireur.
        :param opponent_touches: Touches portées par l'adversaire.
        """
        # Score du tireur
        self._victories += 1.0
        self._touches_scored += self_touches
        self._touches_received += opponent_touches

        # Mémoire du tireur
        self._opponents_encountered.add(opponent)

        # Score de l'adversaire
        opponent._touches_scored += opponent_touches
        opponent._touches_received += self_touches

        # Mémoire de l'adversaire
        opponent._opponents_encountered.add(self)

    def draw(self, opponent: "Fencer", touches: int) -> None:
        """
        Ajoute un match nul au tireur et son adversaire.

        :param opponent: Adversaire du tireur.
        :param touches: Touches portées par les tireurs.
        """
        # Score du tireur
        self._victories += 0.5
        self._touches_scored += touches
        self._touches_received += touches

        # Mémoire du tireur
        self._opponents_encountered.add(opponent)

        # Score de l'adversaire
        opponent._victories += 0.5
        opponent._touches_scored += touches
        opponent._touches_received += touches

        # Mémoire de l'adversaire
        opponent._opponents_encountered.add(self)

    def bye(self) -> None:
        """
        Ajoute une ronde exemptée au tireur.
        """
        # Score du tireur
        self._victories += 1.0

        # Mémoire du tireur
        self._has_been_exempted = True






'''
        # Équipe
        self.team = next(filter(lambda x: x.name.casefold() == team.casefold(), self.tournament.teams), None)
        if self.team is None:
            self.team = Team(team, self.tournament)
            self.tournament.add_team(self.team)

        # Club
        if self.tournament.licence_is_needed:
            self.club = next(filter(lambda x: x.name.casefold() == club.casefold(), self.tournament.clubs), None)
            if self.club is None:
                self.club = Club(club, self.tournament)
                self.tournament.add_club(self.club)
        else:
            self.club = None

    def as_table_entry(self) -> tuple[str, ...]:
        """Renvoie le tireur sous la forme d'une entrée de tableau.

        :return: L'entrée de tableau correspondant au tireur.
        """
        table_entry = [self.lastname, self.firstname, self.age, self.gender]
        if self.tournament.licence_is_needed:
            table_entry.extend((self.club.name, self.licence))
        table_entry.extend((str(self.victories),
                            str(self.touches_scored),
                            str(self.touches_received),
                            str(self.indicator)))
        return tuple(table_entry)
    def as_table_entry(self) -> tuple[str, ...]:
        """Renvoie le tireur sous la forme d'une entrée de tableau.

        :return: L'entrée de tableau correspondant au tireur.
        """
        table_entry = [self.lastname, self.firstname, self.age, self.gender]
        if self.tournament.licence_is_needed:
            table_entry.extend((self.club.name, self.licence))
        table_entry.extend(("", "", "", ""))
        return tuple(table_entry)
'''
