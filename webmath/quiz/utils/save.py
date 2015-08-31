from django.core.exceptions import ObjectDoesNotExist

from django.utils import timezone
from quiz.models import *


#Classe abstraite pour toutes les questions
class SaveQuestion:
    """
    Classe abstraite qui créé une nouvelle question dans la base de données avec
    les attributs communs à tous les types de questions. La méthode ``.save()``
    n'est pas encore utilisée car certains attributs doivent encore être ajoutés
    dans les classes filles.
    
    La table concernée peut être :py:class:`models.SimpleQuestion` ou :py:class:`models.Qcm`.
    Cela dépend de l'argument ``Model`` qui définit la classe à utiliser. 
    
    L'argument ``question`` est un dictionnaire contenant les données sur la question.
    Les arguments `quiz_db`` et ``n`` correspondent respectivement à la référence
    du quiz dans la table :py:class:models.Quiz`` et à l'index de la position
    de la question.
    """
    def __init__(self, question, Model, quiz_db, n):
        # Création de la nouvelle entrée sans utiliser la méthode .save()
        self.question_db = Model(
            text=question["text"],
            comment=question["comment"],
            points=question["points"],
            number=n,
            id_quiz=quiz_db
        )

class SaveSimpleQuestion(SaveQuestion):
    """
    Enregistre une question à réponse courte dans la base de données. Tous les champs
    de la base de données ont déjà été définis par :py:class:`SaveQuestion`,
    la méthode ``.save()`` peut donc être utilisée directement. Les différentes
    solutions sont ensuite sauvegardées.
    """
    def __init__(self, question, *args, **kwargs):
        SaveQuestion.__init__(self, question, *args, **kwargs)
        
        # Enregistrement dans la base de données
        self.question_db.save()
        
        # Ajout des réponses
        for answer in question["answers"]:
            self.add_answer(answer)
            
        for regex in question["regex_answers"]:
            self.add_regex_answer(regex)
            
    def add_answer(self, text):
        """
        Ajoute une solution à la question en créant un champ dans la table 
        :py:class:`models.SqAnswer`.
        """
        answer_db = SqAnswer(text=text, id_question=self.question_db)
        answer_db.save()
        
    def add_regex_answer(self, answer):
        """
        Ajoute une solution à la question sous forme d'expression régulière. La
        table utilisée est :py:class:`models.SqRegexAnswer`.
        """
        text = answer["text"]
        regex = answer["regex"]
        
        answer_db = SqRegexAnswer(text=text, id_question=self.question_db, regex=regex)
        answer_db.save()

#Classe abstraite pour tous les QCM
class SaveQcm(SaveQuestion):
    """
    Enregistre une question à choix multiples dans la base de données. S'il s'agit
    d'une question à réponses correctes multiples, il faut assigner la valeur ``True``
    à l'attribut ``multi_answers``. Par défaut, celui-ci reçoit la valeur ``False``.
    Les différentes options à sélectionner sont également enregistrées.
    """
    def __init__(self, question, *args, **kwargs):
        SaveQuestion.__init__(self, question, *args, **kwargs)
        
        if question["type"] == 1:
            self.question_db.multi_answers = True
        
        self.question_db.save()
        
        for option in question["options"]:
            self.add_option(option)
            
    def add_option(self, option):
        """
        Ajoute une option à la question en créant une nouvelle entrée dans la table
        :py:class:`models.QcmChoice`.
        """
        text = option["content"]
        valid = option["valid"]
        
        choice_db = QcmChoice(text=text, valid=valid, id_question=self.question_db)
        choice_db.save()


class SaveQuiz:
    """
    Classe permettant l'enregistrement d'un quiz et de toutes ses questions dans
    la base de données. Une première entrée :py:class:`models.Quiz` est enregistrée
    puis les données des questions sont sauvegardées par l'intermédiaire des classes
    :py:class:`SaveSimpleQuestion` et :py:class:`SaveQcm`.
    
    """
    TYPES = [SaveSimpleQuestion, SaveQcm, SaveQcm]
    MODELS = [SimpleQuestion, Qcm, Qcm]
    
    def __init__(self, title, questions_list, quizcode, teacher, tags=None):
        self.quiz_db = Quiz(title=title, code=quizcode, id_teacher=teacher)
        self.quiz_db.save()

        tags = tags or []

        # création et/ou liaison avec la table des tags
        for t in tags:
            t = t.strip()
            t = t.replace(' ', '-')
            try:
                tag = Tag.objects.get(name=t)
            except ObjectDoesNotExist:
                # créer le tag
                tag = Tag(name=t)
                tag.save()
            self.quiz_db.tags.add(tag)

        
        n_question = 0
        global_points = 0
        
        for question in questions_list:
            q_type = question["type"] #Récupération du type de question
            
            Constructor = SaveQuiz.TYPES[q_type]
            Model = SaveQuiz.MODELS[q_type]
            
            Constructor(question=question, Model=Model, quiz_db=self.quiz_db, n=n_question) #Instanciation à patir du constructeur correspondant
            
            global_points += question["points"]
            n_question += 1
            
        self.quiz_db.points = global_points
        self.quiz_db.save()