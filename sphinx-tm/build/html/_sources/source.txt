###########
Vues Django
###########

**************************
Concept de vue dans Django
**************************

Le principe des vues dans Django est relativement simple à comprendre, mais il est parfois
plus difficile à appliquer de manière concrète. On peut expliquer ce concept de
la manière suivante : il s'agit de la définition d'un ensemble d'actions à réaliser
lorsqu'une requête précise est effectuée pour déterminer la réponse qui sera renvoyée
par le serveur.

Une vue se divise généralement en trois parties distinctes.
La première est la récupération des données de la requête. La deuxième consiste
à l'analyse et au traitement de ces données. Dans la dernière partie, on détermine
enfin la réponse qui sera envoyée. Il peut s'agir d'une page HTML à afficher, de
données en réponse à une requête Ajax ou encore d'un fichier à télécharger.

*********************
Vues de l'application
*********************

Les vues de l'application sont définies dans le fichier **views.py**. Certaines renvoient
des pages HTML, d'autres sont uniquement destinées à fonctionner avec des requête Ajax.
Le but de cette section est d'expliquer le rôle ainsi que le fonctionnent de chacun de ces vues.

.. automodule:: quiz.views
    :members:

***************
Les formulaires
***************

Django propose des outils pour créer des formulaires et récupérer les
données de ceux-ci. La vue ``complete`` profite grandement de cette possibilité
pour faciliter l'enregistrement des résolutions de quiz.

.. automodule:: quiz.forms
    :members:
    
********************
Le package **utils**
********************

Afin de ne pas surcharger le fichier **views.py**, il était préférable que certaines
manipulations complexes soient définies dans des modules externes. C'est pourquoi un package
**utils** a été créé. Il comporte trois fichiers, destinés respectivement à l'enregistrement
des quiz, à la sauvegarde des résolutions des étudiants et à la correction automatique des résolutions.

=============
utils/save.py
=============

.. automodule:: quiz.utils.save
    :members:

===============
utils/submit.py
===============

.. automodule:: quiz.utils.submit
    :members:
    
================
utils/correct.py
================

.. automodule:: quiz.utils.correct
    :members: