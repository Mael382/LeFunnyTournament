from collections import defaultdict

from itertools import combinations

from utils.enumit import reversed_enumerate, sorted_iterate
from utils.matching import max_weighted_matching

from assault.match import Match

from competition.fencer import Fencer
from competition.team import Team


class Round:
    """
    Classe représentant une ronde.

    :param int number: Numéro de la ronde.
    :param int max_score: Score maximum des matchs.
    :param bool draw_is_allowed: Autorisation du match nul.
    :param set[Fencer]|set[Team] participants: Tireurs/Équipes de la ronde.
    """
    #: Numéro de la ronde
    _number: int
    #: Score maximum des matchs
    _max_score: int
    #: Autorisation des matchs nuls
    _draw_is_allowed: bool
    #: Tireurs/Équipes de la ronde.
    _participants: set[Fencer] | set[Team]

    def __init__(self, number: int, max_score: int, draw_is_allowed: bool,
                 participants: set[Fencer] | set[Team]) -> None:
        """
        Initialise une nouvelle ronde.
        """
        # Numéro
        self._number = number

        # Score maximum
        if max_score <= 0:
            raise ValueError("Le paramètre `max_score` doit être strictement supérieur à `0`.")
        self._max_score = max_score

        # Autorisation du résultat nul
        self._draw_is_allowed = draw_is_allowed

        # Tireurs/Équipes
        self._participants = participants

    @property
    def participants(self) -> set[Fencer] | set[Team]:
        return self._participants

    @participants.setter
    def participants(self, new_participants: set[Fencer] | set[Team]) -> None:
        self._participants = new_participants

    @property
    def matches(self) -> list[Match]:
        """
        Matchs de la ronde
        """

        def matching(participants: defaultdict[float, list[Fencer]] | defaultdict[float, list[Team]]) -> tuple[set[tuple[Fencer, Fencer]] | set[tuple[Team, Team]], bool]:
            """
            ...

            :param participants: ...
            :return: ...
            """
            pairs: set[tuple[Fencer, Fencer, float]] | set[tuple[Team, Team, float]] = set()
            half: int = len(participants) // 2
            for (i, participant1), (j, participant2) in combinations(enumerate(participants), 2):
                if (participant2 not in participant1.opponents_encountered) and (participant1 not in participant2.opponents_encountered):
                    distance: int = abs(i - j - half)
                    if (i < half <= j) or (i >= half > j):
                        weight: float = 1 / (distance + 1) + 1.0
                    else:
                        weight: float = 1 / (distance + 1)
                    pairs.add((participant1, participant2, weight))
            pairing: set[tuple[Fencer, Fencer]] | set[tuple[Team, Team]] = max_weighted_matching(participants, pairs)
            return pairing, len(pairing) == half

        # Classement
        sorted_participants: list[Fencer] | list[Team] = sorted(self._participants, reverse=True)

        # Participant exempté
        exempted: Fencer | Team | None = None
        if len(sorted_participants) % 2 != 0:
            for i, participant in reversed_enumerate(sorted_participants):
                if not participant.has_been_exempted:
                    exempted = sorted_participants.pop(i)

        # Groupement
        groups: defaultdict[float, list[Fencer]] | defaultdict[float, list[Team]] = defaultdict(list)
        for participant in sorted_participants:
            groups[participant.victories].append(participant)

        # Regroupement
        victories: list[float] = sorted(groups.keys(), reverse=True)
        for i, victory in enumerate(victories):
            group: list[Fencer] | list[Team] = groups[victory]
            if len(group) % 2 != 0:
                groups[victories[i + 1]].insert(0, group.pop())
        # TODO : régler les problèmes potentiels

        # Appariement
        dict_couples: dict[list[float], set[tuple[Fencer, Fencer]]] | dict[list[float], set[tuple[Team, Team]]] = dict()
        wins: list[float] = list()
        group: list[Fencer] | list[Team] = list()
        coupling_is_total: bool = True
        for victory in victories:
            wins.append(victory)
            group.extend(groups[victory])
            coupling_group: set[tuple[Fencer, Fencer]] | set[tuple[Team, Team]]
            coupling_group, coupling_is_total = matching(group)
            if coupling_is_total:
                dict_couples[wins] = coupling_group
                wins = list()
                group = list()

        # Ré-appariement
        if not coupling_is_total:
            for list_victory in sorted_iterate(dict_couples.keys()):
                dict_couples.pop(list_victory)
                wins.extend(list_victory)
                for victory in list_victory:
                    group.extend(groups[victory])
                coupling_group, coupling_is_total = matching(group)
                if coupling_is_total:
                    dict_couples[wins] = coupling_group
                    break

        # Matchs
        matches: list[Match] = list()
        for couples in dict_couples.values():
            for couple in couples:
                matches.append(Match(self._max_score, self._draw_is_allowed,
                                     participant1=couple[0], participant2=couple[1]))
        if exempted:
            matches.append(Match(self._max_score, self._draw_is_allowed,
                                 participant1=exempted))

        return matches
