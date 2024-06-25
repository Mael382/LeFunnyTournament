import re
from re import Pattern


class Score:
    """
    Classe représentant un score.

    :param int touches: Touches du score.
    :param str status: Statut du score : ``'V'`` (victoire), ``'D'`` (défaite) ou ``'N'`` (nul).
    """
    #: Touches du score
    _touches: int
    #: Statut du score : ``'V'`` (victoire), ``'D'`` (défaite) ou ``'N'`` (nul)
    _status: str | None

    def __init__(self, touches: int, status: str | None = None):
        """
        Initialise un nouveau score.
        """
        # Touches
        if touches < 0:
            raise ValueError("Le paramètre `touches` doit être supérieur ou égal à `0`.")
        self._touches = touches

        # Statut
        if isinstance(status, str) and (status not in frozenset({"V", "D", "N"})):
            raise ValueError("Le paramètre `status` doit être parmi `{'V', 'D', 'N'}`, ou `None`.")
        self._status = status

    @classmethod
    def from_str_score(cls, str_score: str) -> "Score":
        touches: int
        status: str | None = None
        if len(str_score) == 0:
            raise ValueError("Le paramètre `str_score` doit être non vide.")

        # Touches uniquement
        elif str_score.isdecimal():
            touches = int(str_score)
            if touches < 0:
                raise ValueError("Les touches du paramètre `str_score` doivent représenter un entier supérieur ou égal à `0`.")

        # Touches et statut
        elif str_score[0].isalpha() and str_score[1:].isdecimal():
            touches = int(str_score[1:])
            if touches < 0:
                raise ValueError("Les touches du paramètre `str_score` doivent représenter un entier supérieur ou égal à `0`.")
            status = str_score[0]
            if status not in frozenset({"V", "D", "N"}):
                raise ValueError("Le statut du paramètre `str_score` doit être parmi `{'V', 'D', 'N'}`.")

        # Paramètre ininterprétable
        else:
            raise ValueError("Le paramètre `str_score` n'est pas interprétable comme un score.")
        return cls(touches, status)

    @property
    def touches(self) -> int:
        return self._touches

    @touches.setter
    def touches(self, new_touches: int) -> None:
        if new_touches < 0:
            raise ValueError("L'attribut `touches` doit être supérieur ou égal à `0`.")
        self._touches = new_touches

    @property
    def status(self) -> str | None:
        return self._status

    @status.setter
    def status(self, new_status: str | None) -> None:
        if isinstance(new_status, str) and (new_status not in frozenset({"V", "D", "N"})):
            raise ValueError("L'attribut `status` doit être parmi `{'V', 'D', 'N'}`, ou `None`.")
        self._status = new_status

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(touches={self._touches}, status={self._status})"

    def __eq__(self, other_score: "Score") -> bool:
        return (self._touches, self._status) == (other_score._touches, other_score._status)

    def __ne__(self, other_score: "Score") -> bool:
        return (self._touches, self._status) != (other_score._touches, other_score._status)

    def __lt__(self, other_score: "Score") -> bool:
        if self._touches == other_score._touches:
            return (self._status, other_score._status) == ("D", "V")
        return self._touches < other_score._touches

    def __le__(self, other_score: "Score") -> bool:
        if self._touches == other_score._touches:
            return (self._status == other_score._status) or ((self._status, other_score._status) == ("D", "V"))
        return self._touches < other_score._touches

    def __gt__(self, other_score: "Score") -> bool:
        if self._touches == other_score._touches:
            return (self._status, other_score._status) == ("V", "D")
        return self._touches > other_score._touches

    def __ge__(self, other_score: "Score") -> bool:
        if self._touches == other_score._touches:
            return (self._status == other_score._status) or ((self._status, other_score._status) == ("V", "D"))
        return self._touches > other_score._touches
