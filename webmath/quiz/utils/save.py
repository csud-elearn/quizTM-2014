from django.utils import timezone
from quiz.models import *


#Classe abstraite pour toutes les questions
class SaveQuestion:
    def __init__(self, quiz_db, question, n):
        self.question = question
        
        self.text = question["text"]
        self.comment = question["comment"]
        self.points = question["points"]
        self.id_quiz = quiz_db
        self.number = n

#Enregistre une question simple
class SaveSimpleQuestion(SaveQuestion):
    def save_db(self):
        self.question_db = SimpleQuestion( #Enregistrement dans la table avec les paramètres
            text=self.text,
            comment=self.comment,
            number=self.number,
            id_quiz=self.id_quiz,
            points=self.points
        )
        self.question_db.save()
        
        for answer in self.question["answers"]:
            self.add_answer(answer)
            
    def add_answer(self, text):
        answer_db = SqAnswer(text=text, id_question=self.question_db)
        answer_db.save()

#Classe abstraite pour tous les QCM
class SaveQcm(SaveQuestion):
    def save_db(self):
        self.question_db = Qcm(
            text=self.text, 
            comment=self.comment, 
            number=self.number, 
            id_quiz=self.id_quiz, 
            multi_answers=self.multi_answers, 
            show_list=self.show_list, 
            points=self.points
        )
        self.question_db.save()
        
        for option in self.question["options"]:
            self.add_option(option)
            
    def add_option(self, option):
        text = option["content"]
        valid = option["valid"]
        
        choice_db = QcmChoice(text=text, valid=valid, id_question=self.question_db)
        choice_db.save()

#Enregistre un qcm de type checkbox
class SaveQcmCheckbox(SaveQcm):
    def __init__(self, quiz_db, question, n):
        SaveQcm.__init__(self, quiz_db, question, n)
        
        self.multi_answers = True
        self.show_list = False

#Enregistre un qcm de type radio
class SaveQcmRadio(SaveQcm):
    def __init__(self, quiz_db, question, n):
        SaveQcm.__init__(self, quiz_db, question, n)
        
        self.multi_answers = False
        self.show_list = False

#Enregistre un qcm de type liste déroulante
class SaveQcmSelect(SaveQcm):
    def __init__(self, quiz_db, question, n):
        SaveQcm.__init__(self, quiz_db, question, n)
        
        self.multi_answers = False
        self.show_list = True

class SaveQuiz:
    TYPES = [SaveSimpleQuestion, SaveQcmCheckbox, SaveQcmRadio, SaveQcmSelect]
    
    def __init__(self, title, questions_list, quizcode, teacher):
        self.quiz_db = Quiz(title=title, code=quizcode, id_teacher=teacher)
        self.quiz_db.save()
        
        n_question = 0
        
        for question in questions_list:
            q_type = question["type"] #Récupération du type de question
            Constructor = SaveQuiz.TYPES[q_type] 
            q = Constructor(self.quiz_db, question, n_question) #Instanciation à patir du constructeur correspondant
            q.save_db()
            n_question += 1
            
    def get_id(self):
        return self.quiz_db.pk