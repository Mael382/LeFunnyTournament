import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mb
import tkinter.colorchooser as cc

from itertools import groupby
import random
from PIL import Image, ImageDraw, ImageTk, ImageFont


class RoundProperties(tk.Toplevel):
    """...
    """

    def __init__(self, parent: ...) -> None:
        """...

        :param parent:
        """
        # ...  # RESOLVE
        super().__init__(parent)
        self.parent = parent

        # ...
        self.pairings = []
        self.has_bye = []

        # ...
        self.score_label = tk.Label(self, text="Entrer les scores pour la prochaine ronde :")
        self.score_label.pack()
        self.score_entry = tk.Entry(self)
        self.score_entry.pack()
        self.submit_button = tk.Button(self, text="Envoyer Scores", command=self.submit_scores)
        self.submit_button.pack()

        # Fenêtre
        self.title("Nouvelle ronde")
        self.iconbitmap(r"assets\images\ico\LeFunnyIcon.ico")
        # self.geometry("600x600+70+70")
        # self.resizable(False, False)

        # ...
        self.__create_header()
        self.__create_pairs()
        # self.__create_remains()

    def __create_header(self) -> None:
        """...
        """
        # Style
        # NEEDS TTK

        # Label
        label = tk.Label(self, text=f"Ronde n°{self.parent.rounds_id}")

        # Positionnement
        label.pack()

    def __create_pairs(self) -> None:
        """...
        """
        # Style
        # NEEDS TTK

        def matching(fencers: ...):
            pairings, has_bye = [], []
            groups = []
            for _, group in groupby(sorted(fencers, key=lambda x: x["wins"], reverse=True), key=lambda x: x["wins"]):
                groups.append(list(group))
            for group_id, group in enumerate(groups):
                group.sort(key=lambda x: (x["wins"], x["indice"], x["score"]), reverse=True)
                strong, weak = group[:len(group)//2], group[len(group)//2:]
                for fencer in strong:
                    i = strong.index(fencer)
                    opponents = weak[i:] + weak[:i]  # TO CHANGE BY A DISTANCE WITH ALL OPPONENTS
                    for opponent in opponents:
                        if fencer["id"] not in opponent["memory"]:
                            pairings.append((fencer, opponent))
                            strong.pop(i)
                            weak.remove(opponent)
                            group.remove(fencer)
                            group.remove(opponent)
                            break
                # NOT NEEDED WHEN DISTANCE WITH ALL OPPONENTS
                for fencer in weak:
                    i = weak.index(fencer)
                    opponents = strong[i:] + strong[:i]
                    for opponent in opponents:
                        if fencer["id"] not in opponent["memory"]:
                            pairings.append((fencer, opponent))
                            weak.pop(i)
                            strong.remove(opponent)
                            group.remove(fencer)
                            group.remove(opponent)
                            break
                for fencer in group:
                    if group_id < len(groups) - 1:
                        groups[group_id+1].append(fencer)
                    else:
                        has_bye.append(fencer)
            print(pairings)
            print(has_bye)

            return pairings, has_bye

        pairs, has_bye = matching(self.parent.tournament_fencers)
        self.pairings = [(d[0]["id"], d[1]["id"]) for d in pairs]
        self.has_bye = [d["id"] for d in has_bye]

        pairings_listbox = tk.Listbox(self, width=50)
        pairings_listbox.pack()
        pairings_listbox.delete(0, tk.END)
        for pair in pairs:
            participant1, participant2 = pair
            pairings_listbox.insert(tk.END, f"{participant1["name"]} vs {participant2["name"]}")
        for participant in has_bye:
            pairings_listbox.insert(tk.END, f"{participant["name"]} est exempté")

    def __create_remains(self) -> None:
        score_label = tk.Label(self, text="Entrer les scores pour la prochaine ronde:")
        score_label.pack()
        score_entry = tk.Entry(self)
        score_entry.pack()
        submit_button = tk.Button(self, text="Envoyer Scores", command=self.submit_scores)
        submit_button.pack()

    def submit_scores(self):
        matchs = self.score_entry.get().split()
        if len(matchs) != len(self.pairings):
            mb.showerror("Error", "Number of scores entered does not match the number of pairings.")
            return

        for i, ids in enumerate(self.pairings):
            wis1, wis2 = matchs[i].split("#")
            w1, i1, s1 = wis1.split(",")
            w2, i2, s2 = wis2.split(",")
            for j, d in enumerate(self.parent.tournament_fencers):
                a_done, b_done = False, False
                if d["id"] == ids[0]:
                    d["wins"] += int(w1)
                    d["indice"] += int(i1)
                    d["score"] += int(s1)
                    d["memory"].add(ids[1])
                    a_done = True
                elif d["id"] == ids[1]:
                    d["wins"] += int(w2)
                    d["indice"] += int(i2)
                    d["score"] += int(s2)
                    d["memory"].add(ids[0])
                    b_done = True
                if a_done and b_done:
                    break

        for ids in self.has_bye:
            for j, d in enumerate(self.parent.tournament_fencers):
                if d["id"] == ids:
                    d["wins"] += 1
                    break

        self.parent.rounds_id += 1
        self.score_entry.delete(0, tk.END)
        mb.showinfo("Success", f"Scores envoyés avec succès pour la ronde n°{self.parent.rounds_id-1}")

        print(self.parent.tournament_fencers)
        self.destroy()











































































