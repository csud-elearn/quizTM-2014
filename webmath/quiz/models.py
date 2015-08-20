from django.db import models
from django.contrib.auth.models import User
from common.models import Teacher
import quiz.forms as forms
from quiz.utils.correct import *
import re

# Create your models here.

class Quiz(models.Model): #Infos générales sur le quiz
    """
    La table ``Quiz`` est la table centrale de l'application et toutes les autres 
    tables s'organisent autour d'elle. Elle comporte trois colonnes importantes :
    une contenant le titre, une autre contenant la date et l'heure de création 
    ainsi qu'une colonne 
    dans laquelle est stockée le nombre maximal de points pouvant être obtenus pour
    le quiz en question. Cette table comporte également une relation vers une table
    Teacher  qui permet d'intégrer le système d'authentification des utilisateurs.

    Avec django, il est possible d'initialiser automatiquement un champ ``DateTimeField`` à la date/heure du moment où le modèle est instancié avec le paramètre ``auto_now_add``

    .. code-block:: python
    
        creation_date = models.DateTimeField(auto_now_add=True)
    """
    title = models.CharField(max_length=200)
    points = models.FloatField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    code = models.TextField() #Format texte du quiz
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
    Cette table est un peu isolée dans le schéma relationnel et n'a qu'une fonction :
    enregistrer le code qu'un quiz qu'un professeur n'a pas terminé et lui offrir
    la possibilité de le récupérer plus tard pour continuer son travail.
    Outre la relation vers la table ``Teacher`` et la colonne stockant le code du
    quiz, une colonne permet de stocker un titre pour pouvoir identifier rapidement
    un brouillon.
    """
    title = models.CharField(max_length=200)
    code = models.TextField()
    id_teacher = models.ForeignKey('common.Teacher')
    
    def __str__(self):
        return self.title
    
class CompletedQuiz(models.Model):
    """
    Comme on peut le voir sur le diagramme, à l'instar de ``Quiz``, cette table
    occupe aussi un rôle central dans le modèle relationnel. Elle permet de faire
    le lien entre un quiz créé par un professeur et les réponses soumises à ce quiz
    par les étudiants. Elle possède donc une relation vers une table ``Student``,
    qui définit l'étudiant ayant répondu au quiz. De l'autre côté, cette table pointe
    vers ``Quiz`` et définit logiquement le quiz auquel l'étudiant a répondu. Un seul
    champ est présent : la date et l'heure de la soumission des réponses.
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
        la liste des réponses apportées avec la méthode ``.get_questions_submits()``
        appliquée à la résolution en question.
        
        Cette méthode peut être utilisée lorsqu'une résolution vient d'être soumise
        par un élève pour comptabiliser une première fois les points obtenus ou 
        lorsqu'une entrée dans :py:class:`SqAnswer` a été ajoutée pour mettre à jour les
        statistiques en fonction des changements.
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
    text = models.TextField() #Énoncé
    comment = models.TextField(blank=True) #Commentaire affiché lors de la correction
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
    """
    Cette table contient les informations générales sur les questions simples du quiz.
    Ces questions sont présentées sous la forme d'un simple champ de texte lorsqu'un
    élève complète le quiz. Une première colonne ``title`` stocke l'énoncé de la
    question, ``comment`` permet d'inclure un commentaire affiché lors de la
    correction automatique du quiz (par exemple la démonstration d'une égalité),
    ``points`` définit le nombre de points attribués sur cette question et ``number``
    enregistre la position à laquelle doit apparaître la question dans le quiz. Une relation
    désigne le quiz qui intègre la question.
    """
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
        la concernant puissent éventuellement être obtenues depuis le formulaire.
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
        
        L'argument ``data`` est un dictionnaire contenant les paramètres de la 
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
        dans la table ``SqSubmit``. Elle applique la méthode ``SqSubmit.save_result()`` à 
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
            
class SqAnswerAbstract(models.Model):
    text = models.CharField(max_length=200)
    id_question = models.ForeignKey(SimpleQuestion) #Relation vers la question
    
    class Meta:
        abstract = True
        
    def __str__(self):
        return self.text
            
class SqAnswer(SqAnswerAbstract):
    """
    Cette table contient simplement la solution de la question définie par la
    relation vers la table ``SimpleQuestion``. Il est important de noter qu'il
    peut y avoir plusieurs solutions possibles pour une question et c'est la raison
    pour laquelle la solution n'est pas simplement stockée dans une colonne de
    :py:class:`SimpleQuestion`.
    """
        
    def match(self, answer):
        return self.text == answer
        
class SqRegexAnswer(SqAnswerAbstract):
    """
    Table très similaire à ``SqAnswer`` sauf qu'elle contient une solution sous la
    forme d'une expression régulière. Cette solution offre plus de souplesse
    dans la correction des réponses soumises par les étudiants.
    """
    
    regex = models.CharField(max_length=200)
    
    def match(self, answer):
        print(self.regex)
        if re.match(self.regex, answer):
            return True
        else:
            return False

class SqSubmit(models.Model):
    """
    Il s'agit simplement de la réponse apportée à une question simple. La table
    a donc un champ ``text`` qui contient la réponse soumise par l'élève et un champ
    ``result`` qui stocke le nombre de points obtenus pour la question. Elle possède
    aussi deux relations, une vers ``SimpleQuestion`` pour préciser la question auquel
    l'élève a répondu, et une autre vers ``CompletedQuiz``. La réponse soumise par l'élève
    sera ensuite comparée à(aux) solution(s) enregistrées pour déterminer si les points
    sont attribués ou non.
    """
    text = models.CharField(max_length=200)
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
        Renvoie la liste des solutions correctes pour la question
        """
        # Récupération des corrections de la question
        l_sq_answer = list(SqAnswer.objects.filter(id_question=self.id_question))\
        + list(SqRegexAnswer.objects.filter(id_question=self.id_question))
        
        return l_sq_answer
        
    def correct(self):
        """
        Détermine si la réponse soumise est correcte en vérifiant qu'elle correspondent à
        une des solutions de la question.
        """
        
        print("Correction")
        
        for correction in self.get_corrections():
            
            print(self.get_corrections())
            if correction.match(self.text):
                print(correction)
                return True
                
        print("problème")
        
        return False
            
    def set_as_correct(self):
        """
        Si la réponse soumise à la question avait été définie comme incorrecte
        lors de la correction automatique, cette méthode permet d'ajouter la réponse
        soumise aux solutions correctes de la question.
        
        Toutes les réponses soumises pour la question sont ensuite rééavaluées pour
        mettre à jour les statistiques.
        """
        # Nouvelle entrée dans la db pour ajouter la solution
        new_answer = SqAnswer(text=self.text, id_question=self.id_question)
        new_answer.save()
        
        # Recomptabilisation des points pour toutes les réponses soumises à la question
        self.id_question.update_question_results()
        
    def build_correct(self):
        """
        Instancie et retourne un objet :py:class:`CorrectSq` correspondant à la réponse soumise ``self``.
        La classe :py:class:`CorrectSq` permet un accès plus rapide aux données nécessaires à
        l'affichage de la correction.
        """
        # Instanciation de l'objet. L'argument est la réponse soumise à corriger (self)
        return CorrectSq(self)
# 
#Tables concernant les QCM
#

class Qcm(QuizQuestion):
    """
    La table Qcm permet de stocker les informations générales à propos des questions à choix multiples.
    Ces questions sont affichées sous forme de boutons radio ou de cases à cocher en HTML.
    Cette table reprend plusieurs colonnes de la table ``SimpleQuestion``. C'est
    pourquoi ces deux tables héritent en fait de la même classe dans Django ``QuizQuestion``.
    Cette dernière n'est pas à proprement parler un modèle, puisqu'elle ne correspond
    à aucune table de la base de données. C'est une classe abstraite, c'est à dire
    que d'autres classes peuvent hériter de ses caractéristiques mais qu'elle ne
    sera jamais directement instanciée.
    
    Dans Django, la définition d'un modèle de ce type se fait en déclarant une classe
    interne ``Meta`` et en initialisant la variable de classe ``abstract`` à ``True`` :

    .. code-block:: python
            
        class Meta:
            abstract = True

    En plus des colonnes héritées de ``QuizQuestion```, ``Qcm`` possède un champ
    de type booléen. Il s'agit de ``multi_answers``, qui détermine si plusieurs
    options peuvent être cochées ou non. Si ce champ vaut ``True``, la question
    sera affichée sous forme de cases à cocher en HTML. Dans le cas contraire, elle
    sera affichée à l'aide de boutons radio.
    """
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
        et l'instanciation du modèle est analogue à la manipulation effectuée dans ``.save_submit()``
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
    
class QcmChoice(models.Model):
    """
    Cette table contient les différents choix possibles pour la question définie
    par la relation vers ``Qcm``. Elle est formée de deux champs, le premier contenant
    le texte du choix et l'autre définissant par un booléen s'il est correct ou
    non de cocher ce choix. Une question à choix multiples doit avoir au moins
    deux choix possibles et au moins un choix correct. Si ``multi_answers`` vaut
    ``False`` dans ``Qcm``, une seule option peut être correcte puisque l'étudiant
    n'a la possibilité de cocher qu'une seule option.
    
    .. note::
        D'un point de vue purement relationnel, comme il est indiqué sur
        le diagramme, cette table possède une relation vers une table qui sert
        d'intermédiaire entre ``QcmChoice`` et ``QcmSubmitMulti``. Cette table intermédiaire
        crée en fait une relation de type *complexe-complexe*. L'implémentation de ce
        type de relation avec Django sera abordée plus loin.
    """
    text = models.TextField()
    valid = models.BooleanField(default=True) #Vaut True si la case doit être cochée
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
    """
    ``QcmSubmit`` est une classe abstraite dont héritent :py:class:`QcmSubmitOne`
    et :ref:class`QcmSubmitMulti`. Elle ne définit donc pas une table dans la base
    de données mais rassemble les attributs communs aux deux classes filles.
    
    Les tables :py:class:`QcmSubmitOne` et :py:class`QcmSubmitMulti` sont très similaires.
    La première contient une relation
    vers l'option sélectionnée par l'étudiant dans une question à choix multiples
    avec ``multi_answers`` valant ``False```, tandis que ``QcmSubmitMulti`` peut
    contenir des relations vers plusieurs options et est utilisée lorsque ``multi_answers`` vaut
    ``True``. Il s'agit donc dans le premier cas d'une relation *complexe-simple*,
    puique chaque entrée pointe vers une seule option. Dans le deuxième
    cas, c'est une relation de type *complexe-complexe*, puisqu'il est possible qu'une
    entrée soit reliée à plus d'une option.

    Dans Django, voici comment seront définies ces relations :

    .. code-block:: python
    
        id_selected = models.ForeignKey(QcmChoice, null=True) #Relation complexe-simple
        id_selected = models.ManyToManyField(QcmChoice, null=True) #Relation complexe-complexe
        
    L'argument ``null`` vaut ici ``True`` car il se peut que l'étudiant ne coche aucun choix.
    
    En plus de ces relations, ces tables enregistrent aussi le nombre de points obtenus
    par l'étudiant pour la question dans la colonne ``result``. Deux autres relations
    sont présentes : la première fait le lien avec la résolution dans la table :ref:class:`CompletedQuiz`
    et la deuxième relie l'entrée avec la question à laquelle la réponse est apportée.
    """
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
        Comptabilise et enregistre les points obtenus par rapport au choix sélectionné.
        
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
        ``self.id_question`` récupérés avec ``.get_choices()``. Pour chaque
        choix, elle utilise la méthode ``.correct_submit()`` pour
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