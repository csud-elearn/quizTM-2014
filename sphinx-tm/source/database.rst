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

Comme indiqué précédemment, Django fournit une interface de haut niveau pour créer et interagir avec une base de données. On peut écrire nos tables avec une architecture orientée objet, que Django "traduira" ensuite en SQL. Ainsi, pour créer une table dans notre base de données, il suffit de définir une classe héritant de ``models.Model`` et d'initialiser des variables de classes pour ajouter des colonnes à la table. Ainsi, par exemple, pour implémenter une table contenant les données générales d'un quiz, il suffit d'écrire le code suivant :

.. code-block:: python

    class Quiz(models.Model): #Infos générales sur le quiz
        title = models.CharField(max_length=100) #Colonne contenant une chaîne de caractères
        creation_date = models.DateTimeField() #Colonne contenant une date/heure
        code = models.CharField(max_length=1000) #Colonne contenant une chaîne de caractères
        
Les objets comme ``CharField()`` ou ``DateTimeField()`` permettent de définir des champs d'un type de données précis. Une liste complète des types de champs est disponible sur `la documentation officielle de Django <https://docs.djangoproject.com/en/1.7/ref/models/fields/#field-types>`_ [#2]_

=============
Schéma global
=============

L'élaboration d'un schéma relationnel n'est pas chose facile car il est nécessaire que celui-ci réponde à certains critères. Il doit être relativement simple afin de garder une certaine flexibilité pour pouvoir être modifié plus tard, car il est souvent difficile de prédire à l'avance les difficultés liées au stockage des données qui pourraient être rencontrées au cours du développement. Il doit également être possible d'ajouter des fonctionnalités sans devoir revoir toute l'organisation du schéma ou créer un trop grand nombre de nouvelles tables. Malgré cela, le modèle doit aussi correspondre aux exigences des fonctionnalités de l'application et doit inclure toutes les relations nécessaires. Il s'agit donc d'une étape cruciale qui peut s'avérer décisive pour la suite du développement.

Voici le diagramme des tables utilisés pour stocker les données des quiz :

.. figure:: figures/quiz-models.png
    :align: center
    
=======================
Explications des tables
=======================

Dans ce chapitre sont présentés tous les modèles définis dans le fichier *models.py*.
L'utilisation d'une architecture orientée objet pour la création de tables dans la base
de données permet l'utilisation de méthodes, qui se révèlent très pratiques lorsqu'on
veut récupérer des informations équivalentes depuis des éléments provenant de tables
différentes. Par exemple, si on veut afficher le résultat moyen obtenu pour chacune
des questions d'un quiz, il est très intéressant de pouvoir appliquer la même méthode
à toutes les questions pour récupérer leur moyenne sans se soucier de la classe à laquelle
ces questions appartiennent.

.. autoclass:: quiz.models.Quiz
    :members:
    
.. autoclass:: quiz.models.CompletedQuiz
    :members:
    
.. autoclass:: quiz.models.QuizDraft
    :members:
    
.. autoclass:: quiz.models.SimpleQuestion
    :members:
    
.. autoclass:: quiz.models.SqAnswer
    :members:
    
.. autoclass:: quiz.models.SqSubmit
    :members:
    
.. autoclass:: quiz.models.Qcm
    :members:
    
.. autoclass:: quiz.models.QcmChoice
    :members:

.. autoclass:: quiz.models.QcmSubmit
    :members:

.. autoclass:: quiz.models.QcmSubmitMulti
    :members:
    
.. autoclass:: quiz.models.QcmSubmitOne
    :members:
    
.. [#2] https://docs.djangoproject.com/en/1.7/ref/models/fields/#field-types. Consulté le 29 mars 2015.