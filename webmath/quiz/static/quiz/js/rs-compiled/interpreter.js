(function(){
    "use strict";
    var _$rapyd$_Temp;
    function range(start, stop, step) {
        var length, idx, range;
        if (arguments.length <= 1) {
            stop = start || 0;
            start = 0;
        }
        step = arguments[2] || 1;
        length = Math.max(Math.ceil((stop - start) / step), 0);
        idx = 0;
        range = new Array(length);
        while (idx < length) {
            range[idx++] = start;
            start += step;
        }
        return range;
    }
    function _$rapyd$_Iterable(iterable) {
        if (iterable instanceof Array || iterable instanceof String || typeof iterable === "string") {
            return iterable;
        }
        return Object.keys(iterable);
    }
    function _$rapyd$_in(val, arr) {
        if (arr instanceof Array || typeof arr === "string") {
            return arr.indexOf(val) !== -1;
        } else {
            if (arr.hasOwnProperty(val)) {
                return true;
            }
            return false;
        }
    }
    function dir(item) {
        var arr;
        arr = [];
        for (var i in item) {
            arr.push(i);
        }
        return arr;
    }
    function _$rapyd$_extends(child, parent) {
        child.prototype = Object.create(parent.prototype);
        child.prototype.constructor = child;
    }
    function len(obj) {
        var count;
        if (obj instanceof Array || typeof obj === "string") {
            return obj.length;
        } else {
            count = 0;
            for (var i in obj) {
                if (obj.hasOwnProperty(i)) {
                    count += 1;
                }
            }
            return count;
        }
    }
    var str;
            str = JSON.stringify;
    function kwargs(f) {
        var argNames;
        argNames = f.toString().match(/\(([^\)]+)/)[1];
        argNames = argNames ? argNames.split(",").map(function(s) {
            return s.trim();
        }) : [];
        return function() {
            var args, kw, i;
            args = [].slice.call(arguments);
            if (args.length) {
                kw = args.pop();
                if (typeof kw === "object") {
                    for (i = 0; i < argNames.length; i++) {
                        if (_$rapyd$_in(argNames[i], dir(kw))) {
                            args[i] = kw[argNames[i]];
                        }
                    }
                } else {
                    args.push(kw);
                }
            }
            return f.apply(this, args);
        };
    }
    function IndexError() {
        IndexError.prototype.__init__.apply(this, arguments);
    }
    _$rapyd$_extends(IndexError, Error);
    IndexError.prototype.__init__ = function __init__(message){
        var self = this;
        if (typeof message === "undefined") message = "list index out of range";
        self.name = "IndexError";
        self.message = message;
    };

    function TypeError() {
        TypeError.prototype.__init__.apply(this, arguments);
    }
    _$rapyd$_extends(TypeError, Error);
    TypeError.prototype.__init__ = function __init__(message){
        var self = this;
        self.name = "TypeError";
        self.message = message;
    };

    function ValueError() {
        ValueError.prototype.__init__.apply(this, arguments);
    }
    _$rapyd$_extends(ValueError, Error);
    ValueError.prototype.__init__ = function __init__(message){
        var self = this;
        self.name = "ValueError";
        self.message = message;
    };

    function AssertionError() {
        AssertionError.prototype.__init__.apply(this, arguments);
    }
    _$rapyd$_extends(AssertionError, Error);
    AssertionError.prototype.__init__ = function __init__(message){
        var self = this;
        if (typeof message === "undefined") message = "";
        self.name = "AssertionError";
        self.message = message;
    };

    function map(oper, arr) {
        return list(arr.map(oper));
    }
    function filter(oper, arr) {
        return list(arr.filter(oper));
    }
    function sum(arr, start) {
        if (typeof start === "undefined") start = 0;
        return arr.reduce(function(prev, cur) {
            return prev + cur;
        }, start);
    }
    function deep_eq(a, b) {
        var i;
        "\n    Equality comparison that works with all data types, returns true if structure and\n    contents of first object equal to those of second object\n\n    Arguments:\n        a: first object\n        b: second object\n    ";
        if (a === b) {
            return true;
        }
        if (a instanceof Array && b instanceof Array || a instanceof Object && b instanceof Object) {
            if (a.constructor !== b.constructor || a.length !== b.length) {
                return false;
            }
            var _$rapyd$_Iter0 = _$rapyd$_Iterable(dict.keys(a));
            for (var _$rapyd$_Index0 = 0; _$rapyd$_Index0 < _$rapyd$_Iter0.length; _$rapyd$_Index0++) {
                i = _$rapyd$_Iter0[_$rapyd$_Index0];
                if (b.hasOwnProperty(i)) {
                    if (!deep_eq(a[i], b[i])) {
                        return false;
                    }
                } else {
                    return false;
                }
            }
            return true;
        }
        return false;
    }
    String.prototype.find = String.prototype.indexOf;
    String.prototype.strip = String.prototype.trim;
    String.prototype.lstrip = String.prototype.trimLeft;
    String.prototype.rstrip = String.prototype.trimRight;
    String.prototype.join = function(iterable) {
        return iterable.join(this);
    };
    String.prototype.zfill = function(size) {
        var s;
        s = this;
        while (s.length < size) {
            s = "0" + s;
        }
        return s;
    };
    function list(iterable) {
        if (typeof iterable === "undefined") iterable = [];
        var result, i;
        result = [];
        var _$rapyd$_Iter1 = _$rapyd$_Iterable(iterable);
        for (var _$rapyd$_Index1 = 0; _$rapyd$_Index1 < _$rapyd$_Iter1.length; _$rapyd$_Index1++) {
            i = _$rapyd$_Iter1[_$rapyd$_Index1];
            result.append(i);
        }
        return result;
    }
    Array.prototype.append = Array.prototype.push;
    Array.prototype.find = Array.prototype.indexOf;
    Array.prototype.index = function(index) {
        var val;
        val = this.find(index);
        if (val === -1) {
            throw new ValueError(str(index) + " is not in list");
        }
        return val;
    };
    Array.prototype.insert = function(index, item) {
        this.splice(index, 0, item);
    };
    Array.prototype.pop = function(index) {
        if (typeof index === "undefined") index = this.length - 1;
        return this.splice(index, 1)[0];
    };
    Array.prototype.extend = function(array2) {
        this.push.apply(this, array2);
    };
    Array.prototype.remove = function(item) {
        var index;
        index = this.find(item);
        this.splice(index, 1);
    };
    Array.prototype.copy = function() {
        return this.slice(0);
    };
    function dict(iterable) {
        var result, key;
        result = {};
        var _$rapyd$_Iter2 = _$rapyd$_Iterable(iterable);
        for (var _$rapyd$_Index2 = 0; _$rapyd$_Index2 < _$rapyd$_Iter2.length; _$rapyd$_Index2++) {
            key = _$rapyd$_Iter2[_$rapyd$_Index2];
            result[key] = iterable[key];
        }
        return result;
    }
    if (typeof Object.getOwnPropertyNames !== "function") {
        dict.keys = function(hash) {
            var keys;
            keys = [];
            
        for (var x in hash) {
            if (hash.hasOwnProperty(x)) {
                keys.push(x);
            }
        }
        ;
            return keys;
        };
    } else {
        dict.keys = function(hash) {
            return Object.getOwnPropertyNames(hash);
        };
    }
    dict.values = function(hash) {
        var vals, key;
        vals = [];
        var _$rapyd$_Iter3 = _$rapyd$_Iterable(dict.keys(hash));
        for (var _$rapyd$_Index3 = 0; _$rapyd$_Index3 < _$rapyd$_Iter3.length; _$rapyd$_Index3++) {
            key = _$rapyd$_Iter3[_$rapyd$_Index3];
            vals.append(hash[key]);
        }
        return vals;
    };
    dict.items = function(hash) {
        var items, key;
        items = [];
        var _$rapyd$_Iter4 = _$rapyd$_Iterable(dict.keys(hash));
        for (var _$rapyd$_Index4 = 0; _$rapyd$_Index4 < _$rapyd$_Iter4.length; _$rapyd$_Index4++) {
            key = _$rapyd$_Iter4[_$rapyd$_Index4];
            items.append([key, hash[key]]);
        }
        return items;
    };
    dict.copy = dict;
    dict.clear = function(hash) {
        var key;
        var _$rapyd$_Iter5 = _$rapyd$_Iterable(dict.keys(hash));
        for (var _$rapyd$_Index5 = 0; _$rapyd$_Index5 < _$rapyd$_Iter5.length; _$rapyd$_Index5++) {
            key = _$rapyd$_Iter5[_$rapyd$_Index5];
            delete hash[key];
        }
    };
    function QuestionAbstract() {
        QuestionAbstract.prototype.__init__.apply(this, arguments);
    }
    QuestionAbstract.prototype.__init__ = function __init__(parent, text, line){
        var self = this;
        self.line = line;
        self.parent = parent;
        text = self.parent.converter.makeHtml(text);
        self.text = text.replace("<pre>", "<pre class=\"prettyprint\">");
        self.tags_list = {
            "+": {
                "function": self.add_comment,
                "markdown": true
            },
            ".": {
                "function": self.add_points,
                "markdown": false
            }
        };
        self.comment = "";
        self.points = 1;
    };
    QuestionAbstract.prototype.add_attribute = function add_attribute(tag, content){
        var self = this;
        if (self.tags_list[tag]) {
            if (self.tags_list[tag]["markdown"]) {
                content = self.parent.converter.makeHtml(content);
                content = content.replace("<pre>", "<pre class=\"prettyprint\">");
            }
            self.tags_list[tag]['function'].call(self, content);
        } else {
            self.parent.error("Balise invalide pour ce type de question");
        }
    };
    QuestionAbstract.prototype.add_comment = function add_comment(content){
        var self = this;
        self.comment += content;
    };
    QuestionAbstract.prototype.add_points = function add_points(n_points){
        var self = this;
        var i_comma;
        i_comma = n_points.find(",");
        if (i_comma >= 0) {
            n_points = n_points.slice(0, i_comma) + "." + n_points.slice(i_comma + 1);
        }
        self.points = parseFloat(n_points);
        if (!self.points) {
            self.parent.error("La valeur en points doit être un nombre décimal");
        }
    };
    QuestionAbstract.prototype.properties = function properties(){
        var self = this;
        var properties;
        properties = {
            "text": self.text,
            "comment": self.comment,
            "points": self.points
        };
        return properties;
    };
    QuestionAbstract.prototype.render = function render(){
        var self = this;
    };

    function SimpleQuestion() {
        SimpleQuestion.prototype.__init__.apply(this, arguments);
    }
    _$rapyd$_extends(SimpleQuestion, QuestionAbstract);
    SimpleQuestion.prototype.__init__ = function __init__(parent, text, line){
        var self = this;
        QuestionAbstract.prototype.constructor.call(self, parent, text, line);
        self.answers = [];
        self.regex_answers = [];
        self.tags_list["="] = {
            "function": self.add_answer,
            "markdown": false
        };
        self.tags_list["=r"] = {
            "function": self.add_regex_answer,
            "markdown": false
        };
    };
    SimpleQuestion.prototype.add_answer = function add_answer(content){
        var self = this;
        self.answers.append(content);
    };
    SimpleQuestion.prototype.add_regex_answer = function add_regex_answer(content){
        var self = this;
        var answer_dict;
        if (_$rapyd$_in("//", content)) {
            answer_dict = {
                "text": self.parent.converter.makeHtml(content.split("//")[0].clean()),
                "regex": content.split("//")[1].clean()
            };
            if (!answer_dict["text"]) {
                self.parent.error("Texte à afficher vide");
            }
            if (!answer_dict["regex"]) {
                self.parent.error("Expression régulière vide");
            }
            self.regex_answers.append(answer_dict);
        } else {
            self.parent.error("Le texte à afficher doit être séparé de l'expression régulière par un <code>//</code>");
        }
    };
    SimpleQuestion.prototype.render = function render(){
        var self = this;
        var id_input, $container;
        id_input = self.parent.get_id();
        $container = $("<li>", {
            "class": "q-container list-group-item"
        }).appendTo(self.parent.$render);
        $("<label>", {
            "for": id_input,
            "class": "markdown-body"
        }).append(self.text).appendTo($container);
        $("<input>", {
            "type": "text",
            "id": id_input,
            "class": "form-control markdown-body"
        }).appendTo($container);
    };
    SimpleQuestion.prototype.properties = function properties(){
        var self = this;
        var properties;
        properties = QuestionAbstract.prototype.properties.call(self);
        properties["type"] = 0;
        properties["answers"] = self.answers;
        properties["regex_answers"] = self.regex_answers;
        return properties;
    };
    SimpleQuestion.prototype.check_question = function check_question(){
        var self = this;
        if (len(self.answers) < 1 && len(self.regex_answers) < 1) {
            self.parent.error("Cette question doit comporter au moins une réponse", self.line);
        }
    };

    function QCM_Checkbox() {
        QCM_Checkbox.prototype.__init__.apply(this, arguments);
    }
    _$rapyd$_extends(QCM_Checkbox, QuestionAbstract);
    QCM_Checkbox.prototype.__init__ = function __init__(parent, text, line){
        var self = this;
        QuestionAbstract.prototype.constructor.call(self, parent, text, line);
        self.has_answer = false;
        self.options = [];
        self.input_type = "checkbox";
        self.tags_list["*"] = {
            "function": self.add_option,
            "markdown": true
        };
        self.tags_list["="] = {
            "function": self.add_answer,
            "markdown": true
        };
    };
    QCM_Checkbox.prototype.add_option = function add_option(content){
        var self = this;
        self.options.append({
            "content": content,
            "valid": false
        });
    };
    QCM_Checkbox.prototype.add_answer = function add_answer(content){
        var self = this;
        self.has_answer = true;
        self.options.append({
            "content": content,
            "valid": true
        });
    };
    QCM_Checkbox.prototype.render = function render(){
        var self = this;
        var $container, name, id_option, option;
        $container = $("<li>", {
            "class": "q-container list-group-item"
        }).appendTo(self.parent.$render);
        $("<div>", {
            "class": "markdown-body"
        }).append(self.text).appendTo($container);
        name = self.parent.get_name();
        var _$rapyd$_Iter6 = _$rapyd$_Iterable(self.options);
        for (var _$rapyd$_Index6 = 0; _$rapyd$_Index6 < _$rapyd$_Iter6.length; _$rapyd$_Index6++) {
            option = _$rapyd$_Iter6[_$rapyd$_Index6];
            id_option = self.parent.get_id();
            $("<input>", {
                "type": self.input_type,
                "id": id_option,
                "name": name
            }).appendTo($container);
            $("<label>", {
                "for": id_option,
                "class": "markdown-body"
            }).append(option.content).appendTo($container);
            $("<br />").appendTo($container);
        }
    };
    QCM_Checkbox.prototype.properties = function properties(){
        var self = this;
        var properties;
        properties = QuestionAbstract.prototype.properties.call(self);
        properties["type"] = 1;
        properties["options"] = self.options;
        return properties;
    };
    QCM_Checkbox.prototype.check_question = function check_question(){
        var self = this;
        if (len(self.options) < 2) {
            self.parent.error("Cette question doit comporter au moins deux options", self.line);
        } else if (!self.has_answer) {
            self.parent.error("Cette question doit comporter au moins une option correcte", self.line);
        }
    };

    function QCM_Radio() {
        QCM_Radio.prototype.__init__.apply(this, arguments);
    }
    _$rapyd$_extends(QCM_Radio, QCM_Checkbox);
    QCM_Radio.prototype.__init__ = function __init__(parent, text, line){
        var self = this;
        QCM_Checkbox.prototype.constructor.call(self, parent, text, line);
        self.input_type = "radio";
    };
    QCM_Radio.prototype.add_answer = function add_answer(content){
        var self = this;
        if (self.has_answer) {
            self.parent.error("Ce type de question ne peut comporter qu'une seule réponse valide");
        } else {
            self.options.append({
                "content": content,
                "valid": true
            });
            self.has_answer = true;
        }
    };
    QCM_Radio.prototype.properties = function properties(){
        var self = this;
        var properties;
        properties = QCM_Checkbox.prototype.properties.call(self);
        properties["type"] = 2;
        return properties;
    };

    function Parse() {
        Parse.prototype.__init__.apply(this, arguments);
    }
    Parse.prototype.__init__ = function __init__(text){
        var self = this;
        self.questions = [];
        self.errors = [];
        self.id = 0;
        self.name = 0;
        self.number = 0;
        self.question_parent = null;
        self.l = 0;
        self.converter = new Showdown.converter();;
        self.read(text);
    };
    Parse.prototype.read = function read(texte){
        var self = this;
        var l_blocks, block_1, i_closing_tag, tag, content, question, block;
        l_blocks = texte.split("\n{");
        block_1 = l_blocks[0];
        if (block_1[0] === "{") {
            l_blocks[0] = block_1.slice(1);
        }
        var _$rapyd$_Iter7 = _$rapyd$_Iterable(l_blocks);
        for (var _$rapyd$_Index7 = 0; _$rapyd$_Index7 < _$rapyd$_Iter7.length; _$rapyd$_Index7++) {
            block = _$rapyd$_Iter7[_$rapyd$_Index7];
            i_closing_tag = block.find("}");
            if (i_closing_tag === -1) {
                self.error("Balise manquante ou incomplète");
            } else {
                tag = block.slice(0, i_closing_tag);
                content = block.slice(i_closing_tag + 1).clean();
                if (content) {
                    question = self.new_question(tag, content);
                    if (question) {
                        self.question_parent = question;
                        self.questions.append(question);
                    } else {
                        self.new_attribute(tag, content);
                    }
                } else {
                    self.error("Texte vide");
                }
            }
            self.l += 1;
            self.l += block.count("\n");
        }
        var _$rapyd$_Iter8 = _$rapyd$_Iterable(self.questions);
        for (var _$rapyd$_Index8 = 0; _$rapyd$_Index8 < _$rapyd$_Iter8.length; _$rapyd$_Index8++) {
            question = _$rapyd$_Iter8[_$rapyd$_Index8];
            question.check_question();
        }
    };
    Parse.prototype.new_question = function new_question(tag, content){
        var self = this;
        var questions_types, question;
        questions_types = {
            "??": SimpleQuestion,
            "++": QCM_Checkbox,
            "**": QCM_Radio
        };
        if (questions_types[tag]) {
            question = new questions_types[tag](self, content, self.l);
            return question;
        } else {
            return false;
        }
    };
    Parse.prototype.new_attribute = function new_attribute(tag, content){
        var self = this;
        if (self.question_parent) {
            if (content) {
                self.question_parent.add_attribute(tag, content);
            } else {
                self.error("La valeur de l'attribut est introuvable");
            }
        } else {
            self.error("Une nouvelle question doit être créée avant de définir un attribut");
        }
    };
    Parse.prototype.render = function render(){
        var self = this;
        var question;
        if (len(self.questions) > 0) {
            $(".viewbox").css("display", "block");
            self.$render = $("#view_form");
            self.$render.empty();
            var _$rapyd$_Iter9 = _$rapyd$_Iterable(self.questions);
            for (var _$rapyd$_Index9 = 0; _$rapyd$_Index9 < _$rapyd$_Iter9.length; _$rapyd$_Index9++) {
                question = _$rapyd$_Iter9[_$rapyd$_Index9];
                question.render();
            }
        } else {
            $(".viewbox").css("display", "none");
        }
        self.show_errors();
    };
    Parse.prototype.error = function error(message, line){
        var self = this;
        if (typeof line === "undefined") line = self.l;
        self.errors.append({
            "line": line + 1,
            "message": message
        });
    };
    Parse.prototype.show_errors = function show_errors(){
        var self = this;
        var $errors_div, $container, error;
        self.errors.sort(sort_by_line);
        if (len(self.errors) > 0) {
            $(".errorsbox").removeClass("panel-default content-hidden disabled").addClass("panel-danger");
            $errors_div = $("#errors-div");
            $errors_div.empty();
            var _$rapyd$_Iter10 = _$rapyd$_Iterable(self.errors);
            for (var _$rapyd$_Index10 = 0; _$rapyd$_Index10 < _$rapyd$_Iter10.length; _$rapyd$_Index10++) {
                error = _$rapyd$_Iter10[_$rapyd$_Index10];
                $container = $("<div>", {
                    "class": "error-container"
                }).appendTo($errors_div);
                $("<div>", {
                    "class": "error-line"
                }).append("Ligne " + error.line).appendTo($container);
                $("<div>", {
                    "class": "error-content"
                }).append(error.message).appendTo($container);
            }
        } else {
            $(".errorsbox").addClass("panel-default content-hidden disabled").removeClass("panel-danger");
        }
    };
    Parse.prototype.tojson = function tojson(){
        var self = this;
        var object_json, question, json;
        json = "";
        if (len(self.errors) > 0) {
            utils.alert_dialog("Erreur", "Vous devez corriger les erreurs avant de pouvoir envoyer le quiz");
        } else if (len(self.questions) === 0) {
            utils.alert_dialog("Erreur", "Votre quiz ne comporte aucune question");
        } else {
            object_json = [];
            var _$rapyd$_Iter11 = _$rapyd$_Iterable(self.questions);
            for (var _$rapyd$_Index11 = 0; _$rapyd$_Index11 < _$rapyd$_Iter11.length; _$rapyd$_Index11++) {
                question = _$rapyd$_Iter11[_$rapyd$_Index11];
                object_json.append(question.properties());
            }
            json = JSON.stringify(object_json);
        }
        return json;
    };
    Parse.prototype.get_id = function get_id(){
        var self = this;
        self.id += 1;
        return "id_" + self.id;
    };
    Parse.prototype.get_name = function get_name(){
        var self = this;
        self.name += 1;
        return "name_" + self.name;
    };

    function start_render() {
        var code, parse;
        code = $("#quizcode").val();
        parse = new Parse(code).render();
        PR.prettyPrint();
        MathJax.Hub.Queue([ "Typeset", MathJax.Hub ]);
    }
    function submit(event) {
        var parse, tags, tags_json, json_string, title;
        event.preventDefault();
        parse = new Parse($("#quizcode").val());
        tags = $("#tags-input").tagsinput("items");
        tags_json = JSON.stringify(tags);
        json_string = parse.tojson();
        title = $("#title").val();
        if (json_string) {
            if (title) {
                $("#quiz_json").val(json_string);
                $("#tags").val(tags_json);
                $("#createform").submit();
            } else {
                utils.alert_dialog("Erreur", "Vous devez spécifier un titre pour votre quiz");
            }
        } else {
            parse.render();
        }
    }
    function sort_by_line(a, b) {
        if (a["line"] < b["line"]) {
            return -1;
        } else {
            return 1;
        }
    }
    function demo() {
        var demo_text;
        demo_text = "{++} Cases à cocher\n{*} Option 1\n{=} Option 4\n{=} Option 5\n\n\n{??} Question simple\n{=} Réponse\n\n{**} Boutons radio\n{*} Option 1\n{=} Option 2";
        $("#quizcode").val(demo_text);
        show_lines();
    }
    function prevent_submit(event) {
        if (event.which === 13) {
            event.preventDefault();
        }
    }
    function main() {
        $("#start-render").click(start_render);
        $("#demo").click(demo);
        $("#submit").click(submit);
        $("#title").keypress(prevent_submit);
    }
    jQuery(document).ready(main);
})();