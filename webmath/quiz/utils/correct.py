"""
Ensemble d'objets pour permettre un accès facilité aux données nécessaires à
l'affichage des corrections
"""

class CorrectQuestion:
    """
    Définit des raccourcis pour accéder aux attributs communs à tous les types
    de questions.
    """
    def __init__(self, submit):
        # Définition des caractéristiques de base des corrections à afficher
        self.comment = submit.id_question.comment
        self.text = submit.id_question.text
        self.points = submit.id_question.points
        self.result = submit.result
        self.average = submit.id_question.average_result()

class CorrectSq(CorrectQuestion):
    """
    Fournit des attributs spécifiques à la correction des questions à réponse courte.
    L'attribut ``type`` permet d'identifier dans le template le type de question
    dont il s'agit et de déterminer la manière d'afficher la correction.
    
    Pour une question à réponse courte, ``type`` vaut ``0``.
    """
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
    """
    Facilite l'affichage de la correction des questions à choix multiples par
    l'intermédiaire de raccourcis et instancie des objets de type :py:class:`CorrectChoice`.
    
    L'attribut ``type`` vaut ``1`` pour les QCM à réponses multiples, ``2`` pour
    les listes déroulantes et ``3`` pour les QCM à réponse unique.
    """
    def __init__(self, qcmsubmit):
        CorrectQuestion.__init__(self, qcmsubmit)
        
        self.l_correct_choices = [] # Contient les objets CorrectChoice

        # Détermination du type de questions pour l'affichage dans le template
        if qcmsubmit.id_question.multi_answers:
            self.type = 1
        else:
            self.type = 2
        
        # Choix possibles pour la question
        l_choices = qcmsubmit.id_question.get_choices()
        
        for choice in l_choices:
            self.l_correct_choices.append(CorrectChoice(choice, qcmsubmit))

class CorrectChoice:
    """
    Fournis des raccourcis pour accéder aux données des choix de QCM à corriger.
    Cette classe permet d'indiquer le texte à afficher avec le choix, de déterminer
    s'il a été coché et s'il est correct.
    """
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