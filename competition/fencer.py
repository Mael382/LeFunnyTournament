GENDERS: frozenset[str] = frozenset(("Masculin", "Féminin", "Autre"))


class Fencer:
    """
    Classe représentant un tireur.

    :param str lastname: Nom du tireur.
    :param str firstname: Prénom du tireur.
    :param int age: Âge du tireur.
    :param str gender: Sexe du tireur.
    :param str club: Club du tireur.
    :param int licence: Licence du tireur.
    :param bool has_team: Individualité du tireur.
    """
    #: Nom du tireur
    _lastname: str
    #: Prénom du tireur
    _firstname: str
    #: Sexe du tireur
    _gender: str
    #: Âge du tireur
    _age: int
    #: Club du tireur
    _club: str | None
    #: Licence du tireur
    _licence: int | None
    #: Victoires du tireur
    _victories: float | None
    #: Touches portées par le tireur
    _touches_scored: int | None
    #: Touches reçues par le tireur
    _touches_received: int | None
    #: Tireurs adverses rencontrés
    _opponents_encountered: set["Fencer"] | None
    #: Exemption du tireur
    _has_been_exempted: bool | None

    def __init__(self, lastname: str, firstname: str, gender: str, age: int, *,
                 club: str | None = None,
                 licence: int | None = None,
                 has_team: bool = False) -> None:
        """
        Initialise un nouveau tireur.
        """

        # Nom
        if len(lastname) == 0:
            raise ValueError("Le paramètre `lastname` doit être non vide.")
        self._lastname = lastname

        # Prénom
        if len(firstname) == 0:
            raise ValueError("Le paramètre `firstname` doit être non vide.")
        self._firstname = firstname

        # Sexe
        if gender not in GENDERS:
            raise ValueError("Le paramètre `gender` doit être parmi `{'Masculin', 'Féminin', 'Autre'}`.")
        self._gender = gender

        # Âge
        if age <= 0:
            raise ValueError("Le paramètre `age` doit être strictement supérieur à `0`.")
        self._age = age

        # Club
        if isinstance(club, str) and (len(club) == 0):
            raise ValueError("Le paramètre `club` doit être non vide, ou `None`.")
        self._club = club

        # Licence
        if isinstance(licence, int) and (licence <= 0):
            raise ValueError("Le paramètre `licence` doit être strictement supérieur à `0`, ou `None`.")
        self._licence = licence
        # TODO : Les licences commencent à 0 ou à 1 ?

        # Tireur individuel
        if not has_team:

            # Score
            self._victories = 0.0
            self._touches_scored = 0
            self._touches_received = 0

            # Mémoire
            self._opponents_encountered = set()
            self._has_been_exempted = False

        # Tireur en équipe
        else:

            # Score
            self._victories = None
            self._touches_scored = None
            self._touches_received = None

            # Mémoire
            self._opponents_encountered = None
            self._has_been_exempted = None

    @property
    def lastname(self) -> str:
        return self._lastname

    @property
    def firstname(self) -> str:
        return self._firstname

    @property
    def gender(self) -> str:
        return self._gender

    @gender.setter
    def gender(self, new_gender: str) -> None:
        if new_gender not in GENDERS:
            raise ValueError("L'attribut `gender` doit être parmi `{'Masculin', 'Féminin', 'Autre'}`.")
        self._gender = new_gender

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, new_age: int) -> None:
        if new_age <= 0:
            raise ValueError("L'attribut `age` doit être strictement supérieur à `0`.")
        self._age = new_age

    @property
    def club(self) -> str | None:
        return self._club

    @club.setter
    def club(self, new_club: str) -> None:
        if len(new_club) == 0:
            raise ValueError("L'attribut `club` doit être non vide.")
        self._club = new_club

    @property
    def licence(self) -> int | None:
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
    def touches_scored(self) -> int | None:
        return self._touches_scored

    @property
    def touches_received(self) -> int | None:
        return self._touches_received

    @property
    def opponents_encountered(self) -> set["Fencer"] | None:
        return self._opponents_encountered

    @property
    def has_been_exempted(self) -> bool | None:
        return self._has_been_exempted

    @property
    def name(self) -> tuple[str, str]:
        """
        Nom complet du tireur.
        """
        return self._lastname, self._firstname

    @property
    def is_licensed(self) -> bool:
        """
        Titularisation du tireur.
        """
        return (self._club is not None) and (self._licence is not None)
    # TODO : Y a-t-il un meilleur terme que "titularisation" ?

    @property
    def has_team(self) -> bool:
        """
        Individualité du tireur.
        """
        return (self._victories is None) or (self._touches_scored is None) or (self._touches_received is None) or (
                    self._opponents_encountered is None) or (self._has_been_exempted is None)

    @property
    def indicator(self) -> int | None:
        """
        Indice du tireur.
        """
        if not self.has_team:
            return self._touches_scored - self._touches_received

    @property
    def score(self) -> tuple[float, int, int] | None:
        """
        Score global du tireur.
        """
        if not self.has_team:
            return self._victories, self.indicator, self._touches_scored

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(lastname={self._lastname!r}, firstname={self._firstname!r}, "\
               f"gender={self._gender!r}, age={self._age}, club={self._club!r}, licence={self._licence}, "\
               f"has_team={self.has_team})"

    def __hash__(self) -> int:
        return hash((self._lastname, self._firstname))

    def __eq__(self, other_fencer: "Fencer") -> bool:
        return self.score == other_fencer.score

    def __ne__(self, other_fencer: "Fencer") -> bool:
        return self.score != other_fencer.score

    def __lt__(self, other_fencer: "Fencer") -> bool:
        return self.score < other_fencer.score

    def __le__(self, other_fencer: "Fencer") -> bool:
        return self.score <= other_fencer.score

    def __gt__(self, other_fencer: "Fencer") -> bool:
        return self.score > other_fencer.score

    def __ge__(self, other_fencer: "Fencer") -> bool:
        return self.score >= other_fencer.score

    def win(self, opponent: "Fencer", *,
            self_touches: int, opponent_touches: int) -> None:
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
        if opponent not in self._opponents_encountered:
            self._opponents_encountered.add(opponent)

        # Score de l'adversaire
        opponent._touches_scored += opponent_touches
        opponent._touches_received += self_touches

        # Mémoire de l'adversaire
        opponent._opponents_encountered.add(self)

    def draw(self, opponent: "Fencer", *,
             touches: int) -> None:
        """
        Ajoute un match nul au tireur et son adversaire.

        :param opponent: Adversaire du tireur.
        :param touches: Touches portées par les tireurs, individuellement.
        """
        # Score du tireur
        self._victories += 0.5
        self._touches_scored += touches
        self._touches_received += touches

        # Mémoire du tireur
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
        Ajoute une ronde exemptée au tireur.
        """
        # Score du tireur
        self._victories += 1.0

        # Mémoire du tireur
        self._has_been_exempted = True
