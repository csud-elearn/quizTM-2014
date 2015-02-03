(function() {
$( document ).ready(function(){
    $(".tag-insert").each(function(){ // Parcours de tous les boutons de tags
        $(this).click(function(){
            if ($(this).hasClass("tag-q")) {
                // Il faut 2 retours à la ligne pour créer un nouvelle question
                // L'attribut data-tag contient le tag correspondant au bouton
                insertTag($(this).attr("data-tag"), 2);
            }
            else if ($(this).hasClass("tag-p")) {
                // Un seul retour est nécessaire
                insertTag($(this).attr("data-tag"), 1);
            }
        });
    });
    
    $("#savedraft-btn").click(open_savedraft);
    
    $("#submitdraft-btn").click(submitdraft);
    
    $("#importdraft-btn").click(get_draftlist);
});

/*
Insertion de tags
*/

function insertTag(tag, n_linebreaks) {
    // Insère un tag dans la zone de texte
    var pos = $("#quizcode").caret(); // Position du curseur dans la textarea
    var text = $("#quizcode").val(); // Texte avant la modification
    
    var new_text = text; // Texte qui remplacera l'ancien
    
    // Ajout de retours à la ligne s'il n'y en a pas déjà suffisamment
    while (new_text.slice(pos-n_linebreaks, pos) != "\n".repeat(n_linebreaks) && pos-n_linebreaks >= 0) {
        new_text = new_text.insert("\n", pos);
        pos ++;
    }
    
    // Ajout du contenu du tag
    new_text = new_text.insert(tag, pos);
    pos += tag.length;
    
    // Ajout d'espace après le tag s'il n'y en a pas
    if (new_text.charAt(pos) != " ") {
        new_text = new_text.insert(" ", pos);
        pos ++;
    }
    
    // Le contenu de la textarea est redéfini
    $("#quizcode").val(new_text);
    // Le curseur est replacé après tout le texte ajouté
    $("#quizcode").caret(pos);
    
    // Les numéros de lignes sont mis à jour
    show_lines();
}

String.prototype.insert = function(string, index) {
    // Permet d'insérer la sous-chaîne string à l'index en paramètre
    return this.slice(0, index) + string + this.slice(index);
};

String.prototype.repeat = function(n) {
    // Retourne la chaîne répétée n fois
    var result = "";
    for (var i = 0; i < n; i++) {
        result += this;
    }
    
    return result;
};

/* 
Fonctions traitant l'enregistrement de brouillons
*/

// Préparation de la boîte de dialogue
function open_savedraft() {
    $("#draft-title").val($("#title").val()); // Copie du titre dans la boite de dialogue lorsqu'elle s'ouvre
    $("#save-status").css("display", "none"); // Masquage du message éventuellement affiché précédemment
    $("#submitdraft-btn").css("display", "inline-block"); // Réaffichage du bouton s'il avait été caché
}

// Tentative d'envoi des données au serveur via ajax
function submitdraft() {
    var csrftoken = getCookie('csrftoken'); // Récupération du csrf dans les cookies
    var quizcode = $("#quizcode").val();
    var title = $("#draft-title").val();
    
    if (quizcode && title) { // Pas d'enregistrement si les champs sont vides
        // Requête ajax POST pour enregistrer le brouillon
        $.ajax({
                "url": "/quiz/savedraft/",
                "type": "POST",
                "dataType": "text",
                "data": "csrfmiddlewaretoken=" + csrftoken + "&title=" + title + "&code=" + quizcode,
                "success": savedraft_success,
                "error": savedraft_error,
        });
    }
    
    else {
        savedraft_warning(); // Si un des champs est vides, affichage d'un warning
    }
}

// Sauvegarde réussie
function savedraft_success() {
    var $status_box = $("#save-status");
    
    $status_box.removeClass("alert-danger alert-warning"); // Changement de la couleur de fond bootstrap
    $status_box.addClass("alert-success");
    $status_box.css("display", "block"); // Affichage du message
    $status_box.text("Brouillon enregistré");
    
    $("#submitdraft-btn").css("display", "none"); // Le bouton "enregistrer" est masqué
}

// Sauvegarde non réussie
function savedraft_error() {
    var $status_box = $("#save-status");

    $status_box.removeClass("alert-warning alert-success"); // Changement de la couleur de fond bootstrap
    $status_box.addClass("alert-danger");
    $status_box.css("display", "block"); // Affichage du message
    $status_box.text("L'enregistrement a échoué. Veuillez vérifier votre connexion");
}

// Les champs ne sont pas remplis
function savedraft_warning() {
    var $status_box = $("#save-status");

    $status_box.removeClass("alert-danger alert-success"); // Changement de la couleur de fond bootstrap
    $status_box.addClass("alert-warning");
    $status_box.css("display", "block"); // Affichage du message
    $status_box.text("Vous devez entrer un titre et ajouter du contenu au quiz");
}

/*
Fonctions traitant l'import des brouillons
*/

// Affiche la liste des brouillons dans la boite de dialogue
function get_draftlist() {
    $.getJSON("/quiz/listdrafts/", function(data) {
        var $list = $("#list-drafts"); // Liste qui contiendra les brouillons
        $list.children().remove();
        
        for (var i = 0; i < data.length ; i++) {
            $("<a>", {
                "class" : "list-group-item bold",
                "data-id" : data[i]['id'],
                "data-dismiss" : "modal", // Attribut bootstrap pour fermer la boite
            }).text(data[i]["title"]).appendTo($list);
        }
        
        // Lorsqu'on clique sur un bouton, on éxecute importdraft() avec l'id correspondant au bouton en argument
        $list.children().each(function() {
            $(this).click(function() {
               importdraft($(this).attr("data-id")); 
            });
        });
    });
}

// Importe un brouillon depuis le serveur
function importdraft(id) {
    $.ajax({
        "url": "/quiz/getdraft/",
        "type": "GET",
        "dataType": "json",
        "data": "draft=" + id,
        "success": importdraft_success,
    });
}

// Place le titre du brouillon et le code
function importdraft_success(data) {
    var title = data['title'];
    var code = data['code'];
    
    $("#title").val(title);
    $("#quizcode").val(code);
    
    show_lines();
}

// Source : Doc django --> https://docs.djangoproject.com/en/1.7/ref/contrib/csrf/#ajax
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

})();