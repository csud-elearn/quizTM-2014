from quiz.forms import CheckboxForm, RadioForm, SelectForm, TextForm
from quiz.models import SimpleQuestion, Qcm, SqSubmit, QcmChoice, QcmSubmitOne, QcmSubmitMulti, CompletedQuiz
from itertools import chain

class QuizForms:
    def __init__(self, quiz, data=None):
        self.quiz = quiz
            
        self.l_questions = quiz.get_questions()
        self.l_forms = []
        
        for question in self.l_questions:
            self.l_forms.append(question.create_form(data=data))
        
            
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
        
    def save_answers(self, user):
        """
        Sauvegarde dans la db les réponses soumises
        """
        completed = CompletedQuiz(id_quiz=self.quiz, id_user=user)
        completed.save()
        
        global_result = 0
        
        for question, form in zip(self.l_questions, self.l_forms):
            #Pour chaque question, on appelle la méthode avec en argument les données du formulaires correspondant et la référence vers la tentative de réponse
            submit = question.save_submit(form.cleaned_data, completed)
            global_result += submit.result # Ajout des points obtenus
            
        completed.result = global_result
        completed.save()
            
        return completed