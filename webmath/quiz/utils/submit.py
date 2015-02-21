from quiz.forms import CheckboxForm, RadioForm, SelectForm, TextForm
from quiz.models import SimpleQuestion, Qcm, SqSubmit, QcmChoice, QcmSubmitOne, QcmSubmitMulti, CompletedQuiz
from itertools import chain

class QuizForms:
    def __init__(self, quiz, data=None):
        self.quiz = quiz
        
        #On récupère toutes les questions dans la db et on les met dans une seule liste
        queryset = list(SimpleQuestion.objects.filter(id_quiz=quiz)) + list(Qcm.objects.filter(id_quiz=quiz))
        
        self.l_questions = [None] * len(queryset) #Construction d'une liste d'éléments vide qui contiendra les formulaires
        self.l_forms = [None] * len(queryset)
        
        #On classe les questions par ordre d'apparition avec les formulaires correspondants
        for question in queryset:
            self.l_questions[question.number] = question
            self.l_forms[question.number] = question.create_form(data=data)
        
            
    def get_forms(self):
        """
        Renvoie la liste des formulaires
        """
        return self.l_forms
        
    def are_valid(self):
        """
        Renvoie True si tous les formulaires sont valides
        """
        valid = True
        for form in self.l_forms:
            if not form.is_valid():
                valid = False
        
        return valid
        
    def save_answers(self):
        """
        Sauvegarde dans la db les réponses soumises
        """
        completed = CompletedQuiz(id_quiz=self.quiz)
        completed.save()
        
        for question, form in zip(self.l_questions, self.l_forms):
            #Pour chaque question, on appelle la méthode avec en argument les données du formulaires correspondant et la référence vers la tentative de réponse
            question.save_submit(form.cleaned_data, completed)