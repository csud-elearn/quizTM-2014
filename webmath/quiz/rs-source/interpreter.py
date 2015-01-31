import stdlib

class QuestionAbstract: #Classe mère de toutes les questions, non destinée à avoir des instances
    def __init__(self, parent, text, line):
        self.line = line #Numéro de ligne dans la textarea qui correspond à la question
        self.text = text #Enoncé de la question
        self.parent = parent #Référence de l'objet Parse pour pouvoir appeler les méthodes de celui-ci
        #Associaton des différents tags au méthodes de la classe
        self.tags_list = {
            "+" : self.add_comment,
            "." : self.add_points,
        }
        self.comment = "" #Commentaire affiché lors de la correction
        self.points = 1

    def add_attribute(self, tag, content): #Décide l'action à éxecuter avec un attribut selon le tag
        if self.tags_list[tag]:
            JS("self.tags_list[tag].call(self, content)") #Exécute la méthode associé au tag
        else:
            self.parent.error("Tag inconnu") #Si le tag n'est pas supporté par la question

    def add_comment(self, content):
        self.comment += content

    def add_points(self, n_points):
        self.points = float(n_points)

        if not self.points:
            self.parent.error("La valeur en points doit être un nombre décimal")

    def properties(self):
        #Retourne les propriétés communes à tous types de question pour la construction du json
        properties = {
            "text" : self.text,
            "comment" : self.comment,
            "points" : self.points,
        }

        return properties

class SimpleQuestion(QuestionAbstract): #Question simple avec un champ de texte classique pour entrer la réponse
    def __init__(self, parent, text, line):
        QuestionAbstract.__init__(self, parent, text, line)
        self.answers = [] #Listes des réponses correctes

        self.tags_list["="] = self.add_answer #Associaton des différents tags au méthodes de la classe

    def add_answer(self, content):
        self.answers.append(content)

    def render(self): #Aperçu du rendu final de la question
        id_input = self.parent.get_id()
        $container = $("<li>", {"class" : "q_container list-group-item"}).appendTo(self.parent.$render)
        $("<label>", {"for" : id_input}).append(self.text).appendTo($container)
        $("<input>", {"type" : "text", "id" : id_input, "class" : "form-control"}).appendTo($container)
        
    def properties(self): #Renvoie les caractéristiques de la question pour la construction du json
        properties = QuestionAbstract.properties(self)
        properties["type"] = 0
        properties["answers"] = self.answers

        return properties

    def check_question(self): #Recherche la présence d'erreurs dans la question
        if len(self.answers) < 1:
            self.parent.error("Cette question doit comporter au moins une réponse", self.line)

class QCM_Checkbox(QuestionAbstract):
    def __init__(self, parent, text, line):
        QuestionAbstract.__init__(self, parent, text, line)
        self.has_answer = False
        self.options = []
        self.input_type = "checkbox" #Indique le type de <input>

        #Associaton des différents tags au méthodes de la classe
        self.tags_list["*"] = self.add_option
        self.tags_list["="] = self.add_answer

    def add_option(self, content):
        self.options.append({"content" : content, "valid" : False})

    def add_answer(self, content):
        self.has_answer = True
        self.options.append({"content" : content, "valid" : True})

    def render(self):
        $container = $("<li>", {"class" : "q_container list-group-item"}).appendTo(self.parent.$render)
        $("<span>", {"class" : "label-span"}).append(self.text).appendTo($container)
        name = self.parent.get_name()
        for option in self.options:
            id_option = self.parent.get_id() #Génération d'un id unique pour lier le label à la case à cocher
            $("<input>", {"type" : self.input_type, "id" : id_option, "name" : name}).appendTo($container)
            $("<label>", {"for": id_option}).append(option.content).appendTo($container)
            $("<br />").appendTo($container)
            
    def properties(self): #Renvoie les caractéristiques de la question pour la construction du json
        properties = QuestionAbstract.properties(self)
        properties["type"] = 1
        properties["options"] = self.options

        return properties

    def check_question(self): #Recherche la présence d'erreurs dans la question
        if len(self.options) < 2:
            self.parent.error("Cette question doit comporter au moins deux options", self.line)
        elif not self.has_answer:
            self.parent.error("Cette question doit comporter au moins une option correcte", self.line)

class QCM_Radio(QCM_Checkbox):
    def __init__(self, parent, text, line):
        QCM_Checkbox.__init__(self, parent, text, line)
        self.input_type = "radio" #Indique le type de <input>

    def add_answer(self, content):

        if self.has_answer:
            self.parent.error("Ce type de question ne peut comporter qu'une seule réponse valide")
        else:
            self.options.append({"content" : content, "valid" : True})
            self.has_answer = True
            
    def properties(self): #Renvoie les caractéristiques de la question pour la construction du json
        properties = QCM_Checkbox.properties(self)
        properties["type"] = 2

        return properties

class QCM_Select(QCM_Radio): #Question à liste déroulante. Seule le rendu change par rapport à QCM_Radio
    def render(self):
        id_input = self.parent.get_id()
        $container = $("<li>", {"class" : "q_container list-group-item"}).appendTo(self.parent.$render)
        $("<label>", {"for" : id_input}).append(self.text).appendTo($container)
        $select = $("<select>", {"class" : "form-control", "id" : id_input}).appendTo($container)
        $("<option>").append("---------").appendTo($select) #Ajout d'une option vide
        for option in self.options:
            $("<option>").append(option.content).appendTo($select)
            
    def properties(self): #Renvoie les caractéristiques de la question pour la construction du json
        properties = QCM_Radio.properties(self)
        properties["type"] = 3

        return properties

class Parse:
    def __init__(self, text):
        self.questions = [] #Listes contenant les objets questions du quiz
        self.errors = [] #Pour chaque erreur, contient la ligne et le message d'erreur
        self.id = 0 #id unique utilisé pour le rendu
        self.name = 0 #name unique utilisé pour le rendu
        self.number = 0 #Numéro de question
        self.question_parent = None #Référence vers le dernier objet question instancié

        self.read(text)

    def read(self, text): #Lecture du texte
        lines = text.split("\n")

        split_lines = [] #Pour chaque ligne, contient le tag et le contenu
        self.l = 0 #Ligne lue actuellement

        #Séparation du tag et du contenu de chaque ligne
        for line in lines:
            tag = ""
            content = ""
            is_content = False #Vaut True si la suite de la ligne fait partie du contenu
            for char in line:
                if is_content: 
                    content += char
                elif char == " ": #Le premier espace de la ligne sépare le tag du contenu
                    is_content = True
                else:
                    tag += char
            split_lines.append({"tag" : tag, "content" : content}) #Le tag et le contenu de chaque ligne sont rangés dans une liste

        line_is_question = True #La première ligne est forcément une nouvelle question

        while self.l < len(split_lines):
            if split_lines[self.l].tag == "": #Si le tag est vide, la ligne est forcément vide et signale le passage à la question suivante
                line_is_question = True
                self.l += 1
            else:
                tag = split_lines[self.l].tag
                content = split_lines[self.l].content

                #Création des questions et des attributs suivant le type de la ligne
                if line_is_question:
                    self.new_question(tag, content)
                    line_is_question = False
                else:
                    self.new_attribute(tag, content)

                self.l += 1

        for question in self.questions:
            question.check_question()

    def new_question(self, tag, contenu):
        self.question_parent = None #On repasse le parent à None pour éviter que les attributes viennent s'ajouter à la question précédente si la question ne peut pas être crée
        if contenu:
            questions_types = {
                "??" : SimpleQuestion,
                "##" : QCM_Checkbox,
                "**" : QCM_Radio,
                "^^" : QCM_Select
            }
            
            if questions_types[tag]:
                #Instanciation de la question avec le constructeur associé au tag
                self.question_parent = JS("new questions_types[tag](self, contenu, self.l)") #Utilisation de JS() pour écrire du JS pur. Sans cela, RS n'ajoute pas "new"
                self.questions.append(self.question_parent)
            
            else: #Si la queston n'a pas pu être crée car le tag n'a pas été trouvé
                self.error("Tag inconnu")
        else:
            self.error("Contenu introuvable")

    def new_attribute(self, tag, contenu, line):
        if self.question_parent: #On s'assure qu'il y a une question parente valide.
            if contenu:
                self.question_parent.add_attribute(tag, contenu)
            else:
                self.error("Contenu introuvable")

    def render(self): #Aperçu du quiz
        if len(self.questions) > 0:
            $(".viewbox").css("display", "block")

            self.$render = $("#view_form")
            self.$render.empty()

            for question in self.questions:
                question.render()

        else:
            $(".viewbox").css("display", "none")

        self.show_errors()

    def error(self, message, line = self.l): #Permet de signaler une erreur
        self.errors.append({"line" : line+1, "message" : message})

    def show_errors(self): #Affiche les différentes erreurs signalées dans le format texte
        if len(self.errors) > 0:
            $(".errorsbox").css("display", "block")

            $errors_div = $("#errors-div")
            $errors_div.empty()

            for error in self.errors:
                $container = $("<div>", {"class" : "error-container"}).appendTo($errors_div)
                $("<div>", {"class" : "error-line"}).append("Ligne " + error.line).appendTo($container)
                $("<div>", {"class" : "error-content"}).append(error.message).appendTo($container)
        else:
            $(".errorsbox").css("display", "none")
            
    def tojson(self): #Renvoie la chaine json contenant toutes les caractéristiques du quiz
        json = ""
        if len(self.errors) > 0:
            alert("Il y a encore des erreurs")
        elif len(self.questions) == 0:
            alert("Contenu vide")
        else:
            object_json = [] #Objet destiné à être converti en json
            for question in self.questions:
                object_json.append(question.properties()) #Ajout des propriétés de chaque question
            json = JSON.stringify(object_json)
        return json

    #Méthodes de générations de chaines uniques

    def get_id(self): #Génère un id unique
        self.id += 1
        return "id_" + self.id

    def get_name(self): #Génère un name unique
        self.name += 1
        return "name_" + self.name

def get_text(): #Retourne le contenu de la textarea
    return $("#quizcode").val()

def start_render(): #Affiche l'aperçu
    parse = Parse(get_text()).render()
    
def submit(): #Soumet les données au serveur
    parse = Parse(get_text())
    json_string = parse.tojson()
    if json_string:
        $("#quiz_json").val(json_string) #On ajoute le json dans un champ de formulaire caché
        $("#createform").submit() #Le formulaire est soumis
    else:
        parse.render()



def demo(): #Permet d'insérer un exemple de format texte
    demo_text = "## Cases à cocher\
\n* Option 1\
\n= Option 4\
\n= Option 5\
\n\
\n-- Liste déroulante\
\n* Option 2\
\n= Option 3\
\n\
\n?? Question simple\
\n= Réponse\
\n\
\n** Boutons radio\
\n* Option 1\
\n= Option 2\
\nerreur"
    $("#quizcode").val(demo_text)
    show_lines()

def main(): #Chaque bouton est lié à une méthode
    $("#bouton").click(start_render)
    $("#demo").click(demo)
    $("#submit").click(submit)

jQuery(document).ready(main)