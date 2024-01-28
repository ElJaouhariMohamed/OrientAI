import pandas as pd

class CalculMoyenneFiliere:
    def __init__(self):
        self.coefficients = {
            "IID": {"Analyse 1": 7, "Algebre 1": 7, "Mecanique 1": 1,"Physique 1":1,"LC 1":2,"Informatique 1":7,"Physique 2":1, "Algebre 2": 7, "Analyse 2": 7,"Chimie":1,"Informatique 2":7,"LC 2":2,"Algebre 3":7,"Analyse 3":7,"Mecanique 2":1,"Electronique 1":1,"Informatique 3":7,"LC 3":2,"Analyse 4":7,"Math Appliquees":7,"Physique 4":1,"Physique 3":1,"Electronique 2":3,"LM":2},
            "GI":  {"Analyse 1": 5, "Algebre 1": 5, "Mecanique 1": 1,"Physique 1":1,"LC 1":2,"Informatique 1":7,"Physique 2":1, "Algebre 2": 5, "Analyse 2": 5,"Chimie":1,"Informatique 2":7,"LC 2":2,"Algebre 3":5,"Analyse 3":5,"Mecanique 2":1,"Electronique 1":1,"Informatique 3":7,"LC 3":2,"Analyse 4":5,"Math Appliquees":5,"Physique 4":1,"Physique 3":1,"Electronique 2":1,"LM":2},
            "GE":  {"Analyse 1": 1, "Algebre 1": 1, "Mecanique 1": 2,"Physique 1":4,"LC 1":2,"Informatique 1":2,"Physique 2":4, "Algebre 2": 1, "Analyse 2": 1,"Chimie":1,"Informatique 2":3,"LC 2":2,"Algebre 3":1,"Analyse 3":1,"Mecanique 2":2,"Electronique 1":4,"Informatique 3":3,"LC 3":2,"Analyse 4":1,"Math Appliquees":2,"Physique 4":3,"Physique 3":2,"Electronique 2":4,"LM":2},
            "GPEE":  {"Analyse 1": 2, "Algebre 1": 1, "Mecanique 1": 3,"Physique 1":2,"LC 1":1,"Informatique 1":1,"Physique 2":1, "Algebre 2": 3, "Analyse 2": 3,"Chimie":3,"Informatique 2":3,"LC 2":1,"Algebre 3":1,"Analyse 3":2,"Mecanique 2":3,"Electronique 1":2,"Informatique 3":2,"LC 3":1,"Analyse 4":2,"Math Appliquees":3,"Physique 4":1,"Physique 3":3,"Electronique 2":2,"LM":1},
            "IRIC":  {"Analyse 1": 2, "Algebre 1": 2, "Mecanique 1": 1,"Physique 1":1,"LC 1":2,"Informatique 1":3,"Physique 2":2, "Algebre 2": 2, "Analyse 2": 2,"Chimie":1,"Informatique 2":3,"LC 2":1,"Algebre 3":2,"Analyse 3":2,"Mecanique 2":1,"Electronique 1":2,"Informatique 3":3,"LC 3":1,"Analyse 4":2,"Math Appliquees":3,"Physique 4":4,"Physique 3":1,"Electronique 2":1,"LM":1}
        }

    def calculer_moyennes(self, notes):
        fnotes = {}
        for fil in self.coefficients.keys():
            fnotes[fil] = {}
            for mod in notes.keys():
                fnotes[fil][mod]= notes[mod]
        notes = fnotes
        moyennes_ponderees = {}
        for filiere, modules in self.coefficients.items():
            somme_notes = 0
            somme_coefficients = 0
            for module, coefficient in modules.items():
                note = notes[filiere][module]
                somme_notes += note * coefficient
                somme_coefficients += coefficient
            moyenne_ponderee = somme_notes / somme_coefficients
            moyennes_ponderees[filiere] = moyenne_ponderee  
            print(f"Moyenne pour la filière {filiere}: {moyenne_ponderee:.2f}")
        return moyennes_ponderees