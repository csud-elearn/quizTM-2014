from quiz.models import CompletedQuiz

class QuizForms:
    """
    Le rôle de cette classe est de créer des formulaires Django correspondant aux
    questions d'un quiz en particulier puis de fournir des méthodes pour traiter
    les données récupérées grâce aux formulaires et de les enregistrer.
    """
    def __init__(self, quiz, data=None):
        """
        Lorsqu'un objet ``QuizForms`` est instancié, les questions correspondant à l'argument ``quiz``
        sont récupérées dans la base de données. Ensuite, un formulaire Django est
        créé pour chaque question. La création de ce formulaire se fait
        en appliquant la méthode ``.create_form()`` aux diférentes questions. Cette
        méthode prend en charge l'instanciation du formulaire Django adéquat par rapport
        au type de la question à laquelle elle est appliquée. ``.create_form()``
        possède un argument, ``data``. Il s'agit des paramètres de la requête HTTP POST.
        Si l'objectif est d'afficher un formulaire vide, cet argument vaut toujours
        ``None`` et n'est pas utilisé. En revanche, il permet d'accéder aux données entrées par l'utilisateur
        après qu'un élève a complété le quiz.
        """
        self.quiz = quiz
        
        self.l_questions = quiz.get_questions() # Questions composant le quiz
        self.l_forms = []
        
        # Création des formualaires pour chaque question
        for question in self.l_questions:
            self.l_forms.append(question.create_form(data=data))
        
    def are_valid(self):
        """
        Applique la méthode ``.is_valid()`` à chaque formulaire correspondant à une
        question et renvoie ``True`` si aucun problème survient avec la validation.
        """
        valid = True
        # Si .is_valid() renvoie toujours True, .are_valid() renvoie True
        for form in self.l_forms:
            if not form.is_valid():
                valid = False
        
        return valid
        
    def save_answers(self, user):
        """
        Cette méthode permet de sauvegarder dans la base de données les réponses
        soumises par le biais des formulaires Django correspondant à chaque question.
        
        Pour ce faire, une nouvelle entrée dans la table ``CompletedQuiz`` est
        d'abord créée. Ensuite, la méthode parcourt parallèlement la liste des questions
        du quiz et les formulaires correspondants. Pour chaque question, elle appelle
        la méthode ``.save_submit()`` avec en argument les données récupérées à partir
        du formulaire associé à la question. La méthode ``.save_submit()`` se charge
        ensuite de sauvegarder les données concernant les réponses soumises aux différentes
        questions. La manière de traiter ces données dépendera du type de question
        dont il s'agit. On peut appliquer la méthode ``.save_submit()`` à chacune
        des questions du quiz sans se soucier du type car son comportement est défini
        différement selon la classe à laquelle appartient la question.
        """
        # Nouvelle entrée dans la base de données
        completed = CompletedQuiz(id_quiz=self.quiz, id_user=user)
        completed.save()
        
        for question, form in zip(self.l_questions, self.l_forms):
            #Pour chaque question, on appelle la méthode avec en argument les données du formulaires
            # correspondant et la référence vers la résolution du quiz (table CompletedQuiz)
            submit = question.save_submit(form.cleaned_data, completed)
            
        completed.update_total_result() # Comptabilisation des points d'après les réponses soumises
        completed.save()
            
        return completed