from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.core.urlresolvers import reverse
from quiz.utils.save import SaveQuiz
from quiz.utils.submit import QuizForms
from quiz.utils.correct import CorrectQuiz
from quiz.forms import TextForm, CheckboxForm, RadioForm, SelectForm
from quiz.models import Quiz, QuizDraft, CompletedQuiz, SqSubmit, QcmSubmitMulti, QcmSubmitOne
from common.models import Teacher, Student
from common.auth_utils import *
from django.contrib.auth.decorators import login_required, user_passes_test
import json

def index(request):
    return render(request, 'quiz/index.html')

@login_required
@user_passes_test(is_teacher)
def create(request):
    """
    Cette vue sert à la fois à l'affichage de l'outil de création de quiz et à
    l'enregistrement de nouveaux quiz.
    
    S'il s'agit d'une requête HTTP GET, elle renvoie simplement le template de
    création de quiz contenant un formulaire vide.
    
    Au contraire, s'il la requête HTTP est de type POST, la vue se charge d'enregistrer
    le nouveau quiz dans la base de données en instanciant un objet de la classe
    ``SaveQuiz`` avec en argument les paramètres de la requête HTTP et le compte
    utilisateur du créateur du quiz. Cette
    classe se charge ensuite de créer les entrées nécessaires dans les différentes tables de
    la base de données.
    
    Une fois le quiz enregistré, la vue redirige l'utilisateur vers la page de
    résolution du quiz qui vient d'être créé.
    
    **Paramètres de la requête HTTP POST \:**
    
    * ``title`` : Le titre du quiz
    * ``json`` : Les données des questions du quiz structurées sous forme de json. Le json sera ensuite parsé par la classe ``SaveQuiz``.
    * ``quizcode`` : Le format texte du quiz, interprété côté client pour construire le json
    """
    if request.method == 'POST':
        json_string = request.POST['json'] #Chaîne json contenant toutes les données des questions du quiz
        title = request.POST['title']
        quizcode = request.POST['quizcode'] #Code (format texte) du quiz
        
        questions_list = json.loads(json_string) #Parsing du json
        
        teacher_account = Teacher.objects.get(user=request.user) #Compte prof correspondant à l'user
        
        quiz = SaveQuiz(title, questions_list, quizcode, teacher_account) #Sauvegarde du quiz dans la db
        
        # Redirection vers la page de résolution du quiz créé
        return HttpResponseRedirect(reverse("quiz:complete", args=[quiz.get_id()]))
    else:
        return render(request, 'quiz/create.html')

@login_required
def complete(request, n_quiz):
    """
    Cette vue est destinée à la résolution des quiz. Comme ``create``, son comportement
    change selon qu'il s'agisse d'une requête HTTP de type GET ou de type POST.
    
    Dans le cas d'une requête de type GET, la vue se contente de récupérer le quiz
    correspondant à l'id ``n_quiz`` et d'instancier un objet ``QuizForms`` à partir
    du quiz sélectionné. Cet objet prend en charge la création de tous les formulaires
    Django nécessaires pour compléter le quiz (un formulaire Django par question).
    Ces formulaires Django sont ensuite récupérés par l'intermédiaire de la méthode
    ``.get_forms()`` et placés dans le contexte de la fonction ``render``.
    
    La requête de type POST est utilisée pour l'enregistrement des réponses soumises
    au quiz par un étudiant. Là aussi, on utilise la classe ``QuizForms``, sauf que
    l'instanciation se fait avec un deuxième argument, ``data``. Cet argument contient
    en fait les données soumises par le biais des formulaires Django lorsque un
    étudiant complète le quiz. Pour s'assurer de la validité de ces données, on
    utilise la méthode ``.are_valid`` de la classe ``QuizForms``. Une fois le
    contrôle effectué, la méthode ``.save_answers`` se charge d'ajouter de nouvelles
    entrées dans la base de donnée pour stocker les réponses soumises par l'étudiant.
    Pour finir, l'utilisateur est redirigé vers la page de correction correspondant
    aux réponses envoyées précédemment.
    
    **Paramètres de la requête HTTP POST \:""
    
    * Ces paramètres dépendent du type et du nombre de questions qui constituent le quiz.
    """
    # Si la requête est de type POST, on créer un nouveau formulaire et on le remplit avec les données de requête
    if request.method == 'POST':
        quiz = Quiz.objects.get(id=n_quiz) #Récupération du quiz sélectionné dans la base de donnée
        
        quizforms = QuizForms(quiz, data=request.POST)
        
        #On controle que les formulaires sont valides
        if quizforms.are_valid():
            
            completed = quizforms.save_answers(request.user) #Les réponses sont enregistrées dans la db
            
            return HttpResponseRedirect(reverse("quiz:correct", args=[completed.pk]))

    # Si la requête est de type GET, on affiche un formulaire vide
    else:
        quiz = get_object_or_404(Quiz, id=n_quiz) #Récupération du quiz dans la db
        
        quizforms = QuizForms(quiz)
            
        return render(
            request, 'quiz/complete.html',
            {'quiz': quiz, 'l_forms': quizforms.get_forms()}
        )
        
def find(request):
    """
    Récupère dans la base de données les derniers quiz créés par des professeurs
    et renvoie un template contenant des informations générales sur ces quiz et
    un lien pour y accéder.
    """
    return render(
        request, 'quiz/find.html',
        {'l_quiz' : Quiz.objects.order_by('-creation_date')[:5]}
    )

def findquiz(request):
    """
    Renvoie sous forme de json le titre et l'url pour accéder au quiz dont l'id est donné
    en paramètre de la requête GET.
    
    L'url du quiz est construite à l'aide de la méthode ``reverse(vue, arguments)``
    fournie par Django.
    Le premier argument est une chaîne de caractère composé du nom de l'application
    et du nom de la vue (dans les urls) respectant le schéma suivant :
    ``"nom_app:nom_vue"``. L'argument ``args`` est une liste contenant les arguments
    de l'URL de la page souhaitée. Ici, il s'agit simplement de l'ID du quiz recherché.
    
    Cette vue est essentiellement destinée à être utilisé par une requête Ajax
    depuis la vue ``find``.
    
    **Exemple de json renvoyé par la vue \:**
    
    .. code-block:: json
    
        {
            "title": "Un quiz sympathique",
            "url": "/quiz/1/complete/"
        }
    
    **Paramètres de la requête HTTP GET\:**
    
    * ``quiz`` : Id du quiz recherché
    """
    if request.method == "GET":
        n_quiz = request.GET['quiz'] # id du quiz dans les argument de la requête
        
        quiz = get_object_or_404(Quiz, id=n_quiz) # Récupération du quiz dans la db
        url = reverse("quiz:complete", args=[n_quiz]) # Construction de l'url du quiz
        
        # Création d'un dictionnaire contenant les informations à envoyer
        json_dict = {
            "url" : url,
            "title" : quiz.title
        }
        json_string = json.dumps(json_dict) # Sérialisation en json
            
        return HttpResponse(json_string)

@login_required
@user_passes_test(is_teacher)
def savedraft(request):
    """
    Créé une nouvelle entrée dans la table ``QuizDraft``. Le brouillon est associé
    à l'utilisateur connecté et enregistre les valeurs données en paramètres pour
    les colonnes ``title`` et ``code``.
    
    Cette vue n'est disponible que si l'utilisateur connecté appartient au groupe
    'teachers'.
    
    **Paramètres de la requête HTTP POST\:**
    
    * ``title`` : Titre du brouillon
    * ``code`` : Code du quiz
    """
    if request.method == "POST":
        title = request.POST["title"]
        code = request.POST["code"]
        
        # Récupération des données du professeur dans la base de données
        # à partir de l'utilisateur connecté
        user = Teacher.objects.get(user=request.user)
        
        # Enregistrement dans la base de données
        draft = QuizDraft(title=title, code=code, id_teacher=user)
        draft.save()
        
        return HttpResponse(str(draft.pk))
        
@login_required
@user_passes_test(is_teacher)
def listdrafts(request):
    """
    Renvoie le titre et l'id de tous les brouillons de l'utilisateur connecté
    sous forme de json.
    
    **Exemple de json renvoyé dans le cas d'un professeur ayant
    enregistré deux brouillons \:**
    
    .. code-block:: json
    
        [
            {
                "title": "Brouillon 1",
                "id": 1
            },
            {
                "title": "Brouillon 2",
                "id": 2
            }
        ]
    
    Cette vue est essentiellement destinée à être utilisé par requête Ajax.
    """
    if request.method == "GET":
        # Récupération du professeur à partir des données de l'utilisateur connecté
        teacher_account = Teacher.objects.get(user=request.user)
        
        # Récupération de tous les quiz appartenant au professeur connecté
        drafts = QuizDraft.objects.filter(id_teacher=teacher_account)
        
        list_drafts = [] # Liste qui sera sérializée
        
        # Ajout de dictionnaires contenant les données des brouillons dans la liste
        for d in drafts:
            list_drafts.append({
                "title" : d.title,
                "id" : d.pk,
            })
            
        json_string = json.dumps(list_drafts) # Sérialisation de la liste
    
        return HttpResponse(json_string)

@login_required
@user_passes_test(is_teacher)
def getdraft(request):
    """
    Renvoie sous forme de json le titre et le code correspondant au brouillon en
    paramètre.
    
    Cette vue est essentiellement destinée à être utilisé par une requête Ajax.
    
    **Exemple de données d'un brouillon en json \:**
    
    .. code-block:: json
    
        {
            "title": "Brouillon 1",
            "code": "## Cases à cocher\\n * Option 1\\n= Option 4\\n= Option 5"
        }
    
    **Paramètres de la requête HTTP GET \:**
    
    * ``draft`` : Id du brouillon
    """
    if request.method == "GET":
        n_draft = request.GET['draft']
        
        draft = get_object_or_404(QuizDraft, pk=n_draft)
        teacher_account = Teacher.objects.get(user=request.user)
        
        # On contrôle que le brouillon appartient au professeur connecté
        if draft.id_teacher == teacher_account:
            # Construction d'un dictionnaire contenant les données du brouillon
            json_dict = {
                "title" : draft.title,
                "code" : draft.code,
            }
            json_string = json.dumps(json_dict) # Sérialisation du dictionnaire
            
            return HttpResponse(json_string)

@login_required
def correct(request, n_completed):
    """
    Récupère dans la base de données l'entrée de la table ``CompletedQuiz`` avec
    l'id ``n_completed`` et affiche une correction détaillée des réponses soumises
    par l'étudiant.
    
    L'objet ``CorrectQuiz`` regroupe et calcule toutes les informations nécessaires
    à l'affichage du quiz. Cet objet est ensuite placé dans le contexte de la fonctions
    ``render`` et fournit ainsi un accès facilité aux données de la correction depuis
    le template.
    """
    
    # Récupération de la résolution dans la base de données
    completed = get_object_or_404(CompletedQuiz, pk=n_completed)
    
    # Instanciation d'un objet CorrectQuiz qui contiendra toutes les informations
    # nécessaires à l'affichage de la correction
    correctquiz = CorrectQuiz(completed)
        
    return render(request, 'quiz/correct.html', {'correctquiz' : correctquiz, 'quiz' : completed.id_quiz})

@login_required
def completed_quizzes(request):
    """
    Récupère dans la base de données toutes les entrées de la table ``CompletedQuiz``
    appartenant à l'utilisateur connecté et affiche des informations générales comme
    le nombre de points obtenus et un lien pour afficher la correction des réponses.
    """
    # Récupération des résolutions de l'élève dans la db
    l_completed = CompletedQuiz.objects.filter(id_user=request.user)
    
    return render(request, 'quiz/completed-quizzes.html', {'l_completed' : l_completed})

@login_required
@user_passes_test(is_teacher)
def created_quizzes(request):
    """
    Récupère dans la base de données toutes les entrées de la table ``Quiz`` créées
    par le professeur connecté. Les données des quiz sont utilisées pour afficher
    le résultat moyen des étudiants pour le quiz, la date de création ainsi qu'un lien vers la page de
    résolution du quiz ou vers les statistiques avancées.
    """
    # Récupération des quiz créés par le prof dans la db
    teacher = Teacher.objects.get(user=request.user)
    l_created = Quiz.objects.filter(id_teacher=teacher)
    
    return render(request, 'quiz/created-quizzes.html', {'l_created' : l_created})
    
@login_required
@user_passes_test(is_teacher)
def advanced_stats(request, n_quiz):
    """
    Récupère toutes les résolutions associés au quiz avec l'id ``n_quiz`` et affiche
    des statistques précises montrant le résultat personnel des élèves pour chaque question.
    
    Un objet ``QuizForms`` qui créé des formulaires Django pour toutes les question
    du quiz est instancié pour permettre au professeur de visionner 
    chaque question du quiz. Ce formulaire ne peut pas être envoyé et sert
    uniquement à l'affichage.
    """
    quiz = get_object_or_404(Quiz, pk=n_quiz)
    l_completed = CompletedQuiz.objects.filter(id_quiz=quiz)
    
    # Création d'un formulaire pour pouvoir afficher le rendu des questions
    # dans le template
    quizforms = QuizForms(quiz)
    
    return render(request, 'quiz/advanced-stats.html', {'quiz' : quiz, 'l_completed' : l_completed, 'l_forms' : quizforms.get_forms()})