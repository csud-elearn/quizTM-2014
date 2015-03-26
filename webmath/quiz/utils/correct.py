class CorrectQuestion:
    def __init__(self, submit):
        # Définition des caractéristiques de base des corrections à afficher
        self.comment = submit.id_question.comment
        self.text = submit.id_question.text
        self.points = submit.id_question.points
        self.result = submit.result
        self.average = submit.id_question.average_result()

class CorrectSq(CorrectQuestion):
    def __init__(self, sqsubmit):
        CorrectQuestion.__init__(self, sqsubmit)
        
        self.submit = sqsubmit.text # Texte soumis par l'étudiant
        self.type = 0 # Détermine la manière d'afficher la question dans le template
        
        # Les réponses correctes sont placés dans une liste sous forme de chaînes de charactères
        self.l_correct = sqsubmit.get_corrections()
        
        # Comparaison par rapport à la correction
        if sqsubmit.correct():
            self.is_correct = True
            self.html_class = "success"
        else:
            self.is_correct = False
            self.html_class = "danger"

class CorrectQcm(CorrectQuestion):
    def __init__(self, qcmsubmit):
        CorrectQuestion.__init__(self, qcmsubmit)
        
        self.l_correct_choices = [] # Contient les objets CorrectChoice

####
#### Elements de liste déroulante à supprimer
####
        # Détermination du type de questions pour l'affichage dans le template
        if qcmsubmit.id_question.multi_answers:
            self.type = 1
        else:
            if qcmsubmit.id_question.show_list:
                self.type = 2
            else:
                self.type = 3
        
        # Choix possibles pour la question
        l_choices = qcmsubmit.id_question.get_choices()
        
        for choice in l_choices:
            self.l_correct_choices.append(CorrectChoice(choice, qcmsubmit))
            
####
#### Supprimer ce bloc (concerne les listes déroulantes) 
####
        # Pour une liste déroulante, seul le choix sélectionné est affiché
        if qcmsubmit.id_question.show_list:
            if qcmsubmit.id_selected:
                self.selected = qcmsubmit.id_selected.text
                if qcmsubmit.id_selected.valid:
                    self.html_class = "success"
                else:
                    self.html_class = "danger"
            else:
                self.selected = ""
                self.html_class = "danger"

class CorrectChoice:
    def __init__(self, choice, qcmsubmit):
        self.is_correct = choice.correct_submit(qcmsubmit) # Vérification du choix
        self.is_checked = choice.checked(qcmsubmit) # Vaut true si le choix est sélectionné
        self.text = choice.text # Texte du choix
        
        # Attributs pour l'affichage de la correction
        if self.is_correct:
            self.html_class = "success"
        else:
            self.html_class = "danger"
            
        if self.is_checked:
            self.attribute = "checked"
        else:
            self.attribute = ""