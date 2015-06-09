#########################
Documentation utilisateur
#########################

***********
Professeurs
***********

================
Création de quiz
================

.. _create_main

.. figure:: figures/create.png
    :align: center
    :width: 70%
    
    Page de création de quiz
    
----------------------------------------------------
Création d'une question et définition de ses caractéristiques
----------------------------------------------------

La création du quiz se fait par l'intermédiaire d'un langage de balisage de type Markdown pour définir les différentes questions du quiz ainsi que leurs caractéristiques. Le code du quiz doit être écrit dans la zone de texte principale **(4)** La définition des questions se fait selon le schéma suivant : Une balise avec des accolades comme ``{++}`` permet de définir une nouvelle question. Toutes les balises avec des accolades doivent se situer en début de ligne. Le texte de la question peut être écrit sur plusieurs lignes, chaque retour à la ligne simple est considéré comme un espace. Ensuite, divers attributs peuvent être ajoutés aux questions. Chaque attribut est également caractérisé par une balise avec des accolades.

^^^^^^^^^^^^^^^^^^^^^^^
Explication des balises
^^^^^^^^^^^^^^^^^^^^^^^

+--------+-----------------------------------------------------------------------------+
| Balise | Signification                                                               |
+========+=============================================================================+
| {\+\+} | Question à choix multiple avec plusieurs options qui peuvent être choisies  |
+--------+-----------------------------------------------------------------------------+
| {\*\*} | Question à choix multiple avec une seule option qui peut être choisie       |
+--------+-----------------------------------------------------------------------------+
| {??}   | Question avec un champ de texte à remplir                                   |
+--------+-----------------------------------------------------------------------------+
| {\*}   | Option invalide dans un QCM                                                 |
+--------+-----------------------------------------------------------------------------+
| {=}    | Option valide dans un QCM                                                   |
+--------+-----------------------------------------------------------------------------+
| {=}    | Réponse correcte dans une question à champ de texte                         |
+--------+-----------------------------------------------------------------------------+
| {=r}   | Réponse d'une question à champ de texte définie par une expression régulière|
+--------+-----------------------------------------------------------------------------+
| {.}    | Permet de définir le nombre de points sur la question (par défaut, 1)       |
+--------+-----------------------------------------------------------------------------+
| {\+}   | Ajout d'un commentaire d'explication qui sera affiché lors de la correction |
+--------+-----------------------------------------------------------------------------+

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Exemple de quiz avec le système de balisage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: text
    
    {++}
    Énoncé de la question à choix multiple (plusieurs cases peuvent être cochées)
    {*} Option 1
    {=} Option 2 (correcte)
    {=} Option 4 (correcte)
    {+} Commentaire affiché à la correction
    {.} 1.5
    
    {**}
    Énoncé de la question à choix multiple (une seule case peut être cochée)
    {*} Option 1
    {*} Option 2
    {=} Option 3 (correcte)
    {.} 2
    
    {??} Question à réponse courte
    {=} x = 5
    {=r} La réponse doit contenir 5 // ^.*5.*$
    
Pour la première question, la balise ``{++}`` indique qu'il s'agit d'une question à choix multiple avec plusieurs réponses possibles, alors qu'une option incorrecte et deux options correctes sont respectivement définies avec les balises ``{*}`` et ``{=}``. Ensuite, on a ajouté un commentaire avec ``{+}`` et défini le nombre de points avec le symbole ``{.}``. Le nombre d'espaces ou de retours à la ligne après une balise ou entre les attributs n'a aucune importance.

La barre d'outils **(2)** située en dessus de la zone de texte offre la possibilité de créer un quiz sans maîtriser le système de balisage. Pour ajouter une question, il suffit de cliquer sur l'onglet *Question* et de choisir le type de question souhaité dans le menu déroulant. La balise est insérée automatiquement et il n'y a plus qu'à écrire l'énoncé de la question. Il en va de même pour ajouter des solutions ou des options avec le menu *Réponses*. Les retours à la ligne sont placés automatiquement avant la balise si cela est nécessaire. Le menu *Autres* permet de choisir le nombre de points à attribuer pour chaque question et d'écrire un commentaire destiné à être affiché lors de la correction automatique du quiz. Ce commentaire est censé apporter une justification à la solution de la question ou une aide pour les élèves n'ayant pas répondu correctement.

^^^^^^^^^^^^^^^^^^
Types de questions
^^^^^^^^^^^^^^^^^^

"""""""""""""""""""""""""
Question à réponse courte
"""""""""""""""""""""""""

La question à réponse courte se présente sous la forme d'un simple champ de texte à compléter. La balise
caractérisant ce type de questions est la balise ``{??}``.

Il existe deux possibilités de définir des solutions pour ce type de question. La première méthode consiste
à utiliser la balise ``{=}``. Plusieurs solutions de ce type peuvent être ajoutées. La réponse soumise par
l'étudiant devra exactement correspondre à une des solutions pour que celui-ci obtienne tous les points. Cette méthode permet de déterminer les solutions
de la question de manière simple et rapide. Les réponses apportées par les élèves définies comme incorrectes lors
de la correction automatique pourront toutefois être admise en tant que solution plus tard.

Ce type de question peut aussi comporter des solutions définies par des expressions régulières. Cette méthode, plus souple,
permet de définir un schéma de chaîne de caractère plutôt qu'une solution stricte. La balise
``{=r}`` est cette fois-ci utilisée. Un libellé qui définit ce que représente l'expression régulière doit être
placé après la balise, suivie de l'expression régulière en elle-même. Le libellé doit être séparé de l'expression
par les caractères ``//``. Là encore, les espaces et les retours à la ligne ne sont pas pris en compte.

Exemple de question à réponse courte avec deux solutions :

.. code-block:: text
    
    {??} Résolution de l'équation suivante : 2x = 10
    {=} x = 5
    {=r} Doit comporter le chiffre "5" // ^.*5.*$
    
Avec l'expression régulière ``^.*5.*$``, toutes les réponses contenant le caractère ``5``
seront acceptées. Ainsi, ``x = 5``, ``x=5``, ``5`` ou encore ``solution : 5`` seront des réponses valides.

Pour plus d'informations sur les expressions régulières, se référer à `la documentation officielle de Python <https://docs.python.org/2/library/re.html>`_ [#2]_

.. figure:: figures/short.png
    :align: center
    :width: 80%
    
    Question à réponse courte

""""""""""""""""""""""""""""""""""""""""""""""""""""
Question à choix multiples avec un seul choix valide
""""""""""""""""""""""""""""""""""""""""""""""""""""

Pour ce type, plusieurs options sont affichées et l'élève ne peut en sélectionner qu'une. La balise associé à ce type est la balise ``{**}``. Une seule option valide doit donc être définie avec la balise ``{=}``, toutes les autres doivent être erronées et donc précédées par la balise ``{*}``. L'élève reçoit tous les points s'il sélectionne la bonne solution, et aucun point dans tous les autres cas.

.. figure:: figures/radio.png
    :align: center
    :width: 80%
    
    QCM à boutons radio

""""""""""""""""""""""""""""""""""""""""""""""""""""
Question à choix multiples avec plusieurs choix valides
""""""""""""""""""""""""""""""""""""""""""""""""""""

Définie par la balise ``{++}``, il s'agit d'une question semblable à la précédente mais l'élève a cette fois la possibilité de choisir plusieurs options. Les options qui doivent être sélectionnées sont définies avec la balise ``{=}`` et les autres avec la balise ``{*}``. Le professeur doit cependant définir au moins une option correcte. Lors de la correction, l'élève peut obtenir des points pour un choix qu'il a coché et que le professeur a défini comme correct et inversement, c'est à dire qu'il peut aussi gagner des points sur un choix qui n'est pas sélectionné, à condition qu'il soit défini comme erroné.

.. figure:: figures/checkbox.png
    :align: center
    :width: 80%
    
    QCM à cases à cocher

------------------------------------
Affichage de l'aperçu et des erreurs
------------------------------------

Il est possible à tout moment d'afficher un rendu du quiz tel que le verront les étudiants en cliquant sur le bouton *Aperçu* **(5)** en dessous de la zone de
texte. On peut ainsi voir si toutes les questions s'affichent comme prévu **(8)** et également détecter les éventuelles erreurs dans le code. Ces erreurs
apparaissent dans l'encadré rouge **(7)** en dessous du bouton *Aperçu*. Pour chaque erreur, un message explicatif apparaît accompagné du numéro de ligne où s'est
produite l'erreur.

.. code-block:: text
    
    {??} Résolution de l'équation suivante : 2x = 10
    {*=} x = 5
    {=r} Doit comporter le chiffre "5" // ^.*5.*$

Ici, on a tenté d'utiliser la balise ``{*=}``, qui n'existe pas. C'est pourquoi on obtient le message suivant : *Balise inconnue*.

Un quiz ne peut pas être envoyé et enregistré dans la base de données tant qu'il comporte encore des erreurs.

---------------------------------------------
Utilisation de Markdown pour la mise en forme
---------------------------------------------

La mise en forme de certains éléments des quiz peut se faire avec du Markdown. Le Markdown est un langage de balisage à la syntaxe très
simple et intuitive. Il permet d'afficher d'afficher des titres, des liens, des images, des blocs du code ou encore de mettre du texte en gras ou en italique.
`Ce tutoriel <https://guides.github.com/features/mastering-markdown/>`_ [#3]_ permet de prendre en main ce langage en quelques minutes.

Voici un exemple de question utilisant la mise en forme Markdown :

.. code-block:: text

    {++}
    ### Titre de la question
    
    Voici l'énoncé de la question. **Mot en gras**
    
    ```
    def fonction():
        print("Hello World")
        
        return True
    ```
    
    [Tutoriel sur le markdown](https://guides.github.com/features/mastering-markdown/)
    {=} *Option en italique*
    {*} Code sur une ligne : `print("Hello World")`
    
Une fois le rendu effectué, voici le résultat obtenu :

.. figure:: figures/markdown.png
    :align: center
    :width: 80%
    
    Mise en forme avec Markdown

.. note::
    Il n'est pas nécessaire d'indiquer le langage utilisé pour afficher un bloc de code. Le langage est reconnu automatiquement
    et la coloration syntaxique se fait en conséquence.

--------------------------
Affichage de mathématiques
--------------------------

Il est possible d'afficher des formules mathématiques à l'aide de la bibliothèque Javascript MathJax [#1]_. Cet outil permet d'écrire des expressions sous forme de LaTex et de les convertir en HTML pour qu'elles soient visibles dans le navigateur. Il existe deux méthodes d'affichage proposées par MathJax : la méthode *in-line* et la méthode *displayed*. La première méthode offre la possibilité d'inclure une formule dans un paragraphe de texte. Les formules en *in-line* doivent être entourées des caractères suivants : ``\\(...\\)``. Avec la méthode *displayed*, les expressions sont affichées en plus grand, centrées et détachées du reste du texte. Les formules utilisant cette méthode sont délimitées par les balises ``$$...$$``.

.. figure:: figures/math-menu.png
    :align: center
    :width: 40%
    
    Menu pour l'insertion de mathématiques

La barre d'outils propose un menu dédié à l'affichage des mathématiques **(2)**. Deux boutons permettent d'insérer les délimiteurs des méthodes *in-line* et *displayed* et d'autres options pour afficher un échantillon de formules et de symboles sont disponibles. Cette liste est toutefois non-exhaustive.

Voici un exemple de question comportant l'affichage de limites :

.. code-block:: text

    {++} Coche les affirmations correctes
    {*} \\(\lim_{x\to +\infty} 5x + 2 = -\infty\\)
    {*} \\(\lim_{x\to 0} \frac{5}{x} = -\infty\\)
    {=} \\(\lim_{x\to +\infty} \log_{5}(x) = +\infty\\)
    
Résultat lors de l'aperçu :

.. figure:: figures/checkbox.png
    :align: center
    :width: 70%
    
    Question avec des mathématiques

-------------------------------------------
Enregistrement et importation de brouillons
-------------------------------------------

Les brouillons permettent de stocker dans la base de données le code d'un quiz qui n'a pas encore été envoyé et de le récupérer plus tard pour terminer l'édition du quiz et le publier.

Le menu *Brouillons* de la barre d'outils **(3)** est dédié à cette fonctionnalité.

.. figure:: figures/draft-save.png
    :align: center
    :width: 70%
    
    Sauvegarde d'un brouillon

Lorsqu'on clique sur le bouton *Enregistrer un brouillon*, une boîte de dialogue apparaît. Il suffit de préciser un titre pour le brouillon et d'appuyer sur *Enregistrer*. Un message confirmant que le brouillon a bien été enregistré apparaît.

.. figure:: figures/draft-import.png
    :align: center
    :width: 70%
    
    Importation d'un brouillon

Il est désormais possible d'importer ce brouillon grâce au bouton prévu à cet effet dans le menu. Une boîte de dialogue contenant la liste de tous les brouillons de l'utilisateur s'ouvre. Le brouillon recherché peut être importé par un simple clic. Le code du brouillon est alors inséré dans la zone de texte.

-----------------------
Envoi définitif du quiz
-----------------------

Lorsque l'édition du quiz est terminée et que toutes les questions sont prêtes, le quiz peut être envoyé afin d'être sauvegardé dans la base de données et disponible à la résolution pour les élèves. Avant d'envoyer un quiz, il faut s'assurer d'avoir défini un titre **(1)** et d'avoir corrigé toutes les éventuelles erreurs présentes dans le code **(7)**. Lors du clic sur le bouton *Enregistrer* **(6)**, un avertissement apparaîtra au cas où des erreurs persistent et l'envoi ne pourra pas se faire.

================
Suivi des élèves
================

--------------------------------------
Liste des quiz créés par un professeur
--------------------------------------

.. figure:: figures/my-quiz.png
    :align: center
    :width: 70%
    
    Liste des quiz créés par un professeur

Dans l'onglet *Mes quiz*, le professeur peut consulter la liste des quiz qu'il a créé avec des informations générales sur ceux-ci comme la moyenne de points obtenus pour chaque quiz. Grâce au bouton *Voir les stats*, il peut accéder aux statistiques avancées d'un quiz en particulier.

-----------------------------------
Affichage des statistiques avancées
-----------------------------------

.. figure:: figures/stats.png
    :align: center
    :width: 70%
    
    Statistiques avancées

Cette vue offre au professeur la possibilité de se faire une idée générale du niveau de compréhension des élèves d'un simple coup d'oeil. Pour chaque élève ayant répondu au quiz, il peut voir la note globale obtenue ainsi que les points attribués pour chaque question. Pour consulter les réponses soumises par un étudiant, le professeur peut cliquer sur le bouton orange situé au début de la colonne. Il sera ainsi redirigé vers la page de correction de la résolution.

Les boutons bleus *Afficher* permettent de faire apparaître un aperçu rapide de chaque question. Toutes les questions du quiz peuvent aussi être consultées en même temps grâce au bouton *Afficher toutes les questions*. 

Lorsqu'on affiche une question à réponse courte, il est possible de voir les réponses soumises par les élèves qui n'ont pas répondu correctement. Le bouton rouge situé avant chaque réponse permet de valider une réponse et de l'ajouter aux solutions valides.

.. figure:: figures/add-solution.png
    :align: center
    :width: 70%
    
    Ajout d'une solution

Ici, on voit que des étudiants ont trouvé la solution de l'équation mais l'ont simplement exprimé sous une autre forme que celle qui était attendue. Pour obtenir les points, ils auraient dû n'écrire que ``64``. Après avoir cliqué sur le bouton, un message confirmant l'ajout de la solution apparaît, puis la couleur du bouton change. Les statistiques dans le tableau se mettent ensuite à jour. Désormais, tout élève écrivant la réponse sous cette forme-là obtiendra également les points pour la question.

*********
Étudiants
*********

===============
Trouver un quiz
===============

.. figure:: figures/find.png
    :align: center
    :width: 70%
    
    Page de recherche de quiz

Pour trouver un quiz, un étudiant a plusieurs possibilités. Le professeur peut donner l'URL exacte du quiz à compléter, ce qui peut être pratique dans le cas d'un courriel ou toute autre communication informatisée. Un étudiant peut aussi accéder à un quiz en mémorisant son id et en l'entrant dans la champ prévu à cet effet dans l'onglet *Compléter un quiz*.

===========================================
Compléter un quiz et correction automatique
===========================================

.. figure:: figures/complete.png
    :align: center
    :width: 70%
    
    Page pour compléter un quiz

Une fois que l'étudiant a accédé au quiz, il peut le compléter très simplement en remplissant les champs de formulaires affichés. Lorsqu'il a fini, il peut soumettre ses réponses à l'aide du bouton prévu à cet effet. Les réponses soumises sont enregistrées dans la base de données et il est immédiatement redirigé vers une page de correction.

Les réponses incorrectes sont affichées en rouge avec la solution et une éventuelle explication donnée par le professeur pour chaque question. Les points reçus pour chaque question sont affichés avec le total de points sur le quiz. L'étudiant peut aussi comparer son score à la moyenne des autres étudiants qui ont complété le quiz.

.. figure:: figures/correct.png
    :align: center
    :width: 70%
    
    Page de correction

La page pour compléter un quiz ainsi que celle de la correction sont optimisées pour la navigation sur mobile et le design responsive s'adapte parfaitement à tous types de périphériques tels que les téléphones portables ou les tablettes, comme le montre la capture d'écran ci-dessous.

.. figure:: figures/mobile-1.png
    :align: center
    :width: 40%
    
    Page de correction sur mobile

==========================
Historique des résolutions
==========================

.. figure:: figures/completed.png
    :align: center
    :width: 70%
    
    Historique des résolutions de l'élève

Les étudiants ont aussi la possibilité de garder une trace de tous les quiz qu'ils ont complétés. Dans l'onglet *Mes résolutions* sont présentées toutes les résolutions apportées par l'élève à un quiz. Diverses informations complémentaires sont également disponibles, telles que la date et l'heure de la résolution ou le nombre de points obtenus. En cliquant sur un élément de la liste, l'étudiant est redirigé vers la page de correction de la résolution et peut ainsi voir les éventuelles erreurs qu'il a commises.

.. [#1] http://www.mathjax.org/. Consulté le 29 mars 2015.
.. [#2] https://docs.python.org/2/library/re.html. Consulté le 17 mai 2015.
.. [#3] https://guides.github.com/features/mastering-markdown/. Consulté le 17 mai 2015.