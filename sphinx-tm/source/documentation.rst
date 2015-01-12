##############################
Documentation de l'application
##############################

*******************************
Description des fonctionnalités
*******************************

===========
Professeurs
===========

----------------
Création de quiz
----------------

Les professeurs peuvent créer un quiz en utilisant un format texte de type markdown pour créer différents types de questions et y attribuer certaines caractéristiques. Cet éditeur de quiz se présente se présente sous la forme d'une zone de texte dans laquelle le professeur peut entrer le code du quiz. Au début de chaque ligne, le prof entre un tag, chaque tag a une signification différente. Chaque tag doit être séparé de la suite de la ligne par un espace

+-----+-----------------------------------------------------------------------------+
| Tag | Signification                                                               |
+=====+=============================================================================+
| ##  | Question à choix multiple avec plusieurs options cochables                  |
+-----+-----------------------------------------------------------------------------+
| \*\*| Question à choix multiple avec une seule option cochable                    |
+-----+-----------------------------------------------------------------------------+
| ^^  | Liste déroulante avec une option sélectionnable                             |
+-----+-----------------------------------------------------------------------------+
| ??  | Question avec un champ de texte à remplir                                   |
+-----+-----------------------------------------------------------------------------+
| \*  | Option invalide dans un QCM                                                 |
+-----+-----------------------------------------------------------------------------+
| =   | Option valide dans un QCM                                                   |
+-----+-----------------------------------------------------------------------------+
| =   | Réponse correcte dans une question à champ de texte                         |
+-----+-----------------------------------------------------------------------------+
| .   | Permet de définir le nombre de points sur la question (par défaut, 1)       |
+-----+-----------------------------------------------------------------------------+
| \+  | Ajout d'un commentaire d'explication qui sera affiché lors de la correction |
+-----+-----------------------------------------------------------------------------+


Voici un exemple de quiz comprenant 4 questions :

.. code-block:: text
    
    ## Énoncé de la question à choix multiple (plusieurs cases peuvent être cochées)
    * Option 1
    = Option 2 (correcte)
    * Option 3
    = Option 4 (correcte)
    + Commentaire affiché à la correction
    . 1.5
    
    ** Énoncé de la question à choix multiple (une seule case peut être cochée)
    * Option 1
    * Option 2
    = Option 3 (correcte)
    . 2
    
    ^^ Liste déroulante
    * Option 1
    = Option 2 (correcte)
    * Option 3
    * Option 4
    
    ?? Question à champ de texte
    = Réponse correcte
    = Autre réponse correcte possible
    
Lorsque le professeur appuie sur le bouton "Aperçu", il peut voir le rendu du quiz tel que le verront les étudiants. Les éventuelles erreurs dans le code (tag qui n'existe pas, etc.) sont affichés en rouge en dessous de l'aperçu. Le quiz ne peut pas être enregistré tant qu'il y a encore des erreurs dans le code. S'il commence à créer un quiz et désire le terminer plus tard, le professeur peut enregistrer un brouillon. L'outil de création de quiz supporte l'affichage des mathématiques avec MathJax (http://www.mathjax.org/).

Le prof doit également donner un titre au quiz et peut le relier à un plusieurs chapitres. Il décide de restreindre l'accès aux membres d'un ou plusieurs groupes ou de le rendre public. Pour créer un quiz, un prof a aussi la possibilité de reprendre un quiz déjà existant et de modifier son code. S'il opte pour cette solution, les statistiques du nouveau quiz ainsi créé repartent à zéro, puisque les questions ne sont plus forcément les mêmes.

--------------------------------------
Consultation des statistiques avancées
--------------------------------------

Après que les élèves d'un groupe ont complété un quiz, le professeur peut afficher le résultat moyen des élèves, le % de réussite à chaque question, mais aussi les réponses soumises par chaque élève en particulier. Le prof peut ainsi se faire une idée globale et plus cibleé du niveau de compréhension de son groupe.

=========
Étudiants
=========

---------------
Trouver un quiz
---------------

Pour trouver un quiz, un étudiant a plusieurs possibilités. Le professeur peut donner l'url exacte du quiz à compléter, ce qui peut être pratique dans un email ou toute communicaton informatisée. Une fonctionnalité permet au utilisateurs de générer un code QR correspondant à un quiz, ce qui est idéal pour afficher sur un projecteur en classe ou sur une feuille imprimée. Un étudiant peut aussi accéder à un quiz en mémorisant son id et en l'entrant dans la champ prévu à cet effet sur la page "Trouver un quiz".

Dans son espace utilisateur, l'étudiant peut aussi consulter les derniers quizs créés dans son groupe et peut donc y accéder facilement.

-------------------------------------------
Compléter un quiz et correction automatique
-------------------------------------------

Une fois que l'étudiant à accédé au quiz, il peut le compléter très simplement en remplissant les champs de formulaires affichés. Lorsqu'il a fini, il peut soumettre ses réponses et est redirigé vers une page de correction. Les réponses incorrectes sont affichées en rouge avec la solution et une explication pour chaque question. Les points reçus pour chaque question sont affichés avec le total de points sur le quiz. L'étudiant peut aussi comparer son score à la moyenne des autres étudiants du groupe. Un champ de texte est disponible pour envoyer des éventuelles remarques au professeur (signaler une erreur, poser une question). La page pour compléter un quiz ainsi que celle de la correction sont optimisées pour mobile et le design responsive s'adapte parfaitement à tous types de périphériques (desktop, portable, tablette, téléphone mobile).

********************
Guide du programmeur
********************

******************************************************
Diagrammes de classes et organisation générale du code
******************************************************

************************************
Explication des parties clés du code
************************************