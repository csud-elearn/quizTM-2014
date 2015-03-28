##################
Modèle relationnel
##################

************
Introduction
************

Une des premières étapes importantes dans le développement d'un site web est l'élaboration d'un modèle relationnel structuré permettant de stocker toutes les données générées par l'application et de les relier entre elles. Un modèle relationnel décrit les différentes tables de la base de données et les liens entre ces tables. Une table peut être comparée à un tableau contenant des informations. Chaque table comporte une ou plusieurs colonnes, chaque colonne stockant un type de données précisément défini, par exemple un nombre entier ou une chaîne de caractères. Si on imagine une table contenant les données sur les utilisateurs d'un site, une colonne pourrait alors contenir le pseudonyme d'un utilisateur et une autre son âge. On peut ensuite ajouter des entrées dans une table, c'est à dire un ensemble de données dont chaque élément correspond à une colonne de la table. Dans l'exemple précédent, on ajouterait ainsi une ligne pour chaque utilisateur s'inscrivant sur le site. Chaque ligne est identifiée grâce à une clé primaire unique, habituellement sous la forme d'un entier, qui permet de créer des liens entre différentes lignes de différentes tables. Ces liens entre différentes tables sont appelées relations.

Voici, présenté sous forme simplifiée à l'aide d'un tableau, comment on pourrait stocker les données concernant des quiz et leurs créateurs :

**Table contenant les utilisateurs :**

+--------------+----------+-----+
| Clé primaire | Prénom   | Âge |
+==============+==========+=====+
| 1            | Paul     | 26  |
+--------------+----------+-----+
| 2            | Juliette | 22  |
+--------------+----------+-----+
| 3            | Marc     | 48  |
+--------------+----------+-----+

**Table contenant les quiz :**

+--------------+--------------------------+--------+
| Clé primaire | Titre du quiz            | Auteur |
+==============+==========================+========+
| 1            | Fonctions exponentielles | 3      |
+--------------+--------------------------+--------+
| 2            | Logarithmes              | 3      |
+--------------+--------------------------+--------+
| 3            | Comportement à l'infini  | 2      |
+--------------+--------------------------+--------+

Ici, le premier quiz a comme titre *Fonctions exponentielles*, comporte 5 questions et a été créé par Marc (Utilisateur 3).

Une fois que le modèle relationnel a été élaboré, on peut créer une base de données sous forme de fichier. Le langage SQL permet de créer les tables d'une base de données, d'y enregistrer des informations et de faire des requêtes, c'est à dire récupérer des données enregistrées. Un logiciel ou une application web peut ainsi communiquer avec une base de données et stocker les informations nécessaires de manière permanente.

Django offre la possibilité de créer une base de données et d'interagir avec celle-ci par le biais d'une ORM (Object Relational Mapper), on peut donc éviter l'utilisation du langage SQL et communiquer avec la base de données avec des objets et des méthodes Python. Cet aspect de Django sera abordé un peu plus loin.

**************************************************
Utilisation dans l'application de création de quiz
**************************************************

==========================
Implémentation dans Django
==========================

Comme indiqué précédemment, Django fournit une interface de haut niveau pour créer et interagir avec une base de données. On peut écrire nos tables avec une architecture orientée objet, que Django "traduira" ensuite en SQL. Ainsi, pour créer une table dans notre base de données, il suffit de définir une classe héritant de ``models.Model`` et d'initialiser des variables de classes pour ajouter des colonnes à la tables. Ainsi, par exemple, pour implémenter une table contenant les données générales d'un quiz, il suffit d'écrire le code suivant :

.. code-block:: python

    class Quiz(models.Model): #Infos générales sur le quiz
        title = models.CharField(max_length=100) #Colonne contenant une chaîne de caractères
        creation_date = models.DateTimeField() #Colonne contenant une date/heure
        code = models.CharField(max_length=1000) #Colonne contenant une chaîne de caractères
        
Les objets comme ``CharField()`` ou ``DateTimeField()`` permettent de définir des champs d'un type de données précis. Une liste complète des types de champs est disponible sur la documentation officielle de Django : https://docs.djangoproject.com/en/1.7/ref/models/fields/#field-types

=============
Schéma global
=============

L'élaboration d'un schéma relationnel n'est pas chose facile car il est nécessaire que celui ci réponde à certains critères. Il doit être relativement simple afin de garder une certaine flexibilité et d'avoir la possiblité d'être modifié plus tard, car il est souvent difficile de prédire à l'avance les difficultés liées au stockage des données qui pourraient être rencontrées au cours du développement. Il doit également être possible d'ajouter des fonctionnalités sans devoir revoir toute l'organisation du schéma ou créer un trop grand nombre de nouvelles tables. Malgré cela, le modèle doit aussi correspondre aux exigences des fonctionnalités de l'application et doit inclure toutes les relations nécessaires. Il s'agit donc d'une étape cruciale qui peut s'avérer décisive pour la suite du développement.

Voici le diagramme des tables utilisés pour stocker les données des quiz :

.. figure:: figures/quiz-models.png
    :align: center
    
=======================
Explications des tables
=======================

--------
``Quiz``
--------

La table ``Quiz`` est la table centrale de l'application et toutes les autres tables s'organisent autour d'elle. Elle comporte trois colonnes importantes : une contenant le titre, une autre contenant la date et l'heure de création (ajouté automatiquement lorsqu'un nouveau quiz est créé) ainsi qu'une colonne dans laquelle est stockée le nombre maximal de points pouvant être obtenus pour le quiz en question. Cette table comporte également une relation vers une table Teacher  qui permet l'intégration dans le projet de groupe.

Avec django, il est possible d'initialiser automatiquement un champ ``DateTimeField`` à la date/heure du moment où le modèle est instancié avec le paramètre ``auto_now_add``

.. code-block:: python

    creation_date = models.DateTimeField(auto_now_add=True)
    
-------------
``QuizDraft``
-------------

Cette table est un peu isolée dans le schéma relationnel et n'a qu'une fonction : enregistrer le code qu'un quiz qu'un professeur n'a pas terminé et lui offrir la possibilité de le récupérer plus tard pour continuer son travail. Outre la relation vers la table ``Teacher`` et la colonne stockant le code du quiz, une colonne permet de stocker un titre pour pouvoir identifier rapidement un brouillon.

--------------
``SimpleQuestion``
--------------

Cette table contient les informations générales sur les questions simples du quiz. Ces questions sont présentées sous la forme d'un simple champ de texte lorsqu'un élève complète le quiz. Une première colonne ``title`` stocke l'énoncé de la question, ``comment`` permet d'inclure un commentaire affiché lors de la correction automatique du quiz (par exemple la démonstration d'une égalité), ``points`` définit le nombre de points attribués sur cette question et ``number`` enregistre l'ordre auquel doit apparaître la question dans le quiz. Une relation désigne le quiz qui intègre la question.

--------
``SqAnswer``
--------

Cette table contient simplement la solution de la question définie par la relation vers la table *SimpleQuestion*. Il est important de noter qu'il peut y avoir plusieurs solutions possibles pour une question et c'est la raison pour laquelle la solution n'est pas simplement stockée dans une colonne de *SimpleQuestion*.

-------
``Qcm``
-------

La table Qcm permet de stocker les informations générales à propos des questions à choix multiples. Ces questions sont affichées sous forme de boutons radio, de cases à cocher ou de liste déroulante.
Cette table reprend plusieurs colonnes de la table *SimpleQuestion*. C'est pourquoi ces deux tables héritent en fait du même modèle dans django :

.. code-block:: python

    class QuizQuestion(models.Model): #Classe abstraite dont héritent toutes les questions
        text = models.CharField(max_length=200) #Énoncé
        comment = models.CharField(max_length=200, blank=True) #Commentaire
        points = models.FloatField(default=1)
        number = models.IntegerField() #Ordre de la question dans le quiz
        id_quiz = models.ForeignKey(Quiz)
        
        class Meta:
            abstract = True
            
    class SimpleQuestion(QuizQuestion):
        pass #Cette table reprend simplement les mêmes colonnes que le modèle abstrait
        
    class Qcm(QuizQuestion):
        multi_answers = models.BooleanField()

En plus des colonnes héritées de ``QuizQuestion```, ``Qcm`` possède un champ de type booléen. Il s'agit de ``multi_answers``, qui détermine si plusieurs options peuvent êres cochées ou non. Si ce champ vaut ``True``, la question sera affiché sous forme de cases à cocher en HTML. Dans le cas contraire, elle sera affichée à l'aide de boutons radio.

---------
``QcmChoice``
---------

Cette table contient les différents choix possibles pour la question définie par la relation vers ``Qcm``. Elle est formée de deux champs, le premier contenant le texte du choix et l'autre définissant par un booléen s'il est correct ou non de cocher ce choix. Une question à choix multiples doit avoir au moins deux choix possibles et au moins un choix correct. Si ``multi_answers`` vaut ``False`` dans ``Qcm``, une seule option peut être correcte puisque l'étudiant n'a la possibilité de cocher qu'une seule option.

**Note :** D'un point de vue purement relationnel, comme il est indiqué sur le diagramme, cette table possède une relation vers une table qui sert d'intermédiaire entre *QcmChoice* et ``QcmSubmitMulti``. Cette table intermédiaire crée en fait une relation de type *Complexe-Complexe*. L'implémentation de ce type de relation avec Django sera abordé plus loin.

-------------
``CompletedQuiz``
-------------

Comme on peut le voir sur le diagramme, à l'instar de ``Quiz``, cette table occupe aussi un rôle central dans le modèle relationnel. Elle permet de faire le lien entre un quiz créé par un professeur et les réponses soumises à ce quiz par les étudiants. Elle possède donc une relation vers une table ``Student``, qui définit l'étudiant ayant répondu au quiz. De l'autre côté, cette table pointe vers ``Quiz`` et définit logiquement le quiz auquel l'étudiant a répondu. Un seul champ est présent : la date et l'heure de la soumission des réponses.

--------
``SqSubmit``
--------

Il s'agit simplement de la réponse apportée à une question simple. La table a donc un champ ``text`` qui contient la réponse soumise par l'élève et un champ ``result`` qui stocke le nombre de points obtenus pour la question. Elle possède aussi deux relations, une vers ``SimpleQuestion`` pour préciser la question auquel l'élève a répondu, et une autre vers *CompletedQuiz*. La réponse soumise par l'élève sera ensuite comparée à(aux) solution(s) enregistrées pour déterminer si les points sont attribués ou non.

------------------------------
``QcmSubmitOne et QcmSubmitMulti``
------------------------------

Ces deux tables sont très similaires. ``QcmSubmitOne`` contient une relation vers l'option sélectionnée par l'étudiant dans une question à choix multiples avec *multi_answers* valant ``False```, tandis que ``QcmSubmitMulti`` peut contenir des relations vers plusieurs options, quand ``multi_answers`` vaut ``True``. Il s'agit donc dans le premier cas d'une relation *Complexe-Simple*, puique plusieurs lignes peuvent pointer vers la même option. Dans le deuxième cas, c'est une relation de type *Complexe-Complexe*, puisque plusieurs lignes peuvent pointer vers plusieurs options.

Dans Django, voici comment seront définies ces relations :

.. code-block:: python

    id_selected = models.ForeignKey(QcmChoice, null=True) #Relation Complexe-Simple
    id_selected = models.ManyToManyField(QcmChoice, null=True) #Relation Complexe-Complexe
    
L'argument ``null`` vaut ici ``True`` car il se peut que l'étudiant ne coche aucun choix. Dans ce cas-là, il n'obtiendra dans tous les cas aucun point.

En plus de ces relations, ces tables enregistrent aussi le nombre de points obtenus par l'étudiant pour la question dans la colonne ``result``.
