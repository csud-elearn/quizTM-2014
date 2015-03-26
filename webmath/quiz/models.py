from django.db import models
from django.contrib.auth.models import User
from common.models import Teacher
import quiz.forms as forms
from quiz.utils.correct import *

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
        """
        Retourne le nombre de questions qui composent le quiz.
        """
        return len(self.get_questions())
        
    def get_questions(self):
        """
        Récupère la liste de toutes les questions du quiz et les trie dans l'ordre
        d'apparition dans le quiz.
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
        Récupère dans la base de données toutes les résolutions se rattachant
        au quiz en question puis calcule la moyenne des résultats obtenus sur la base
        du résultat de chaque élève et le nombre de résolutions envoyées.
        """
        total_result = 0 # Somme des points obtenus pour toutes les résolutions
        # Récupération des résolutions concernant le quiz dans la base de donnnées
        l_completed = CompletedQuiz.objects.filter(id_quiz=self)
        
        if len(l_completed) > 0: # Si il n'y a aucune résolution, impossible de diviser par zéro
            for c in l_completed:
                total_result += c.result
                
            # Moyenne arithmétique
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
    
    # def correct(self):
    #     """
    #     Corrige les questions soumises
    #     """
    #     for submit in self.get_questions_submits():
    #         submit.correct()
                
    def get_questions_submits(self):
        """
        Renvoie la liste des entrées des tables ``SqSubmit``, ``QcmSubmitOne`` et
        ``QcmSubmitMulti`` correspondant à chacune des questions du quiz auquel
        l'élève a répondu. Cette liste est triée selon l'ordre d'apparition des
        questions correspondant aux entrées concernées.
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
        
    def update_total_result(self):
        """
        Met à jour le nombre de points obtenus pour la résolution du quiz en entier
        en fonction des points obtenus pour chaque réponse soumise aux questions
        du quiz.
        
        Cette méthode peut être utilisée lorsqu'une entrée dans ``SqAnswer`` a été
        ajoutée pour mettre à jour les statistques en fonction des changements.
        """
        result = 0
        
        # Ajout des points pour chaque réponse soumise
        for submit in self.get_questions_submits():
            result += submit.result
            
        self.result = result # Le nombre de points obtenus est modifié
        self.save()

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
    def get_wrong_answers(self):
        """
        Retourne la liste de toutes les réponses incorrectes soumises pour la question.
        Pour éviter les doublons, les réponses équivalentes sont renvoyées une seule fois.
        Par exemple, si deux réponses valent "5", seule la première sera renvoyée par
        cette fonction. Les réponses vides sont aussi exclues.
        """
        # Les réponses incorrectes sont celles qui ont obtenu 0 point
        l_wrong = SqSubmit.objects.filter(id_question=self).filter(result=0)
        
        l_text = [] # Liste contenant les textes des réponses ajoutés
        l_wrong_filtered = [] # Liste contenant les réponses sans doublons

        for wrong in l_wrong:
            # Si le texte de la réponse est dans la liste des textes déjà ajoutés,
            # la réponse n'est pas ajoutée dans la liste sans doublons
            if wrong.text not in l_text and wrong.text:
                l_text.append(wrong.text)
                l_wrong_filtered.append(wrong)
        
        
        print(l_wrong_filtered)
        return l_wrong_filtered
        
    def create_form(self, *args, **kwargs):
        """
        Retourne un formulaire pour répondre à la question
        """
        return forms.TextForm(question=self, prefix=self.number, *args, **kwargs)
        
    def save_submit(self, data, completed):
        """
        Créé une entrée dans la table ``SqSubmit`` pour stocker la réponse soumise
        relative à la question. L'accès aux données du formulaire Django correspondant à
        la question se fait par le dictionnaire ``data`` en argument.
        """
        # Création de l'entrée dans la base de données avec les arguments correspondants
        submit = SqSubmit(text=data['answer'], id_question=self, id_submitted_quiz=completed)
        
        # Enregistrement du résultat (pour les statistiques)
        submit.save_result()
        submit.save()
        
        return submit
        
    # def save_result(self, submit):
    #     """
    #     Comptabilise et enregistre les points pour la réponse soumise submit
    #     """
    #     result = 0
    #     if submit.correct():
    #         result = self.points
            
    #     return result
        
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
            
    def update_question_results(self):
        """
        Permet de réévaluer toutes les réponses soumises pour la question après
        l'ajout d'une solution correcte pour corriger les statistiques.
        """
        # Liste des réponses soumises à la question
        l_question_submits = SqSubmit.objects.filter(id_question=self)
        
        # Les points pour chaque réponse sont recomptabilisés
        for submit in l_question_submits:
            submit.save_result()
            # Le résultat global de chaque résolution du quiz comportant
            # cette question est mis à jour
            submit.id_submitted_quiz.update_total_result()
            
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
        
    def save_result(self):
        """
        Comptabilise et enregistre les points obtenus. Si la réponse soumise
        est correcte, tous les points sont attribués. Dans le cas contraire,
        aucun point n'est attribué.
        """
        
        result = 0
        if self.correct():
            result = self.id_question.points
        
        self.result = result
        self.save()
        
    def get_corrections(self):
        """
        Renvoie les solutions correctes pour la question sous forme de liste de
        chaînes de charactères
        """
        # Récupération des corrections de la question
        l_sq_answer = SqAnswer.objects.filter(id_question=self.id_question)
        
        # Les réponses correctes (string) sont placés dans une liste
        l_correct_text = [answer.text for answer in l_sq_answer]
        
        return l_correct_text
        
    def correct(self):
        """
        Détermine si la réponse soumise est correcte est vérifiant qu'elle se
        se trouve dans la liste des solutions correctes.
        """
        if self.text in self.get_corrections():
            return True
        else:
            return False
            
    def set_as_correct(self):
        """
        Si la réponse soumise à la question avait été définie comme incorrecte
        lors de la correction automatique, cette méthode permet d'ajouter la réponse
        soumise aux solutions correctes de la question.
        
        Toutes les réponses soumises pour la question sont ensuite rééavluées pour
        mettre à jour les statistiques.
        """
        # Nouvelle entrée dans la db pour ajouter la solution
        new_answer = SqAnswer(text=self.text, id_question=self.id_question)
        new_answer.save()
        
        # Recomptabilisation des points pour toutes les réponses soumises à la question
        self.id_question.update_question_results()
        
    def build_correct(self):
        """
        Instancie et retourne un objet ``CorrectSq`` correspondant à la réponse soumise.CompletedQuiz
        La classe ``CorrectSq`` permet un accès plus rapide aux données nécessaires à
        l'affichage de la correction.
        """
        # Instanciation de l'objet. L'argument est la réponse soumise à corriger (self)
        return CorrectSq(self)
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
        
        submit.save_result()
        submit.save()
        
        return submit
        
    # def save_result(self, submit):
    #     """
    #     Comptabilise et enregistre les points pour la réponse soumise submit
    #     """
    #     result = 0
        
    #     if self.multi_answers:
    #         l_choices = QcmChoice.objects.filter(id_question=self) # Récupération des choix de la question
    #         ppc = self.points / len(l_choices) # Nombre de points attribués par choix correct
            
    #         # À chaque option correctement cochée, on ajoute les points au résultat
    #         for c in l_choices:
    #             if c.correct(submit):
    #                 result += ppc
    #     else:
    #         if submit.id_selected:
    #             if submit.id_selected.valid:
    #                 result = self.points
        
    #     return result
        
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
            
    def get_choices(self):
        return QcmChoice.objects.filter(id_question=self)
    
class QcmChoice(models.Model): #Choix affichés pour un QCM
    text = models.CharField(max_length=50)
    valid = models.BooleanField() #Vaut True si la case doit être cochée
    id_question = models.ForeignKey(Qcm)
    
    def __str__(self):
        return self.text
        
    def correct_submit(self, qcmsubmit):
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
            
    def build_correct(self):
        """
        Instancie et retourne un objet ``CorrectQcm`` correspondant à la réponse soumise.CompletedQuiz
        La classe ``CorrectQcm`` permet un accès plus rapide aux données nécessaires à
        l'affichage de la correction.
        """
        # Instanciation de l'objet. L'argument est la réponse soumise à corriger (self)
        return CorrectQcm(self)
        
class QcmSubmitOne(QcmSubmit):
    id_selected = models.ForeignKey(QcmChoice, null=True) #Choix sélectionnés par l'élève dans un QCM à bouton radio
    
    def save_result(self):
        """
        Comptabilise
        """
        result = 0
        
        if self.id_selected: # On s'assure qu'une option a été sélectionnée
            if self.id_selected.valid: # Si l'option sélectionnée est la réponse valide
                result = self.id_question.points
        
        # Le résultat est enregistré
        self.result = result
        self.save()
    
class QcmSubmitMulti(QcmSubmit): 
    id_selected = models.ManyToManyField(QcmChoice, null=True) #Choix sélectionnés par l'élève dans un QCM à cases à cocher
    
    def save_result(self):
        """
        """
        result = 0
        l_choices = self.id_question.get_choices() # Choix de la question
        
        # Nombre de points atribués par choix correct
        ppc = self.id_question.points / len(l_choices)
        
        # À chaque option correctement cochée, on ajoute les points au résultat
        for choice in l_choices:
            if choice.correct_submit(self):
                result += ppc
        
        # Le résultat est enregistré  
        self.result = result
        self.save()