from quiz.models import SqAnswer, QcmChoice, QcmSubmitMulti, QcmSubmitOne, SqSubmit

class CorrectQuiz:
    def __init__(self, completed):
        # Liste des réponses soumises aux questions simples du quiz
        l_submit_qs = list(SqSubmit.objects.filter(id_submitted_quiz=completed))
        # Liste des réponses aux qcm à réponses muliples du quiz
        l_submit_qcm_multi = list(QcmSubmitMulti.objects.filter(id_submitted_quiz=completed))
        # Liste des réponses aux qcm à réponses uniques
        l_submit_qcm_one = list(QcmSubmitOne.objects.filter(id_submitted_quiz=completed))
        
        # Liste vide qui contiendra les corrections
        self.l_corrections = [None] * len(l_submit_qs + l_submit_qcm_multi + l_submit_qcm_one)
        
        # Les corrections sont placés dans la liste et triées selon l'ordre d'apparition dans le quiz
        for submit in l_submit_qs:
            self.l_corrections[submit.id_question.number] = CorrectSq(submit)
            
        for submit in l_submit_qcm_multi:
            self.l_corrections[submit.id_question.number] = CorrectQcmMulti(submit)
            
        for submit in l_submit_qcm_one:
            self.l_corrections[submit.id_question.number] = CorrectQcmOne(submit)
            
    def get_corrections(self):
        """
        Renvoie la liste des corrections des questions
        """
        return self.l_corrections

class CorrectQuestion:
    def __init__(self, submit):
        # Définition des caractéristiques de base des corrections à afficher
        self.comment = submit.id_question.comment
        self.text = submit.id_question.text
        self.points = submit.id_question.points
        self.result = 0 # Nombre de points obtenus (incrémenté plus tard)

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
            self.result = self.points # Si la réponse est juste, tous les points sont obtenus
        else:
            self.is_correct = False

class CorrectQcm(CorrectQuestion):
    def __init__(self, qcmsubmit):
        CorrectQuestion.__init__(self, qcmsubmit)
        
        self.l_correct_choices = []
        
        # Détermination du type de questions pour l'affichage dans le template
        if qcmsubmit.id_question.multi_answers:
            self.type = 1
        else:
            if qcmsubmit.id_question.show_list:
                self.type = 2
            else:
                self.type = 3
        
        # Récupération des choix possibles dans la db
        l_choices = QcmChoice.objects.filter(id_question=qcmsubmit.id_question)
        
        for choice in l_choices:
            self.l_correct_choices.append(CorrectChoice(choice, qcmsubmit))
            
        self.calculate_result(qcmsubmit) # Comptabilisation des points
    
    def calculate_result(self, qcmsubmit):
        pass

            
class CorrectQcmMulti(CorrectQcm):
    def calculate_result(self, qcmsubmit):
        """
        Attributs les points en fonction des réponses
        """
        ppc = self.points / len(self.l_correct_choices) # Nombre de points par choix
        
        # Pour chaque case cochée correctement, des points sont ajoutés
        for choice in self.l_correct_choices:
            if choice.is_correct:
                self.result += ppc

class CorrectQcmOne(CorrectQcm):
    def calculate_result(self, qcmsubmit):
        """
        Attribue les points en fonction des réponses
        """
        # Si le choix sélectionné correspond au choix défini comme correct, tous les points sont attribués
        if qcmsubmit.id_selected: # Il se peut que l'utilisateur n'ait rien sélectionné
            if qcmsubmit.id_selected.valid:
                self.result = self.points

class CorrectChoice:
    def __init__(self, choice, qcmsubmit):
        self.is_correct = choice.correct(qcmsubmit) # Vérification du choix
        self.is_checked = choice.checked(qcmsubmit) # Vaut true si le choix est sélectionné
        self.text = choice.text # Texte du choix