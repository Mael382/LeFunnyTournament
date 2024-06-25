from assault.score import Score

from competition.fencer import Fencer
from competition.team import Team


class Match:
    """
    Classe représentant un match.

    :param int max_score: Score maximum du match.
    :param bool draw_is_allowed: Autorisation du match nul.
    :param Fencer|Team|None participant1: Premier.ère tireur/équipe du match.
    :param Score|None score1: Score du premier.ère tireur/équipe.
    :param Fencer|Team|None participant2: Second.e tireur/équipe du match.
    :param Score|None score2: Score du second.e tireur/équipe.
    """
    #: Score maximum du match
    _max_score: int
    #: Autorisation du match nul
    _draw_is_allowed: bool
    #: Premier.ère tireur/équipe du match
    _participant1: Fencer | Team | None
    #: Score du premier.ère tireur/équipe
    _score1: Score | None
    #: Second.e tireur/équipe du match
    _participant2: Fencer | Team | None
    #: Score du second.e tireur/équipe
    _score2: Score | None

    def __init__(self, max_score: int, draw_is_allowed: bool, *,
                 participant1: Fencer | Team | None = None, score1: Score | None = None,
                 participant2: Fencer | Team | None = None, score2: Score | None = None) -> None:
        """
        Initialise un nouveau match.
        """
        # Score maximum
        if max_score <= 0:
            raise ValueError("Le paramètre `max_score` doit être strictement supérieur à `0`.")
        self._max_score = max_score

        # Autorisation du résultat nul
        self._draw_is_allowed = draw_is_allowed

        # Premier.ère tireur/équipe
        self._participant1: Fencer | Team | None = participant1
        self._score1: Score | None = score1

        # Second.e tireur/équipe
        if (isinstance(participant1, Fencer) and isinstance(participant2, Team)) or (isinstance(participant1, Team) and isinstance(participant2, Fencer)):
            raise TypeError("Les paramètres `participant1` et `participant2` doivent être des instances de la même classe `Fencer` ou `Team`, ou `None`.")
        self._participant2: Fencer | Team | None = participant2
        self._score2: Score | None = score2

    @property
    def participant1(self) -> Fencer | Team | None:
        return self._participant1

    @participant1.setter
    def participant1(self, new_participant: Fencer | Team | None) -> None:
        if isinstance(self._participant2, Fencer) and isinstance(new_participant, Team):
            raise TypeError("L'attribut `participant1` doit être une instance de `Fencer`, ou `None`.")
        elif isinstance(self._participant2, Team) and isinstance(new_participant, Fencer):
            raise TypeError("L'attribut `participant1` doit être une instance de `Team`, ou `None`.")
        self._participant1 = new_participant

    @property
    def score1(self) -> Score | None:
        return self._score1

    @score1.setter
    def score1(self, new_score: Score | None) -> None:
        self._score1 = new_score

    @property
    def participant2(self) -> Fencer | Team | None:
        return self._participant2

    @participant2.setter
    def participant2(self, new_participant: Fencer | Team | None) -> None:
        if isinstance(self._participant1, Fencer) and isinstance(new_participant, Team):
            raise TypeError("L'attribut `participant2` doit être une instance de `Fencer`, ou `None`.")
        elif isinstance(self._participant1, Team) and isinstance(new_participant, Fencer):
            raise TypeError("L'attribut `participant2` doit être une instance de `Team`, ou `None`.")
        self._participant2 = new_participant

    @property
    def score2(self) -> Score | None:
        return self._score2

    @score2.setter
    def score2(self, new_score: Score | None) -> None:
        self._score2 = new_score

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(max_score={self._max_score}, draw_is_allowed={self._draw_is_allowed}, "\
               f"participant1={self._participant1}, participant2={self._participant2}, score1={self._score1}, "\
               f"score2={self._score2})"

    def validate(self) -> None:
        """
        Valide le match et applique son résultat aux tireurs/équipes.
        """
        # Un.e tireur/équipe (exempté.e)
        if self._participant1 and (self._participant2 is None):
            self._participant1.bye()
        elif self._participant2 and (self._participant1 is None):
            self._participant2.bye()

        # Deux tireurs/équipes (victoire/défaite ou match nul)
        elif self._participant1 and self._participant2:
            if self._score1 > self._score2:
                self._participant1.win(self._participant2,
                                       self_touches=self._score1.touches, opponent_touches=self._score2.touches)
            elif self._score1 < self._score2:
                self._participant2.win(self._participant1,
                                       self_touches=self._score2.touches, opponent_touches=self._score1.touches)
            elif self._score1 == self._score2:
                self._participant1.draw(self._participant2, touches=self._score1.touches)
