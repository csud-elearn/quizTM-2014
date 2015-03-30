########################################
Outil d'édition de quiz avec RapydScript
########################################

Le code de l'interpréteur se trouve dans le fichiers **rs-source/interpreter.pyj** et est écrit entièrement
en RapydScript. Le rôle de ce fichier est de gérer l'interprétation du langage utilisé dans l'outil
de création de quiz.
L'objectif de cette manipulation est de permettre à l'utilisateur
d'entrer du code ressemblant vaguement à du Markdown pour ensuite stocker les informations
concernant le quiz dans la base de données sous forme d'un modèle relationnel. Avant l'enregistrement
des données côté serveur, il est nécessaire de structurer ces informations. Ce fichier,
entièrement écrit en RapydScript, va dans un premier temps se charger de lire le code entré par l'utilisateur
et d'en dégager une structure orientée objet sur laquelle il est facile de se baser
pour afficher un aperçu du quiz et opérer des contrôles sur la validité des données
proposées.

Une fois ces contrôles effectués, cette structure pourra être sérialisée
en JSON (Javascript Object Notation), un format permettant l'échange de données sous
forme de chaînes de caractères. Le résultat ainsi obtenu pourra ainsi être
transmis au serveur à l'aide d'un simple formulaire HTML.

Pour illustrer la manipulation opérée par ce script, on peut prendre l'exemple
de ce code entré par l'utilisateur :

.. code-block:: text

    ## Cases à cocher
    * Option 1
    = Option 4
    = Option 5
    . 3
    + Commentaire affiché lors de la correction
    
Avant d'être envoyées au serveur, voici à quoi ressembleront les données structurées
au format JSON :
    
.. code-block:: json

    [
        {
            "text": "Cases à cocher",
            "comment": "Commentaire affiché lors de la correction",
            "points": 3,
            "type": 1,
            "options": [
                {
                    "content": "Option 1",
                    "valid": false
                },
                {
                    "content": "Option 4",
                    "valid": true
                },
                {
                    "content": "Option 5",
                    "valid": true
                }
            ]
        }
    ]

Le code ainsi produit est humainement lisible et il est facile de comprendre comment
sont organisées les informations sur le quiz.

.. py:class:: Parse(text)
    
    Classe principale du fichier dont le rôle est de gérer la lecture du code pour
    produire du JSON contenant toutes les informations sur le quiz et qui pourra
    être envoyé au serveur pour l'enregistrement dans la base de données.
    
    L'argument ``text`` correspond au code du quiz récupéré dans la zone de texte.
    
    .. py:method:: read(text)
        
        Cette méthode sépare dans un premier temps toutes les lignes du fichier et
        les stocke dans une liste. Elle parcourt ensuite la liste puis sépare
        la balise du contenu de chaque ligne.
        
        Une fois que la balise est séparée
        du contenu, elle appelle la méthode ``.new_question`` pour
        la première ligne du code ainsi que pour toutes les lignes situées après
        une ligne vide. ``.new_question()`` prend en argument la balise
        et le contenu de la ligne en question.
        
        Elle procède ensuite de manière analogue avec la méthode ``.new_attribute``
        pour les lignes qui ne sont pas en début de paragraphe.
        
    .. py:method:: new_question(tag, content)
    
        Instancie une nouvelle question avec la classe associée à la balise ``tag``.
        La question ainsi créée est stockée dans la variable d'instance ``self.question_parent``
        pour pouvoir ajouter plus tard les caractéristiques de la question comme
        les options possibles ou le nombre de points qui peuvent être attibués.
        Elle est également ajoutée dans la liste ``self.questions`` qui contient
        toutes les questions du quiz.
        
    .. py:method:: new_attribute(tag, content)
    
        Utilise la méthode ``.add_attribute()`` de la question ``self.question_parent``
        avec la balise et le contenu en argument pour ajouter un attributs à la question.
        La méthode ``.add_attribute()`` se chargera de déterminer ce à quoi correspond
        l'attribut en fonction de la balise donnée en argument.
        
    .. py:method:: render()
    
        Démarre l'aperçu en appliquant la méthode ``.render()`` pour chaque
        question stockée dans ``self.questions``.
        
    .. py:method:: error(message, line)
    
        Ajoute dans la liste ``self.errors`` un dictionnaire contenant le message
        et la ligne de l'erreur.
        
    .. py:method:: show_errors()
    
        Si des erreurs ont été détectées, affiche pour chaque erreur le message
        accompagné de la ligne à l'aide de jQuery.
        
    .. py:method tojson()
    
        Retourne la liste des questions sérialisée en JSON pour l'envoyer au serveur.
        
        Pour chaque question, la méthode ``.properties()`` est appelée. Cette méthode
        retourne un dictionnaire comportant toutes les informations sur la question
        qui doivent être sérialisées en JSON.
        
    .. py:method get_id()
    
        Génère un ID unique qui s'avère utile pour relier un bouton radio ou une
        case à cocher à son étiquette en HTML.
        
    .. py:method get_name()
    
        Génère un nom unique utilisé pour afficher les boutons radio en HTML. Les
        différentes options d'une même question doivent tous avoir le même attribut
        ``name`` pour que ces boutons fonctionnent correctement. Un nom est donc généré
        pour chaque question comportant des boutons radio.
        
.. py:class:: QuestionAbstract(parent, text, line)

    Classe mère de toutes les classes définissant les questions. C'est une classe
    abstraite, c'est à dire qu'elle n'est pas destinée à être instanciée directement.
    
    L'argument ``parent`` correspond à l'instance de la classe :py:class:`Parse`
    depuis laquelle la question a été instanciée. ``text`` sera défini comme énoncé
    de la question et ``line`` indique la ligne à laquelle la question a été créée
    dans le code pour pouvoir afficher des messages d'erreurs au cas où la question
    rencontre un problème.
    
    L'attribut ``self.tags_list`` est un dictionnaire recensant les balises à utiliser
    pour les attributs de la question. À chaque balise est associée la référence d'une méthode
    qui traitera les données de la ligne contenant la balise.
    
    .. py:method:: add_attribute(self, tag, content)
    
        Appelle la méthode correspondant à la balise ``tag`` si celle-ci est définie
        ``self.tags_list``. La méthode est appelée avec un argument, ``content``.
        
        Si la balise n'est pas répertoriée, cette méthode transmet une erreur à
        ``self.parent```.
        
    .. py:method:: add_comment(self, content)
    
        Ajoute un commentaire à la question en assignant ``content`` à ``self.comment``.
        
    .. py:method:: add_points(self, content)
    
        Définit le nombre de points pour la question. Convertir ``content`` en
        un nombre décimal et l'assigne à ``self.points``.
        
    .. py:method:: properties()
    
        Renvoie un dictionnaire contenant toutes les infos sur la question qui doivent
        être sérialisées en JSON et enregistrées sur la base de données.
        
.. py:class:: SimpleQuestion

    Cette classe hérite de :py:class`QuestionAbstract` et définit les caractéristiques
    d'une question à réponse courte.
    
    En plus des attributs héritées de :py:class:`AbstractQuestion`, chaque objet
    de cette classe possède une liste ``self.answers`` qui contient les solutions valides
    pour la question. La balise ``=`` est associée à la définition des solutons.
    
    .. py:method:: add_answer(content)
    
        Ajoute ``content`` à ``self.answers`` pour ajouter une solution.
    
    .. py:method:: render()
    
        Affiche le rendu final de la question. Ce type de question est présenté sous
        la forme d'un simple champ de texte en HTML.
        
        Cette méthode créé un élément HTML ``<label>`` contenant l'énoncé de la question
        ainsi qu'un ``<input type="text">`` pour entrer la réponse.
        
    .. py:method:: check_question()
    
        Cette méthode est appelée lors de l'aperçu pour vérifier que la question
        soit valide. Pour ce type de question, il suffit qu'au moins une réponse
        valide ait été définie. Si la condition n'est pas remplie, la méthode
        ``.error()`` est appliquée à ``self.parent`` pour signaler qu'il y a une erreur
        et que le quiz n'est pas prêt à être envoyé.
        
.. py:class:: QCM_Checkbox

    Cette classe hérite de :py:class`QuestionAbstract` et est destinée aux questions
    à choix multiples pouvant admettre plusieurs options correctes.
    
    La balise ``*`` est associée à la définition d'une option incorrecte alors que
    le signe ``=`` permet d'ajouter une option valide.
    
    L'attribut ``self.options`` stocke les choix possibles pour la question. Chaque
    élément de cette liste est un dictionnaire qui se présente sous la forme suivante :
    
    .. code-block:: python
    
        {"content" : content, "valid" : False} # Option incorrecte
        {"content" : content, "valid" : True} # Option correcte
    
    .. py:method:: add_option(content)
    
        Ajoute une option invalide avec comme texte ``content`` dans ``self.options``.
        
    .. py:method:: add_answer(content)
    
        Fonctionne de manière analogue à la méthode ``.add_option()`` pour définir une option correcte.
        
    .. py:method:: render()
    
        Permet d'afficher un aperçu de la question. Créé un ``<span>`` pour afficher
        l'énoncé de la question puis ajoute pour chaque option un ``<input type="checkbox">`` avec 
        un ``<label>`` contenant le texte de l'option.
        
    .. py:method:: check_question()
    
        Deux conditions sont nécessaires pour valider cette question : la question
        doit avoir au moins deux options et au moins une option correcte.
        
.. py:class:: QCM_Radio

    Ce type de question hérite de :py:class:`QCM_Checkbox` et y ressemble beaucoup.
    La principale différence se situe au niveau de l'affichage : au lieu d'un
    ``<input type="checkbox">``, ce type est affiché avec un ``<input type="radio">``.
    C'est pourquoi la variable ``self.input_type`` vaut ici ``"radio"`` et sert à
    indiquer à la méthode ``.render()`` la manière d'afficher la question.
    
    .. py:class:: add_answer()
    
        Cette méthode fonctionne comme pour ``QCM_Checkbox`` à la différence près
        qu'elle avertir la présence d'une erreur dès qu'une deuxième option correcte
        est ajoutée.

.. py:function:: start_render()

    Instancie un objet à partir de la classe :py:class:`Parse` et y applique la
    méthode ``.render()`` pour afficher l'aperçu.
    
    Il faut aussi relancer le rendu MathJax pour que les formules mathématiques ajoutées
    dans les questions soient affichés. Cela peut se faire très simplement avec la ligne
    de code suivante :
    
    .. code-block:: python
    
        MathJax.Hub.Queue(["Typeset",MathJax.Hub])
        
.. py:function:: submit()

    Instancie un objet de la classe et y applique la méthode ``.tojson()``. La chaîne
    JSON ainsi obtenue est placée dans un ``<input type="hidden">`` et le formulaire
    comportant les champs de titre et du code du quiz est envoyé au serveur à l'aide
    de jQuery :
    
    .. code-block:: javascript
    
        $("#createform").submit()
        
.. py:function:: demo()

    Insère dans la zone de texte un exemple de code comportant trois questions.
    
.. py:function:: main()

    Il s'agit de la fonction executée au chargement de la page avec ``jQuery(document).ready(main)``.
    Elle définit le rôle des boutons ayant un lien ce fichier.