from django.db import models
from django.contrib.auth.models import User
from common.models import Teacher
import quiz.forms as forms
from quiz.utils.correct import *

# Create your models here.

class Quiz(models.Model): #Infos générales sur le quiz
    """
    Table dont le rôle est de stocker les informations générales sur le quiz telles
    que le titre du quiz, le nombre maximal de points pouvant être obtenus ou la date
    et l'heure de sa création.
    
    Tous les modèles contenant les données des questions du quiz incluent une clé
    étrangère reliant la question avec la table ```Quiz``.
    """
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
        
class QuizDraft(models.Model):
    """
    La table ``QuizDraft`` sert à stocker les brouillons. Elle contient le titre
    du brouillon, le code ainsi qu'une relation vers le créateur du brouillon.
    """
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=1000)
    id_teacher = models.ForeignKey('common.Teacher')
    
    def __str__(self):
        return self.title
    
class CompletedQuiz(models.Model):
    """
    Contient 
    """
    submit_date = models.DateTimeField(auto_now_add=True)
    result = models.FloatField(default=0)
    id_quiz = models.ForeignKey(Quiz) #Relation avec le quiz complété
    id_user = models.ForeignKey(User)
                
    def get_questions_submits(self):
        """
        Renvoie la liste des entrées des tables ``SqSubmit``, ``QcmSubmitOne`` et
        ``QcmSubmitMulti`` correspondant à la résolution ``self``.
        Chaque élément de cette liste représente concrètement la réponse soumise à
        une question du quiz.
        
        Cette liste est triée selon l'ordre d'apparition des questions correspondant
        réponses proposées.
        """
        # Les éléments sont récupérés et placés dans une liste non-triée
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
        
        Pour comptabiliser le nombre total de points obtenus, cette méthode parcourt
        la liste des réponses apportées avec la méthode :py:meth:`CompletedQuiz.get_questions_submits()`
        appliquée à la résolution en question.
        calcule la somme des points obtenus pour chacune des questions.
        
        Cette méthode peut être utilisée lorsqu'une résolution vient d'être soumise
        par un élève pour comptabiliser une première fois les points obtenus ou 
        lorsqu'une entrée dans :py:class:`SqAnswer` a été ajoutée pour mettre à jour les
        statistques en fonction des changements.
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
        Retourne la liste de toutes les réponses incorrectes soumises pour la question ``self``.
        Pour éviter les doublons, les réponses équivalentes sont renvoyées une seule fois.
        Par exemple, si deux réponses valent ``"5"``, seule la première sera renvoyée par
        cette méthode.
        
        Comme cette méthode est utilisée pour afficher les réponses soumises incorrectes pouvant
        potentiellement être définies comme correctes par la suite au cas où le 
        professeur les juge acceptables, les réponses vides sont aussi exclues 
        puisqu'il n'y aurait pas de sens à les admettre dans les solutions.
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
        
        return l_wrong_filtered
        
    def create_form(self, *args, **kwargs):
        """
        Instancie un formulaire Django personnalisé de type ``TextForm`` correspondant
        à la question. Ce type de formulaire est défini dans py:mod:`forms` et spécialement
        conçu pour les questions à réponse courte. 
        
        Lors de l'instanciation, plusieurs arguments sont fournis. Premièrement,
        on indique la question ``self`` pour que des informations supplémentaires
        la concernant puissent éventuellement être obtenues depuis le formulaire.CompletedQuiz
        Ensuite, l'index de la position de la question dans le quiz est attribué à
        l'argument ``prefix``. Cet argument permet d'identifier la question correspondant
        au formulaire lorsque les données entrées par l'utilisateur sont récupérées.
        """
        return forms.TextForm(question=self, prefix=self.number, *args, **kwargs)
        
    def save_submit(self, data, completed):
        """
        Cette méthode permet d'enregistrer dans la base de données une réponse soumise
        par l'utilisateur à la question ``self`` en créant une entrée dans la table
        ``SqSubmit``.
        
        L'argument ``data`` est dictionnaire contenant les paramètres de la 
        requête HTTP qui concernent le formulaire créé pour la question. On peut donc
        facilement accéder au texte entré par l'élève avec la clé ``'answer'``.
        
        L'argument ``completed`` contient la référence vers l'élément de la table
        ``CompletedQuiz`` qui comprend les données de la résolution de l'élève. On
        peut ainsi facilement relier l'entrée créée dans ``SqSubmit`` avec la résolution
        de l'élève.
        """
        # Création de l'entrée dans la base de données avec les arguments correspondants
        submit = SqSubmit(text=data['answer'], id_question=self, id_submitted_quiz=completed)
        
        # Enregistrement du résultat (pour les statistiques)
        submit.save_result()
        submit.save()
        
        return submit
        
    def average_result(self):
        """
        Renvoie le nombre moyen de points obtenus pour la question en se basant sur
        le nombre total de réponses soumises et sur la somme de tous les points obtenus.
        La moyenne est ensuite arrondie à deux chiffres après la virgule pour éviter
        tout problème d'affichage.
        
        Au cas où aucune réponse n'a encore été soumise, cette méthode retourne
        simplement la chaîne ``--`` qui peut directement être utilisée dans le template.
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
        
        Pour ceci, la méthode récupère la liste des réponses soumises à la question
        dans la table ``SqSubmit``. Elle applique la méthode ``.save_result`` à 
        chacune d'entre elles. De plus,
        comme le résultat de la résolution peut changer, il faut aussi mettre à jour
        le résultat total obtenu pour la résolution (table ``CompletedQuiz``) liée à chaque réponse soumise.
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
        Comptabilise et enregistre les points obtenus pour la réponse soumise. Si la réponse soumise
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
        Renvoie la liste des solutions correctes pour la question sous forme de liste de
        chaînes de charactères
        """
        # Récupération des corrections de la question
        l_sq_answer = SqAnswer.objects.filter(id_question=self.id_question)
        
        # Les réponses correctes (string) sont placés dans une liste
        l_correct_text = [answer.text for answer in l_sq_answer]
        
        return l_correct_text
        
    def correct(self):
        """
        Détermine si la réponse soumise est correcte en vérifiant qu'elle se
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
        
        Toutes les réponses soumises pour la question sont ensuite réeavaluées pour
        mettre à jour les statistiques.
        """
        # Nouvelle entrée dans la db pour ajouter la solution
        new_answer = SqAnswer(text=self.text, id_question=self.id_question)
        new_answer.save()
        
        # Recomptabilisation des points pour toutes les réponses soumises à la question
        self.id_question.update_question_results()
        
    def build_correct(self):
        """
        Instancie et retourne un objet ``CorrectSq`` correspondant à la réponse soumise ``self``.
        La classe :py:class:``CorrectSq`` permet un accès plus rapide aux données nécessaires à
        l'affichage de la correction.
        """
        # Instanciation de l'objet. L'argument est la réponse soumise à corriger (self)
        return CorrectSq(self)
# 
#Tables concernant les QCM
#

class Qcm(QuizQuestion):
    multi_answers = models.BooleanField(default=False) #True si il est possible de cocher plusieurs choix
    
    def create_form(self, *args, **kwargs):
        """
        Retourne un formulaire Django permettant à un étudiant de répondre à la question
        ``self``. Le formulaire sera de type ``RadioForm`` si un seul choix
        peut être sélectionné et de type ``CheckboxForm`` si la question autorise
        l'étudiant à cocher plusieurs options.
        
        Les arguments fournis lors de l'instanciation du formulaire sont analogues
        à ceux qui sont donnés pour l'instanciation d'un ``TextForm`` dans :py:meth:`SimpleQuestion.create_form`.
        """
        if self.multi_answers:
            Form = forms.CheckboxForm
        else:
            Form = forms.RadioForm
            
        return Form(queryset=QcmChoice.objects.filter(id_question=self), prefix=self.number, question=self, *args, **kwargs)
        
    def save_submit(self, data, completed):
        """
        Enregistre une nouvelle entrée dans la table :py:class:`QcmSubmitMulti`
        ou :py:class:`QcmSubmitOne` selon qu'il s'agisse d'une question avec
        plusieurs options correctes ou une seule. Ces tables permettent de stocker
        le(s) choix sélectionné(s) par l'étudiant pour la question ``self``.
        
        La récupération des données du formulaire à partir de l'argument ``data``
        et l'instanciation du modèle est analogue à la manipulation effectuée dans :py:meth:`SimpleQuestion.save_submit`
        """
        if self.multi_answers:
            Model = QcmSubmitMulti
        else:
            Model = QcmSubmitOne
            
        submit = Model(id_submitted_quiz=completed, id_question=self)
        
        if self.multi_answers:
            submit.save()
        
        #Comme il peut s'agir d'une relation many to many, il faut sauvegarder et ajouter la relation après
        submit.id_selected=data['answer']
        
        submit.save_result()
        submit.save()
        
        return submit
        
    def average_result(self):
        """
        Récupère toutes les réponses soumises pour la question et renvoie la moyenne
        arrondie à deux chiffres après la virgule sur la base du nombre de réponses
        proposées et sur la somme des résultats obtenus.
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
        Détermine le choix ``self`` a été coché correctement dans la réponse
        soumise ``qcmsubmit``. Si l'option a été cochée et qu'elle est définie
        comme valide, la méthode renvoie ``True``. Si l'option est cochée mais
        définie comme invalide, la valeur de retour sera cette fois ``False``.
        Si l'élève n'a pas coché l'option, le raisonnement se fera de manière analogue
        mais dans le sens inverse.
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
        Détermine si le choix a été sélectionné ou non dans la réponse soumise
        ``qcmsubmit``.
        
        S'il la question peut admettre plusieurs options correctes, deux conditions doivent
        être remplies. D'abord, au moins un choix doit avoir été coché dans ``qcmsubmit``.
        Cette vérification est nécessaire car le champ ``qcmsubmit.id_selected`` peut
        valoir ``null`` dans la base de données. Ensuite, il suffit de regarder
        si le choix se trouve dans la liste des options sélectionnés avec la méthode
        ``qcmsubmit.id_selected.all()``.
        
        Dans le cas d'une question avec une seule réponse correcte, la méthode
        vérifie simplement que l'élément sélectionné corresponde au choix défini comme
        correct.
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
        Instancie et retourne un objet :py:class:`utils.correct.CorrectQcm` correspondant à la réponse soumise.
        La classe :py:class:`utils.correct.CorrectQcm` permet un accès plus rapide aux données nécessaires
        à l'affichage de la solution depuis le template.
        """
        # Instanciation de l'objet. L'argument est la réponse soumise à corriger (self)
        return CorrectQcm(self)
        
class QcmSubmitOne(QcmSubmit):
    id_selected = models.ForeignKey(QcmChoice, null=True) #Choix sélectionnés par l'élève dans un QCM à bouton radio
    
    def save_result(self):
        """
        Comptabilise et enregistre les points obtenus par raport au choix sélectionné.
        
        Si le choix sélectionné correspond à la solution, tous les points sont attribués.
        Si aucune option n'est choisie, l'étudiant obtient automatiquement zéro point.
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
        Comptabilise et enregistre les points obtenus par rapport aux choix cochés.
        
        Cette méthode parcourt tous les choix possibles pour la question
        ``self.id_question`` récupérés avec :py:meth:`Qcm.get_choices`. Pour chaque
        choix, elle utilise la méthode :py:meth:`QcmChoice.correct_submit` pour
        vérifier que le choix a été coché correctement. L'étudiant obtient une part
        des points pour chaque choix correct.
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