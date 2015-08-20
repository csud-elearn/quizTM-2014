#######################################
Fonctionnement général de l'application
#######################################

***
URL
***

Cette section définit les différents chemins d'accès aux pages de l'application. Certaines URL comportent des paramètres,
qui sont indiqués entre **<...>**. Les vues Django correspondant à chaque URL sont affichées entre parenthèses.

* **(find) \:** Page d'accueil de l'application. Les étudiants peuvent voir les derniers quiz publiés ou en rechercher un.
* **/create/ (create) \:** Page de l'outil de création de quiz.
* **/<id-quiz>/complete/ (complete) \:** Page qui permet aux étudiants de répondre à un quiz et de soumettre leurs réponses.
* **/<id-résolution>/correct/ (correct) \:** Affichage de la correction d'une résolution. C'est là qu'est redirigé l'utilisateur après avoir complété un quiz
* **/completed-quizzes/ (completed_quizzes) \:** Historique des résolutions effectuées par l'élève.
* **/created-quizzes/ (created-quizzes) \:** Liste des quiz créés par le professeur. C'est depuis cette page qu'il peut accéder aux statistiques avancées d'un quiz.
* **/<id-quiz>/advanced-stats/ \:** Affichage des statistiques avancées de toutes les résolutions d'un quiz.

D'autres URL sont utilisées uniquement par des requêtes Ajax, c'est à dire que l'utilisateur ne les voit jamais :

* **/findquiz/ (findquiz) \:** Renvoie l'URL du quiz correspondant à la clé primaire du quiz fournie dans les paramètres de la requête HTTP si celui-ci existe.
* **/savedraft/ (savedraft) \:** Permet l'enregistrement dans la base de données d'un brouillon.
* **/listdrafts/ (listdrafts) \:** Récupère la liste des brouillons appartenant à l'utilisateur.
* **/getdraft/ (getdraft) \:** Récupère les données sur le brouillon dont la clé primaire est fournie dans les paramètres de la requête HTTP.
* **/add-correct-answer/ (add_correct_answer) \:** Pour une question à réponse courte, permet d'ajouter une réponse soumise aux solutions de la question

Voici comment sont définies ces URL dans Django :

.. code-block :: python
    
    from django.conf.urls import patterns, url

    from quiz.views import *
    
    urlpatterns = patterns('',
        # URL des pages de l'application
        url(r'^$', find, name="find"),
        url(r'^create/$', create, name="create"),
        url(r'^(\d+)/complete/', complete, name="complete"),
        url(r'^(\d+)/correct/', correct, name="correct"),
        url(r'^completed-quizzes/', completed_quizzes, name="completed-quizzes"),
        url(r'^created-quizzes/', created_quizzes, name="created-quizzes"),
        url('^(\d+)/advanced-stats/', advanced_stats, name="advanced-stats"),
        # URL destinées à l'Ajax
        url(r'^findquiz/', findquiz, name="findquiz"),
        url(r'^savedraft/', savedraft, name="savedraft"),
        url(r'^listdrafts/', listdrafts, name="listdrafts"),
        url(r'^getdraft/', getdraft, name="getdraft"),
        url(r'^add-correct-answer/', add_correct_answer, name="add-correct-answer"),
    )
    
Chaque URL est définie à l'aide de la fonction ``url()``. Cette fonction prend trois arguments : une expression régulière qui
caractérise l'URL, la référence de la fonction correspondante dans les vues ainsi que le nom de l'URL, qui pourra être utilisé
avec la fonction ``reverse()`` pour construire un lien vers une page de l'application.

******************************************
Organisation des fichiers de l'application
******************************************

Ce chapitre décrit tous les dossiers et fichiers importants de l'application ainsi que leur rôle dans le fonctionnement du site.

* **admin.py \:** Fichier qui permet de personnaliser l'interface d'administration de l'application.
* **forms.py \:** Définit les formulaires Django personnalisés utilisés dans l'application.application.
* **models.py \:** Décrit les modèles de l'application, c'est à dire les tables de la base de données.
* **urls.py \:** Définit les chemins d'accès pour les différentes pages de l'application.
* **views.py \:** Les vues Django de l'application, c'est à dire un ensemble de fonctions qui définissent les actions à réaliser lorsqu'un utilisateur tente d'accéder à une page.
* **migrations/ \:** Ce dossier contient des fichiers Python générés par Django qui gèrent les modifications apportées aux tables de la base de données.
* **rs-source/ \:** Dossier contenant tout le code écrit en RapydScript utilisé dans l'application.

    * **find_url.pyj \:** Gère la requête Ajax pour rechercher un quiz à compléter.
    * **interpreter.pyj \:** Permet d'interpréter le code de l'outil de création de quiz pour structurer les données du quiz en JSON.
    * **Makefile \:** Définit des raccourcis pour la compilation des fichiers RapydScript
    * **toolbar.pyj \:** Implémente les différentes fonctionalités de la barre d'outils de la page de création de quiz.
* **static/quiz/ \:** Contient tous les fichiers statiques de l'application

    * **css/ \:** Fichiers CSS
    
        * **awesome-checkbox/ \:** Répertoire contenant les fichiers du plugin `Awesome Bootstrap Checkbox <https://github.com/flatlogic/awesome-bootstrap-checkbox>`_ [#1]_ pour mettre en forme les boutons radio et les cases à cocher.
        * **create.css \:** Feuille de style spécifique à la page de création de quiz
        * **shop-item.css \:** Feuille de style relative au template `Shop Item <http://startbootstrap.com/template-overviews/shop-item/>`_ [#2]_ utilisé dans toute l'application.
        * **stas.css \:** Feuille de style spécifique à la page de statistiques avancées.
        * **style.css \:** Feuille de style qui s'applique à l'ensemble de l'application.
        * **github-markdown.css \:** Feuille de style pour mettre en forme le HTML généré à partir du Markdown de manière similaire à Github [#10]_
        * **showdown.js \:** Fichier de la bibliothèque Javascript Showdown [#9]_
    * **js/ \:** Fichiers Javascript
    
        * **rs-compiled/ \:** Dossier contenant les fichiers RapydScript compilés.
        * **jquery.caret.js \:** Plugin `jQuery Caret <https://github.com/acdvorak/jquery.caret>`_ [#3]_ pour récupérer la position du curseur dans une zone de texte.
        * **stats.js \:** Définit une requête Ajax pour ajouter des solutions à une question dans la page de statistiques.
        * **textarea_lines.js \:** Script pour afficher les numéros de ligne dynamiquement dans une zone de texte.
        * **utils.js \:** Fichier comportant différentes fonctions utiles à différents endroits de l'application.
        
* **templates/quiz/ \:** Dossier contenant les gabarits de l'application. Hormis **base.html**, chaque fichier de ce répertoire correspond à la vue Django du même nom.

    * **base.html \:** Gabarit global de l'application dont héritent tous les autres gabarits.
    
* **utils/ \:** Contient des modules Python utilisés dans les vues.

    * **correct.py \:** Définit des objets utiles pour l'affichage de la correction.
    * **save.py \:** Gère l'enregistrement des quiz dans la base de données.
    * **submit.py \:** Gère la sauvegarde des réponses soumises à un quiz par un étudiant.
    
*****************************************************
Bibliothèques et frameworks utilisés dans l'application
*****************************************************

Voici la liste des outils provenant de sources extérieures utilisés dans le projet

* Django [#4]_ : framework Python pour créer des sites web dynamiques.
* RapydScript [#5]_ : outil pour compiler du Python en Javascript.
* Bootstrap [#6]_ : framwork CSS pour avoir un affichage correct très rapidement.
* jQuery [#7]_ : bibliothèque Javascript pour les manipulations dans le DOM, requêtes Ajax, etc.
* MathJax [#8]_ : bibliothèque Javascript permettant l'affichage de mathématiques.
* Awesome Bootstrap Checkbox [#1]_ : feuille de style pour les cases à cocher et les boutons radio.
* jQuery Caret [#3]_ : plugin jQuery pour récupérer la position du curseur dans une zone de texte.
* Shop Item [#2]_ : gabarit bootstrap utilisé dans toute l'application.
* Showdown [#9]_ : bibliothèque Javascript pour générer du HTML à partir de Markdown.
* Github Markdown CSS [#10]_ : Feuille de style pour mettre en forme le HTML généré à partir du Markdown de manière similaire à Github.
* Google Code Prettify [#11]_ : script pour la coloration syntaxique du code affiché avec le Markdown.
    
.. [#1] https://github.com/flatlogic/awesome-bootstrap-checkbox. Consulté le 29 mars 2015.
.. [#2] http://startbootstrap.com/template-overviews/shop-item/. Consulté le 29 mars 2015.
.. [#3] https://github.com/acdvorak/jquery.caret. Consulté le 29 mars 2015.
.. [#4] https://djangoproject.com. Consulté le 29 mars 2015.
.. [#5] http://rapydscript.pyjeon.com/. Consulté le 29 mars 2015.
.. [#6] http://getbootstrap.com/. Consulté le 29 mars 2015.
.. [#7] https://jquery.com/. Consulté le 29 mars 2015.
.. [#8] http://www.mathjax.org/. Consulté le 29 mars 2015.
.. [#9] https://github.com/showdownjs/showdown. Consulté le 17 mai 2015.
.. [#10] https://github.com/sindresorhus/github-markdown-css. Consulté le 17 mai 2015.
.. [#11] https://github.com/google/code-prettify. Consulté le 17 mai 2015.