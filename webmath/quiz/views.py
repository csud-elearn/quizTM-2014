import json

from django.http import JsonResponse

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404

from common.models import Teacher, Student, Class
from common.auth_utils import *

from quiz.utils.save import SaveQuiz
from quiz.utils.submit import QuizForms
from quiz.models import Quiz, QuizDraft, CompletedQuiz, SqSubmit, QcmSubmitMulti, QcmSubmitOne


@login_required
@user_passes_test(is_teacher)
def create(request):
    """
    Cette vue sert à la fois à l'affichage de l'outil de création de quiz et à
    l'enregistrement de nouveaux quiz.

    S'il s'agit d'une requête HTTP GET, elle renvoie simplement le template de
    création de quiz contenant un formulaire vide.

    Au contraire, si la requête HTTP est de type POST, la vue se charge d'enregistrer
    le nouveau quiz dans la base de données en instanciant un objet de la classe
    :py:class:`.utils.save.SaveQuiz` avec en argument les paramètres de la requête HTTP et le compte
    utilisateur du créateur du quiz. Cette
    classe se charge ensuite de créer les entrées nécessaires dans les différentes tables de
    la base de données.

    Une fois le quiz enregistré, la vue redirige l'utilisateur vers la page de
    résolution du quiz qui vient d'être créé.

    **Paramètres de la requête HTTP POST \:**

    * ``title`` : Le titre du quiz
    * ``tags`` : liste des tags au format JSON
    * ``json`` : Les données des questions du quiz structurées sous forme de json. Le json sera ensuite parsé par la classe ``SaveQuiz``.
    * ``quizcode`` : Le format texte du quiz, interprété côté client pour construire le json
    """
    if request.method == 'POST':
        json_string = request.POST['json'] #Chaîne json contenant toutes les données des questions du quiz
        title = request.POST['title']
        quizcode = request.POST['quizcode'] #Code (format texte) du quiz
        # liste des tags au format JSON
        tags_list = json.loads(request.POST.get('tags_list', '[]'))
        print('liste de tags pour le quiz:', tags_list)


        # pour chaque tag qui n'est pas déjà dans la table des tags, il faut
        #créer une entrée dans la table des tags. Pour les entrées existantes,
        #il faut rajouter un lien avec le quiz que nous sommes en train de créer


        questions_list = json.loads(json_string) #Parsing du json

        teacher_account = Teacher.objects.get(user=request.user) #Compte prof correspondant à l'user

        quiz = SaveQuiz(title, questions_list, quizcode, teacher_account, tags_list) #Sauvegarde du quiz dans la db

        # création et mise à jour des tags

        # Redirection vers la page de résolution du quiz créé
        return HttpResponseRedirect(reverse("quiz:complete", args=[quiz.quiz_db.pk]))
    else:
        return render(request, 'quiz/create.html')

@login_required
def complete(request, n_quiz):
    """
    Cette vue est destinée à la résolution des quiz. Comme ``create``, son comportement
    change selon qu'il s'agisse d'une requête HTTP de type GET ou de type POST.

    Dans le cas d'une requête de type GET, la vue se contente de récupérer le quiz
    avec la clé primaire ``n_quiz`` et d'instancier un objet :py:class:`utils.submit.QuizForms` à partir
    du quiz sélectionné. Cet objet prend en charge la création de tous les formulaires
    Django nécessaires pour compléter le quiz (un formulaire Django par question).
    Ces formulaires Django sont ensuite récupérés par l'intermédiaire de la méthode
    ``.get_forms()`` et placés dans le contexte de la fonction ``render()``.

    La requête de type POST est utilisée pour l'enregistrement des réponses soumises
    au quiz par un étudiant. Là aussi, on utilise la classe ``QuizForms``, sauf que
    l'instanciation se fait avec un deuxième argument, ``data``. Cet argument contient
    en fait les données soumises par le biais des formulaires Django lorsqu'un
    étudiant complète le quiz. Pour s'assurer de la validité de ces données, on
    utilise la méthode ``.are_valid()`` de la classe ``QuizForms``. Une fois le
    contrôle effectué, la méthode ``.save_answers()`` se charge d'ajouter de nouvelles
    entrées dans la base de donnée pour stocker les réponses soumises par l'étudiant.
    Pour finir, l'utilisateur est redirigé vers la page de correction correspondant
    aux réponses envoyées précédemment.

    **Paramètres de la requête HTTP POST \:**

    * Ces paramètres dépendent du type et du nombre de questions qui constituent le quiz.
    """
    # Si la requête est de type POST, on créer un nouveau formulaire et on le remplit avec les données de requête
    if request.method == 'POST':
        quiz = Quiz.objects.get(id=n_quiz) #Récupération du quiz sélectionné dans la base de donnée

        quizforms = QuizForms(quiz, data=request.POST)

        #On controle que les formulaires sont valides
        if quizforms.are_valid():

            #Les réponses sont enregistrées dans la db par l'intermédiaire de la méthode .save_answers()
            completed = quizforms.save_answers(request.user)

            return HttpResponseRedirect(reverse("quiz:correct", args=[completed.pk]))

    # Si la requête est de type GET, on affiche un formulaire vide
    else:
        quiz = get_object_or_404(Quiz, id=n_quiz) #Récupération du quiz dans la db

        quizforms = QuizForms(quiz)

        return render(
            request, 'quiz/complete.html',
            {'quiz': quiz, 'l_forms': quizforms.l_forms}
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
    Renvoie sous forme de json le titre et l'url pour accéder au quiz dont la clé primaire est donnée
    en paramètre de la requête GET.

    L'url du quiz est construite à l'aide de la méthode ``reverse(vue, arguments)``
    fournie par Django.
    Le premier argument de la fonction ``reverse()`` est une chaîne de caractère composée du nom de l'application Django
    et du nom de la vue (dans les urls) respectant le schéma suivant :
    ``"nom_app:nom_vue"``. L'argument ``args`` est une liste contenant les arguments
    de l'URL de la page souhaitée. Ici, il s'agit simplement de la clé primaire du quiz recherché.

    Cette vue est essentiellement destinée à être utilisé par une requête Ajax
    depuis la vue ``find``.

    **Exemple de json renvoyé par la vue \:**

    .. code-block:: json

        {
            "title": "Un quiz sympathique",
            "url": "/quiz/1/complete/"
        }

    **Paramètres de la requête HTTP GET \:**

    * ``quiz`` : Clé primaire du quiz recherché
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

        return JsonResponse(json_dict)

@login_required
@user_passes_test(is_teacher)
def savedraft(request):
    """
    Créé une nouvelle entrée dans la table ``QuizDraft``. Le brouillon est associé
    à l'utilisateur connecté et enregistre les valeurs données en paramètres pour
    les colonnes ``title`` et ``code``.

    Cette vue n'est disponible que si l'utilisateur connecté appartient au groupe
    'teachers'.

    **Paramètres de la requête HTTP POST \:**

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
    Renvoie le titre et la clé primaire de tous les brouillons de l'utilisateur connecté
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

        # Pour encoder des listes, safe doit valoir False
        return JsonResponse(list_drafts, safe=False)

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

    * ``draft`` : Clé primaire du brouillon
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

            return JsonResponse(json_dict)

@login_required
def correct(request, n_completed):
    """
    Récupère dans la base de données l'entrée de la table ``CompletedQuiz`` avec
    la clé primaire ``n_completed`` et affiche une correction détaillée des réponses soumises
    par l'étudiant.

    On parcourt ensuite la liste des réponses soumises à chaque question et on appelle
    la méthode ``.build_correct()`` qui instancie des objets contenant les données
    à afficher pour la correction.
    """

    # Récupération de la résolution dans la base de données
    completed = get_object_or_404(CompletedQuiz, pk=n_completed)

    # Instanciation d'un objet CorrectQuiz qui contiendra toutes les informations
    # nécessaires à l'affichage de la correction
    # correctquiz = CorrectQuiz(completed)

    l_corrections = []

    # Pourcentage de réussite du quiz pour la barre de progression
    success_prct = int(completed.result / completed.id_quiz.points * 100)
    average_prct = int(completed.id_quiz.average_result() / completed.id_quiz.points * 100)

    for submit in completed.get_questions_submits():
        l_corrections.append(submit.build_correct())

    return render(request, 'quiz/correct.html', {
        'completed' : completed,
        'quiz' : completed.id_quiz,
        'l_corrections' : l_corrections,
        'success_prct' : success_prct,
        'average_prct' : average_prct,
    })

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
    Récupère toutes les résolutions associées au quiz avec la clé primaire ``n_quiz`` dans la base de données et affiche
    des statistiques précises montrant le résultat personnel des élèves pour chaque question.

    Un objet ``QuizForms`` qui créé des formulaires Django pour toutes les questions
    du quiz est instancié pour permettre au professeur de visionner
    chaque question du quiz. Ce formulaire ne peut pas être envoyé et sert
    uniquement à l'affichage.
    """

    quiz = get_object_or_404(Quiz, pk=n_quiz)
    l_completed = CompletedQuiz.objects.filter(id_quiz=quiz)

    n_completed = len(l_completed)

    # Création d'un formulaire pour pouvoir afficher le rendu des questions
    # dans le template
    quizforms = QuizForms(quiz)

    # classes appartenant à teacher
    classes = Class.objects.filter(owner=request.user)

    return render(request, 'quiz/advanced-stats.html', {
        'quiz' : quiz,
        'l_completed' : l_completed,
        'l_forms' : quizforms.l_forms,
        'n_completed' : n_completed,
        'classes' : classes,
    })

@login_required
@user_passes_test(is_teacher)
def add_correct_answer(request):
    """
    Cette fonctionnalité donne la possibilité de définir comme correcte une réponse
    soumise par l'étudiant à une question courte et de l'ajouter aux solutions de
    la question en créant une nouvelle entrée dans la table ``SqAnswer``.

    Cette vue n'est utilisée que par l'intermédiaire d'une requête Ajax et n'est
    accessible que si l'utilisateur est un professeur.

    **Paramètres de la requête HTTP POST \:**

    * ``answer`` : Clé primaire de l'entrée dans la table ``SqSubmit`` qui doit être ajoutée aux solutions.
    """
    if request.method == "POST":
        submit = SqSubmit.objects.get(pk=request.POST["answer"])
        submit.set_as_correct()

        return HttpResponse(submit.pk)


@login_required
@user_passes_test(is_teacher)
def ls_classes(request):
    teacher = request.user

    # retourne toutes les classes dont possédées par teacher
    classes = Class.objects.filter(owner=teacher)

    return render(request, 'quiz/classes.html', { 'classes': classes })
