#########################
Documentation utilisateur
#########################

***********
Professeurs
***********

================
Création de quiz
================

.. figure:: figures/create-doc.png
    :align: center
    
----------------------------------------------------
Création d'une question et définition de ses caractéristiques
----------------------------------------------------

La création du quiz se fait par l'intermédiaire d'un langage de balisage de type Markdown pour définir les différentes questions du quiz ainsi que leurs caractéristiques. La définition des questions se fait selon le schéma suivant : la première ligne du paragraphe sert à indiquer le type de question et l'énoncé, alors que les lignes suivantes décrivent les solutions ou options possibles ainsi que d'autres paramètres, comme le nombre de points attribués pour la question. Un double retour à la ligne marque le passage à la question suivante. 

Au début de chaque ligne, une balise suivie d'un espace indique la fonction de la ligne en question.

^^^^^^^^^^^^^^^^^^^^^^^
Explication des balises
^^^^^^^^^^^^^^^^^^^^^^^

+--------+-----------------------------------------------------------------------------+
| Balise | Signification                                                               |
+========+=============================================================================+
| ##     | Question à choix multiple avec plusieurs options qui peuvent être choisies  |
+--------+-----------------------------------------------------------------------------+
| \*\*   | Question à choix multiple avec une seule option qui peut être choisie       |
+--------+-----------------------------------------------------------------------------+
| ??     | Question avec un champ de texte à remplir                                   |
+--------+-----------------------------------------------------------------------------+
| \*     | Option invalide dans un QCM                                                 |
+--------+-----------------------------------------------------------------------------+
| =      | Option valide dans un QCM                                                   |
+--------+-----------------------------------------------------------------------------+
| =      | Réponse correcte dans une question à champ de texte                         |
+--------+-----------------------------------------------------------------------------+
| .      | Permet de définir le nombre de points sur la question (par défaut, 1)       |
+--------+-----------------------------------------------------------------------------+
| \+     | Ajout d'un commentaire d'explication qui sera affiché lors de la correction |
+--------+-----------------------------------------------------------------------------+

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Exemple de quiz avec le système de balisage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text
    
    ## Énoncé de la question à choix multiple (plusieurs cases peuvent être cochées)
    * Option 1
    = Option 2 (correcte)
    = Option 4 (correcte)
    + Commentaire affiché à la correction
    . 1.5
    
    ** Énoncé de la question à choix multiple (une seule case peut être cochée)
    * Option 1
    * Option 2
    = Option 3 (correcte)
    . 2
    
    ?? Question à réponse courte
    = Réponse correcte
    = Autre réponse correcte possible
    
Pour la première question, la balise ``##`` indique qu'il s'agit d'une question à choix multiple avec plusieurs réponses possibles, alors qu'une option incorrecte et deux options correctes sont respectivement définies avec les balises ``*`` et ``=``. Ensuite, on a ajouté un commentaire avec ``+`` et défini le nombre de points avec le symbole ``.``. Il est important de retenir que toutes les balises sont suivies d'un espace, sans quoi elles ne sont pas reconnues.

La barre d'outils située en dessus de la zone de texte offre la possibilité de créer un quiz sans maîtriser le système de balisage. Pour ajouter une question, il suffit de cliquer sur l'onglet *Question* et de choisir le type de question souhaité dans le menu déroulant. La balise est insérée automatiquement et il n'y a plus qu'à écrire l'énoncé de la question. Il en va de même pour ajouter des solutions ou des options avec les boutons *Correct* et *Incorrect*. Les retours à la lignes et les espaces sont placés automatiquement avant et après la balise si cela est nécessaire. Le menu *Autres* permet de choisir le nombre de points à attribuer pour chaque question et d'écrire un commentaire destiné à être affiché lors de la correction automatique du quiz. Ce commentaire est censé apporter une justification à la solution de la question ou une aide pour les élèves n'ayant pas répondu correctement.

^^^^^^^^^^^^^^^^^^
Types de questions
^^^^^^^^^^^^^^^^^^

"""""""""""""""""""""""""
Question à réponse courte
"""""""""""""""""""""""""

La question à réponse courte se présente sous la forme d'un simple champ de texte à compléter. La balise caractérisant ce type de questions est la balise ``??``. Ensuite, une ou plusieurs réponses peuvent être définies comme correctes à l'aide de la balise ``=``. S'il y a plusieurs solutions, elles doivent être séparées par un retour à la ligne et chacune doit être précédée de la balise ``=``. Si la réponse donné par l'élève correspond exactement à une des solutions, il obtient tous les points. Il est conseillé de ne pas définir des solutions complexes ou trop longues pour éviter de compter comme une erreur l'absence de virgule, de point ou d'un autre caractère spécial.

IMAGE ICI

""""""""""""""""""""""""""""""""""""""""""""""""""""
Question à choix multiples avec un seul choix valide
""""""""""""""""""""""""""""""""""""""""""""""""""""

Pour ce type, plusieurs options sont affichées et l'élève ne peut en sélectionner qu'une. La balise associé à ce type est la balise ``**``. Une seule option valide doit donc être définie avec la balise ``=``, toutes les autres doivent être erronnées et donc précédées par la balise ``*``. L'élève reçoit tous les points s'il sélectionne la bonne solution, et aucun point dans tous les autres cas.

IMAGE ICI

""""""""""""""""""""""""""""""""""""""""""""""""""""
Question à choix multiples avec un seul choix valide
""""""""""""""""""""""""""""""""""""""""""""""""""""

Définie par la balise ``##``, il s'agit d'une question semblable à la précédente mais l'élève a cette fois la possibilité de choisir plusieurs options. Les options qui doivent être sélectionnées sont définies avec la balise ``=`` et les autres avec la balise ``*``. Le professeur doit cependant définir au moins une option correcte. Lors de la correction, l'élève peut obtenir des points pour un choix qu'il a coché et que le professeur a défini comme correct et inversément, c'est à dire qu'il peut aussi gagner des points sur un choix qui n'est pas sélectionné, à condition qu'il soit défini comme erronné.

IMAGE ICI

------------------------------------
Affichage de l'aperçu et des erreurs
------------------------------------

Il est possible à tout moment d'afficher un rendu du quiz tel que le verront les étudiants en cliquant sur le bouton *Aperçu* en dessous de la zone de texte. On peut ainsi voir si toutes les questions s'affichent comme prévu et également détecter les éventuelles erreurs dans le code. Ces erreurs s'affichent dans l'encadré rouge en dessous du bouton *Aperçu*. Pour chaque erreur, un message explicatif apparaît accompagné du numéro de ligne où s'est produite l'erreur.

IMAGE EXEMPLE

Dans cet exemple, on a tenté d'utiliser la balise ``*=``, qui n'existe pas. C'est pourquoi on obtient le message suivant : *Balise inconnue*.

Un quiz ne peut pas être envoyé et enregistré dans la base de données tant qu'il comporte encore des erreurs. C'est pourquoi elles doivent être impérativement corrigés pour valider l'envoi lors du cliq sur le bouton *Enregistrer*.

--------------------------
Affichage de mathématiques
--------------------------

Il est possible d'afficher des formules mathématiques à l'aide de la bibliothèque Javascript MathJax. Cet outil permet d'écrire des expressions sous forme de LaTex et de les convertir en HTML pour qu'elles soient visibles dans le navigateur. Il existe deux méthodes d'affichage proposées par MathJax : la méthode *in-line* et la méthode *displayed*. La première méthode offre la possibilité d'inclure une formule dans un paragraphe de texte. Les formules en *in-line* doivent être entourées des caractères suivants : ``\(...\)``. Avec la méthode *displayed*, les expressions sont affichées en plus grand, centrées et détachées du reste du texte. Les formules utilisant cette méthode sont délimitées par les balises ``$$...$$``.

La barre d'outils propose un menu dédié à l'affichage des mathématiques. Deux boutons permettent d'insérer les délimiteurs des méthodes *in-line* et *displayed* et d'autres options pour afficher un échantillon de formules et de symboles sont disponibles. Cette liste est toutefois non-exhaustive et il est conseillé de se référer à la documentation de LaTex [#latex-doc] pour obtenir des informations plus précises à ce sujet.

-------------------------------------------
Enregistrement et importation de brouillons
-------------------------------------------

-----------------------
Envoi définitif du quiz
-----------------------


Voici un exemple de quiz comprenant 4 questions :

.. code-block:: text
    
    ## Énoncé de la question à choix multiple (plusieurs cases peuvent être cochées)
    * Option 1
    * Option 2 (correcte)
    * Option 3
    * Option 4 (correcte)
    + Commentaire affiché à la correction
    . 1.5
    
    ** Énoncé de la question à choix multiple (une seule case peut être cochée)
    * Option 1
    * Option 2
    * Option 3 (correcte)
    . 2
    
    ^^ Liste déroulante
    * Option 1
    * Option 2 (correcte)
    * Option 3
    * Option 4
    
    ?? Question à champ de texte
    * Réponse correcte
    * Autre réponse correcte possible
    
Lorsque le professeur appuie sur le bouton *Aperçu*, il peut voir le rendu du quiz tel que le verront les étudiants. Les éventuelles erreurs dans le code (tag qui n'existe pas, etc.) sont affichés en rouge en dessous de l'aperçu. Le quiz ne peut pas être enregistré tant qu'il y a encore des erreurs dans le code. S'il commence à créer un quiz et désire le terminer plus tard, le professeur peut enregistrer un brouillon. L'outil de création de quiz supporte l'affichage des mathématiques avec MathJax (http://www.mathjax.org/).

Le prof doit également donner un titre au quiz et peut le relier à un ou plusieurs chapitres. Il décide de restreindre l'accès aux membres d'un ou plusieurs groupes ou de le rendre public. Pour créer un quiz, un prof a aussi la possibilité de reprendre un quiz déjà existant et de modifier son code. S'il opte pour cette solution, les statistiques du nouveau quiz ainsi créé repartent à zéro, puisque les questions ne sont plus forcément les mêmes.

================
Suivi des élèves
================

--------------------------------------
Liste des quiz créés par un professeur
--------------------------------------

-----------------------------------
Affichage des statistiques avancées
-----------------------------------

----------------------------
Consultation des corrections
----------------------------

*********
Étudiants
*********

===============
Trouver un quiz
===============

.. figure:: figures/find.png
    :align: center

Pour trouver un quiz, un étudiant a plusieurs possibilités. Le professeur peut donner l'url exacte du quiz à compléter, ce qui peut être pratique dans un e-mail ou toute communicaton informatisée. Une fonctionnalité permet au utilisateurs de générer un code QR correspondant à un quiz, ce qui est idéal pour afficher sur un projecteur en classe ou sur une feuille imprimée. Un étudiant peut aussi accéder à un quiz en mémorisant son id et en l'entrant dans la champ prévu à cet effet sur la page "Trouver un quiz".

Dans son espace utilisateur, l'étudiant peut aussi consulter les derniers quizs créés dans son groupe et peut donc y accéder facilement (fonctionnalité externe à l'application).

===========================================
Compléter un quiz et correction automatique
===========================================

Une fois que l'étudiant à accédé au quiz, il peut le compléter très simplement en remplissant les champs de formulaires affichés. Lorsqu'il a fini, il peut soumettre ses réponses et il est redirigé vers une page de correction. Les réponses incorrectes sont affichées en rouge avec la solution et une explication pour chaque question. Les points reçus pour chaque question sont affichés avec le total de points sur le quiz. L'étudiant peut aussi comparer son score à la moyenne des autres étudiants du groupe. Un champ de texte est disponible pour envoyer des éventuelles remarques au professeur (signaler une erreur, poser une question). La page pour compléter un quiz ainsi que celle de la correction sont optimisées pour mobile et le design responsive s'adapte parfaitement à tous types de périphériques (ordinateur de bureau, ordinateur portable, tablette, téléphone mobile).

.. figure:: figures/complete.png
    :align: center
    
===============
Suivi personnel
===============