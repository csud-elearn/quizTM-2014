###########################
Présentation de RapydScript
###########################

************************************************
Pourquoi utiliser Python plutôt que Javascript ?
************************************************

Les sites web d'aujourd'hui utilisent de plus en plus le Javascript afin de rendre la navigation plus confortable pour le visiteur. Les fonctionnalités offertes par ce language permettent de concevoir une grande variété d'applications utilisables directement dans le navigateur, qui s'éxécutent côté client et qui sont donc par conséquent très accessibles au grand public. Le Javascript est donc un langage quasiment incontournable pour toute personne qui s'intéresse au développement web. 

Malgré cela, ce langage n'est pas forcément facile à aborder pour un programmeur habitué à coder en Java, en Python ou dans un autre langage de programmation moderne, car son fonctionnement diffère dans un certain nombre d'aspects fondamentaux. Par exemple, le Javascript est un langage orienté objet à prototype, c'est à dire que les objets utilisés en Javascript sont des copies d'objets prototypes, et non des instances de classes comme en Python et Java. On peut également mentionner d'autres différences importantes, comme la portée des variables par défaut. Afin de palier aux difficultés que peut rencontrer un développeur qui débute dans ce langage, divers outils sont apparus pour tenter de remplacer Javascript par Python, avec pour objectif de combiner les possibilités offertes par le Javascript avec la simplicité et la clarté de Python. Ce travail a pour but de présenter et expliquer les fonctionnalités de RapydScript [#1]_, un outil permettant d'écrire du code très semblable à du code Python et de générer du Javascript à partir de ce code.

*********************************************************************************
Différentes manières d'aborder le problème : CoffeeScript, Brython et RapydScript
*********************************************************************************

Un certain nombre d'outils open-source tentent de faciliter l'écriture de code Javascript et différentes approches du problème sont possibles. CoffeeScript [#2]_ est décrit par ses auteurs comme un langage à part entière, avec sa propre syntaxe, qui ressemble parfois à Python mais est surtout inspirée de celle de Ruby, qui peut être compilé en Javascript. CoffeScript permet l'écriture d'un code source plus clair et concis, le code généré est exécuté avec les mêmes performances que du code Javascript natif, mais son utilisation nécessite l'apprentissage d'un nouveau langage, ce qui peut être un problème pour un débutant.

À l'opposé, Brython [#3]_ propose une toute autre approche : le développeur peut écrire du code en Python qui sera exécuté par un interpréteur Python entièrement codé en Javascript intégré dans la page web. C'est certainement la solution la plus fidèle à Python, puisque la syntaxe de Brython est exactement identique à celle de Python. L'accès au DOM (Document Object Model) et l'utilisation d'Ajax se fait via l'import de modules externes. Brython est donc idéal pour quelqu'un qui ne connaît pas Javascript mais possède de bonnes bases en Python. Cependant, comme la traduction en Javascript se fait en direct, l'impact sur les performances se fait ressentir et peut poser problème pour des scripts complexes. Le script de l'interpréteur (environ 10'000 lignes) doit également être inclus dans chaque page HTML qui comporte du code Brython.

RapydScript a l'avantage de combiner les qualités des deux outils cités plus haut, en permettant d'écrire du code très similaire à du code Python standard et en le compilant en Javascript. Rapydscript est donc facile à prendre en main pour n'importe quelle personne sachant coder en Python et ne limite pas la rapidité d'exécution puisque le code qui sera exécuté est tout simplement du Javascript. Il est aussi possible d'appeler n'importe quelle fonction Javascript standard et par extension d'utiliser n'importe quelle librairie externe. Ce dernier point n'est pas négligeable puisque j'ai opté pour jQuery pour développer mon application de création de quiz en ligne. Le choix de RapydScript pour la réalisation de ce travail est apparu comme évident après avoir considéré les qualités et défauts de ces différents outils. La prise en main ainsi que la compréhension de son fonctionnement a pu se faire aisément, d'autant plus que l'absence de documentation ou de tutoriel complet sur cette technologie en français constitue une motivation supplémentaire et donne un aspect inédit à ce travail.

**************************
Introduction à RapydScript
**************************

============
Installation
============

Il est possible d'installer RapydScript en récupérant directement la dernière version sur le dépôt Github du projet.
Pour cela, il faut exécuter les commandes suivantes dans la console :

.. code-block:: bash
    
    git clone git://github.com/atsepkov/RapydScript.git
    cd RapydScript
    npm link .
    
RapydScript est désormais installé et peut être utilisé en ligne de commande.

===========
Compilation
===========

Pour compiler un fichier **source.pyj** situé dans le répertoire courant, il suffit d'utiliser la commande suivante dans la console :

.. code-block:: bash

    rapydscript source.pyj -o result.js
    
L'option ``-o`` indique à Rapydscript le chemin d'accès du fichier compilé. On peut exécuter la compilation avec d'autres options, comme l'option ``-p``, qui produira du code Javascript indenté avec des retours à la ligne. Le code ainsi obtenu sera beaucoup plus lisible mais aussi plus volumineux.

Une liste plus exhaustive des options de compilation est disponible sur 
`la documentation officielle de RapydScript <http://rapydscript.pyjeon.com/#header-tag-doc3>`_ [#1]_

.. note::

    L'extension habituellement utilisée pour les fichiers RapydScript est l'extension
    ``.pyj``. Il est cependant tout à fait possible d'utiliser l'extension habituelle des fichiers Python ``.py`` ou toute autre          extension au goût de l'utilisateur.

===========================
Programmer avec RapydScript
===========================

---------------
Notions de base
---------------

Pour un habitué de Python, la prise en main de RapydScript peut se faire très rapidement : il suffit d'écrire son programme comme si on écrivait un programme Python, même si dans certains cas particuliers il n'est pas possible de faire exactement la même chose avec RapydScript.

Pour commencer avec un exemple simple, voici en Python une fonction qui prend deux nombres en argument et retourne le plus grand. La fonction est ensuite appelée. Ce code est parfaitement valide en Python :

.. code-block:: python
    
    def maximum(n1, n2):
        if n1 >= n2:
            return n1
        elif n2 > n1:
            return n2
            
    maximum(n1, n2) #Appel de la fonction

Une fois la compilation effectuée avec RapydScript, on obtient ce résultat :

.. code-block:: javascript

    function maximum(n1, n2) {
        if (n1 >= n2) {
            return n1;
        } else if (n2 > n1) {
            return n2;
        }
    }
    maximum(5, 18);
    
On peut voir les opérations qu'a fait RapydScript pour traduire le code source en Javascript : Remplacer le mot clé ``def`` par ``function``, ajouter les accolades qui englobent la fonction et les structures ``if``, ajouter des parenthèses autour des conditions et ajouter un ``;`` à la fin de chaque instruction. On remarque aussi que les commentaires ont été supprimés, puisqu'ils sont seulement utiles dans le code source. Le code ainsi produit peut maintenant être exécuté dans n'importe quel navigateur.

Cet exemple montre cependant un cas assez peu significatif de la puissance de RapydScript puisque le code Javascript correspondant au code source est quasiment identique. Mais RapydScript permet aussi de compiler du code typique de Python, comme par exemple des boucles ``for``, qui n'ont pas d'équivalent en Javascript.

.. code-block:: python

    names_list = ["Paul", "Marie", "Pierre", "Lucie"]
    
    for name in names_list:
        print(name)
        
RapydScript produit un code équivalent en Javascript qui s'éxecutera comme en Python. Le code généré est cette fois plus complexe et des connaissances en Javascript sont nécessaires pour le comprendre. Ce type de manipulation sera étudié dans un chapitre ultérieur. On peut par exemple aussi implémenter une fonction avec des arguments qui prennent des valeurs par défaut, ce qui n'est pas possible en Javascript.

----------------------------------
Programmation orientée objet (POO)
----------------------------------

Ce qui fait de RapydScript un outil si puissant est principalement les possibilités qu'il offre pour faire de la Programmation orientée objet. En Javascript, la POO est basée sur le prototypage, et il est beaucoup plus complexe de créer ses propres objets, avec de l'héritage, etc. En Python, cela est beaucoup plus simple, il est donc particulièrement intéressant de pouvoir utiliser la programmation orientée objet Python pour faire de la programmation web front-end.

Encore une fois, il suffit d'écrire une classe comme on le ferait en Python:

.. code-block:: python
    
    class MyObject:
        def __init__(self, name):
            self.name = name
        
        def get_name(self):
            return self.name
            
    object = MyObject("Object 1") #Instanciation avec un paramètre
    object.get_name() #Retourne "Objet 1"
    
Il est également possible de faire de l'héritage :

.. code-block:: python

    class MyObjectPlus(MyObject): #Classe qui hérite de la classe créée précédemment
        def __init__(self, name, number):
            MyObject.__init__(self, name)
            self.number = number
            
        def get_number(self):
            return self.number
            
        def informations(self):
            return "Nom : " + self.name + " /// Nombre : " + str(self.number)
            
    objet = MyObjectPlus("Objet 2", 5)
    objet.get_name() #Retourne "Objet 2"
    objet.get_number() #Retourne 5
    objet.informations() #Retourne "Nom : Objet 2 /// Nombre : 5"

Il n'est par contre pas possible de définir des variables de classes avec RapydScript (si on définit une variable de classe, RapydScript l'ignore simplement). Cela est dû au fait qu'en Javascript, un objet n'est pas une instance d'une classe comme en Python, mais une copie d'un objet prototype. En Python, une variable de classe est en fait un attribut de l'objet :rst:dir:`Class`. Il n'y a donc qu'un seul espace en mémoire pour cette variable. En Javascript, tous les attributs du prototype sont copiés à chaque fois qu'un objet est créé et il n'y a aucun équivalent aux variables de classe.

----------------------------------------------
Utilisation de la bibliothèque standard Python
----------------------------------------------

Avec RapydScript, il est possible d'utiliser dans le code des fonctions provenant de différentes sources. La première est la bibilothèque standard de Python, c'est à dire les fonctions natives Python, telles que ``print()``, ``len()`` ou ``range()``.

Pour utiliser les fonctions de la bibliothèque standard Python, il faut placer l'instruction suivante au début du fichier Python :

.. code-block:: python

    import stdlib
    
RapydScript définira ainsi ces fonctions dans le fichier généré et leur comportement sera en quelque sorte simulé en Javascript. Ces fonctions peuvent donc être utilisées comme on le ferait en Python, dans le code source.

--------------------------------------
Séparer son code en plusieurs fichiers
--------------------------------------

Il est déconseillé d'écrire tout son code dans un seul fichier lorsqu'on travaille sur un gros projet. Pour séparer son code en plusieurs fichiers, RapydScript prévoit un système d'imports qui ressemble à celui de Python. Voici comment procéder pour écrire son code dans plusieurs fichiers.

Premièrement, chaque fichier du code source doit utiliser l'extension **.pyj**, qui est l'extension des fichiers RapydScript. Ensuite, ces fichiers peuvent être utilisés comme des modules et être importés depuis un autre fichier. Par exemple, si on a placé une partie du code dans un fichier **moduletest.pyj**, on ajoutera l'instruction suivante en début de fichier :

.. code-block:: python
    
    import moduletest
    
Lors de la compilation, RapydScript va rassembler tous les fichiers du code source dans un même fichier Javascript, ce qui facilite aussi l'insertion du script dans un fichier HTML. Il est important de noter, cependant, que l'import d'un module ne rend pas ses fonctions disponibles dans un espace de noms distinct. Par exemple, pour appeler la fonction ``test()`` du module de l'exemple précédent, voici comment procéder :

.. code-block:: python

    import moduletest
    
    test() #Correct
    moduletest.test() #Ne fonctionne pas
    
------------------------------------------------------------------------------
Utilisation de fonctions Javascript natives ou provenant de librairies externes
------------------------------------------------------------------------------

Il est également possible d'utiliser des fonctions Javascript natives, par exemple :

.. code-block:: python

    #Ces deux expressions sont équivalentes :
    console.log("Bonjour") #Fonction Javascript
    print("Bonjour") #Fonction Python
    
L'exemple parle de lui-même et ne nécessite pas d'explication supplémentaire. Il peut parfois être pratique d'utiliser des fonctions qui n'ont pas d'équivalent en Python.

Mais une autre grande force de RapydScript est la possibilité d'utiliser des librairies Javascript externes, telles que jQuery [#4]_ ou AngularJS [#5]_. Pour cela, rien de plus simple, il suffit d'insérer le script de la librairie que l'on veut utiliser dans le code HTML, comme ceci :

.. code-block:: html

    <html>
    <head>
        <script src="jquery.js"></script><!-- jQuery -->
        <script src="myscript.js"></script><!-- Script créé avec RapydScript -->
    </head>
    <body>
        <div id="mydiv"></div>
    </body>
    </html>
    
On peut maintenant utiliser les fonctions jQuery dans notre code. Cette fonction sélectionne le ``<div>`` et y insère du texte :

.. code-block:: python
    
    def add_text(text):
        $("#mydiv").text(text)
        
    add_text("Hello World")
    
On peut procéder de la même manière pour n'importe quelle autre librairie Javascript externe.

.. [#1] http://rapydscript.pyjeon.com. Consulté le 20 mars 2015.
.. [#2] http://coffeescript.org. Consulté le 29 mars 2015.
.. [#3] http://www.brython.info/. Consulté le 29 mars 2015.
.. [#4] https://jquery.com/. Consulté le 29 mars 2015.
.. [#5] https://angularjs.org/. Consulté le 29 mars 2015.