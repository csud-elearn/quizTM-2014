from django.db import models
from django.contrib.auth.models import User
from common.models import Teacher
import quiz.forms as forms

# Create your models here.

class Quiz(models.Model): #Infos générales sur le quiz
    title = models.CharField(max_length=100)
    points = models.FloatField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=1000) #Format texte du quiz
    id_teacher = models.ForeignKey('common.Teacher')
    #id_chapter = models.ForeignKey('teachers.Chapter')
    
    def __str__(self):
        return self.title
        
    def length(self):
        return len(self.get_questions())
        
    def get_questions(self):
        """
        Renvoie la liste des questions du quiz dans l'ordre
        """
        # Liste des questions non triée
        l_questions = list(SimpleQuestion.objects.filter(id_quiz=self)) + list(Qcm.objects.filter(id_quiz=self))
        
        ordered_questions = [None] * len(l_questions) # Création d'une liste vide
        
        # Chaque question est placée à sa place dans la liste triée
        for question in l_questions:
            ordered_questions[question.number] = question
            
        return ordered_questions
        
    def average_result(self):
        """
        Renvoie le nombre moyen de points obtenus pour le quiz
        """
        total_result = 0
        l_completed = CompletedQuiz.objects.filter(id_quiz=self)
        
        if len(l_completed) > 0: # Si il n'y a aucune résolution, impossible de diviser par zéro
            for c in l_completed:
                total_result += c.result
                
            average = total_result / len(l_completed)
            
            return round(average, 2)
            
        else:
            return "--"
        
class QuizDraft(models.Model): #Brouillon contenant le code d'un quiz
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=1000)
    id_teacher = models.ForeignKey('common.Teacher')
    
    def __str__(self):
        return self.title
    
class CompletedQuiz(models.Model): #Tentative de réponse au quiz par un élève
    submit_date = models.DateTimeField(auto_now_add=True)
    result = models.FloatField(default=0)
    id_quiz = models.ForeignKey(Quiz) #Relation avec le quiz complété
    id_user = models.ForeignKey(User)
    
    def correct(self):
        """
        Corrige les questions soumises
        """
        questions_types = [QcmSubmitMulti, QcmSubmitOne, SqSubmit]
        
        for type_ in questions_types:
            l_submits = type_.objects.filter(id_submitted_quiz=self)
            
            for submit in l_submits:
                submit.correct()
                
    def get_questions_submits(self):
        """
        Renvoie la liste des réponses soumises pour chaque question
        """
        # Liste des réponses non triées
        l_submits = list(SqSubmit.objects.filter(id_submitted_quiz=self))\
        + list(QcmSubmitOne.objects.filter(id_submitted_quiz=self))\
        + list(QcmSubmitMulti.objects.filter(id_submitted_quiz=self))
        
        ordered_submits = [None] * len(l_submits)
        
        # Chaque réponse est placée au bon endroit dans la liste
        for submit in l_submits:
            ordered_submits[submit.id_question.number] = submit
            
        return ordered_submits

#    
#Classes abstraites
#

class QuizQuestion(models.Model): #Classe abstraite dont héritent toutes les questions
    text = models.CharField(max_length=200) #Énoncé
    comment = models.CharField(max_length=200, blank=True) #Commentaire affiché lors de la correction
    points = models.FloatField(default=1)
    number = models.IntegerField() #Ordre de la question dans le quiz
    id_quiz = models.ForeignKey(Quiz)
    
    class Meta:
        abstract = True
        
    def __str__(self):
        return self.text

#
#Tables concernant les questions simples
#
        
class SimpleQuestion(QuizQuestion):
    def create_form(self, *args, **kwargs):
        """
        Retourne un formulaire pour répondre à la question
        """
        return forms.TextForm(question=self, prefix=self.number, *args, **kwargs)
        
    def save_submit(self, data, completed):
        submit = SqSubmit(text=data['answer'], id_question=self, id_submitted_quiz=completed)
        
        # Enregistrement du résultat (pour les statistiques)
        submit.result = self.save_result(submit)
        submit.save()
        
        return submit
        
    def save_result(self, submit):
        """
        Comptabilise et enregistre les points pour la réponse soumise submit
        """
        result = 0
        if submit.correct():
            result = self.points
            
        return result
        
    def average_result(self):
        """
        Renvoie le nombre moyen de points obtenus pour la question
        """
        l_submit = SqSubmit.objects.filter(id_question=self)
        total_points = 0 # Points cumulés de toutes les résolutions
        
        if len(l_submit) > 0:
            for s in l_submit:
                total_points += s.result
                
            average = total_points / len(l_submit)
            
            return round(average, 2)
            
        else:
            return "--"

class SqAnswer(models.Model): #Les réponses correctes
    text = models.CharField(max_length=50)
    id_question = models.ForeignKey(SimpleQuestion) #Relation vers la question
    
    def __str__(self):
        return self.text

class SqSubmit(models.Model): #Réponse soumise par un élève
    text = models.CharField(max_length=50)
    result = models.FloatField(default=0)
    id_question = models.ForeignKey(SimpleQuestion) #Relation vers la question à laquelle l'élève a répondu
    id_submitted_quiz = models.ForeignKey(CompletedQuiz) #Relation vers la tentative
    
    def __str__(self):
        return self.text
        
    def get_corrections(self):
        """
        Renvoie la liste des réponses correctes à la question
        """
        # Récupération des corrections de la question
        l_sq_answer = SqAnswer.objects.filter(id_question=self.id_question)
        
        # Les réponses correctes (string) sont placés dans une liste
        l_correct_text = [answer.text for answer in l_sq_answer]
        
        return l_correct_text
        
    def correct(self):
        """
        Détermine si la réponse soumise est correcte
        """
        if self.text in self.get_corrections():
            return True
        else:
            return False

# 
#Tables concernant les QCM
#

class Qcm(QuizQuestion):
    multi_answers = models.BooleanField() #True si il est possible de cocher plusieurs choix
    show_list = models.BooleanField() #True si les choix sont affichés sous forme de liste déroulante
    
    def create_form(self, *args, **kwargs):
        """
        Retourne un formulaire pour répondre à la question
        """
        if self.multi_answers:
            Form = forms.CheckboxForm
        elif self.show_list:
            Form = forms.SelectForm
        else:
            Form = forms.RadioForm
            
        return Form(queryset=QcmChoice.objects.filter(id_question=self), prefix=self.number, question=self, *args, **kwargs)
        
    def save_submit(self, data, completed):
        """
        Enregistre les réponses soumises à la question
        """
        if self.multi_answers:
            Model = QcmSubmitMulti
        else:
            Model = QcmSubmitOne
            
        submit = Model(id_submitted_quiz=completed, id_question=self)
        
        if self.multi_answers:
            submit.save() #Comme il peut s'agir d'une relation many to many, il faut sauvegarder et ajouter la relation après
        submit.id_selected=data['answer']
        
        submit.result = self.save_result(submit)
        submit.save()
        
        return submit
        
    def save_result(self, submit):
        """
        Comptabilise et enregistre les points pour la réponse soumise submit
        """
        result = 0
        
        if self.multi_answers:
            l_choices = QcmChoice.objects.filter(id_question=self) # Récupération des choix de la question
            ppc = self.points / len(l_choices) # Nombre de points attribués par choix correct
            
            # À chaque option correctement cochée, on ajoute les points au résultat
            for c in l_choices:
                if c.correct(submit):
                    result += ppc
        else:
            if submit.id_selected:
                if submit.id_selected.valid:
                    result = self.points
        
        return result
        
    def average_result(self):
        """
        Renvoie le nombre moyen de points obtenus pour la question
        """
        if self.multi_answers:
            model = QcmSubmitMulti
        else:
            model = QcmSubmitOne
        
        l_submit = model.objects.filter(id_question=self)
        total_points = 0 # Points cumulés de toutes les résolutions
        
        if len(l_submit) > 0:
            for s in l_submit:
                total_points += s.result
                
            average = total_points / len(l_submit)
            return round(average, 2)
            
        else:
            return "--"
    
class QcmChoice(models.Model): #Choix affichés pour un QCM
    text = models.CharField(max_length=50)
    valid = models.BooleanField() #Vaut True si la case doit être cochée
    id_question = models.ForeignKey(Qcm)
    
    def __str__(self):
        return self.text
        
    def correct(self, qcmsubmit):
        """
        Détermine si la réponse soumise qcmsubmit est correcte ou non
        """
        # Si le choix est sélectionnée
        if self.checked(qcmsubmit):
            if self.valid: # Le choix est défini comme valide
                return True
            else: # Le choix est défini comme invalide
                return False
        # Si le choix n'est pas sélectionné
        else: # Le choix n'est pas sélectionné
            if self.valid: # Le choix est défini comme valide
                return False
            else: # Le choix est défini comme invalide
                return True
                
    def checked(self, qcmsubmit):
        """
        Détermine si le choix a été sélectionné ou non
        """
        # Si la sélection peut comporter plusieurs choix
        if self.id_question.multi_answers:
            if qcmsubmit.id_selected: # Il faut s'assurer qu'au moins un choix soit coché
                # Récupération des données de la relation M to M
                selected = qcmsubmit.id_selected.all()
                if self in selected:
                    return True
                else:
                    return False
            else:
                return False
        # Si un seul élément peut être sélectionné
        else:
            # Récupération du choix de la foreign key
            selected = qcmsubmit.id_selected
            if self == selected:
                return True
            else:
                return False
        
class QcmSubmit(models.Model):
    result = models.FloatField(default=0)
    id_submitted_quiz = models.ForeignKey(CompletedQuiz) #Relation vers la tentative
    id_question = models.ForeignKey(Qcm) #Relation vers la question : utile si aucune case est cochée
        
    class Meta:
            abstract = True
        
class QcmSubmitOne(QcmSubmit):
    id_selected = models.ForeignKey(QcmChoice, null=True) #Choix sélectionnés par l'élève dans un QCM à bouton radio ou liste déroulante
    
class QcmSubmitMulti(QcmSubmit): 
    id_selected = models.ManyToManyField(QcmChoice, null=True) #Choix sélectionnés par l'élève dans un QCM à cases à cocher