from django.db import models
import quiz.forms as forms

# Create your models here.

class Quiz(models.Model): #Infos générales sur le quiz
    title = models.CharField(max_length=100)
    creation_date = models.DateTimeField(auto_now_add=True)
    code = models.CharField(max_length=1000) #Format texte du quiz
    #id_prof = models.ForeignKey('teachers.Teacher')
    #id_chapter = models.ForeignKey('teachers.Chapter')
    
    def __str__(self):
        return self.title
        
    def length(self):
        return len(SimpleQuestion.objects.filter(id_quiz=self)) + len(Qcm.objects.filter(id_quiz=self))
        
class QuizDraft(models.Model): #Brouillon contenant le code d'un quiz
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=1000)
    #id_prof
    
    def __str__(self):
        return self.title
    
class CompletedQuiz(models.Model): #Tentative de réponse au quiz par un élève
    submit_date = models.DateTimeField(auto_now_add=True)
    id_quiz = models.ForeignKey(Quiz) #Relation avec le quiz complété
    #id_student = models.ForeignKey('students.Student')
    
    def correct(self):
        """
        Corrige les questions soumises
        """
        questions_types = [QcmSubmitMulti, QcmSubmitOne, SqSubmit]
        
        for type_ in questions_types:
            l_submits = type_.objects.filter(id_submitted_quiz=self)
            
            for submit in l_submits:
                submit.correct()

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
        return forms.TextForm(text=self.text, prefix=self.number, *args, **kwargs)
        
    def save_submit(self, data, completed):
        SqSubmit(text=data['answer'], id_question=self, id_submitted_quiz=completed).save()

class SqAnswer(models.Model): #Les réponses correctes
    text = models.CharField(max_length=50)
    id_question = models.ForeignKey(SimpleQuestion) #Relation vers la question
    
    def __str__(self):
        return self.text

class SqSubmit(models.Model): #Réponse soumise par un élève
    text = models.CharField(max_length=50)
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
            
        return Form(queryset=QcmChoice.objects.filter(id_qcm=self), prefix=self.number, text=self.text, *args, **kwargs)
        
    def save_submit(self, data, completed):
        """
        Enregistre les réponses soumises à la question
        """
        if self.multi_answers:
            Model = QcmSubmitMulti
        else:
            Model = QcmSubmitOne
            
        submit = Model(id_submitted_quiz=completed, id_qcm=self)
        
        if self.multi_answers:
            submit.save() #Comme il peut s'agir d'une relation many to many, il faut sauvegarder et ajouter la relation après
        submit.id_selected=data['answer']
        submit.save()
    
class QcmChoice(models.Model): #Choix affichés pour un QCM
    text = models.CharField(max_length=50)
    valid = models.BooleanField() #Vaut True si la case doit être cochée
    id_qcm = models.ForeignKey(Qcm)
    
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
        if self.id_qcm.multi_answers:
            # Récupération des données de la relation M to M
            selected = qcmsubmit.id_selected.all()
            if self in selected:
                return True
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
    id_submitted_quiz = models.ForeignKey(CompletedQuiz) #Relation vers la tentative
    id_qcm = models.ForeignKey(Qcm) #Relation vers la question : utile si aucune case est cochée
        
    class Meta:
            abstract = True
        
class QcmSubmitOne(QcmSubmit):
    id_selected = models.ForeignKey(QcmChoice, null=True) #Choix sélectionnés par l'élève dans un QCM à bouton radio ou liste déroulante
    
class QcmSubmitMulti(QcmSubmit): 
    id_selected = models.ManyToManyField(QcmChoice, null=True) #Choix sélectionnés par l'élève dans un QCM à cases à cocher