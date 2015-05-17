// Définit des fonctions et des méthodes de raccourcis effectuant des actions fréquentes

var utils = {

// Affiche une boîte de dialogue basique
alert_dialog : function(title, message) {
    $("#generic-dialog-title").text(title);
    $("#generic-dialog-message").text(message);
    $("#generic-dialog").modal("show");
},

// Source : Doc django --> https://docs.djangoproject.com/en/1.7/ref/contrib/csrf/#ajax
// Permet de récupérer un cookie (utile pour la protection csrf django)
getcookie : function(name) {
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
},

};

// Permet de définir une action à réaliser sur une liste d'éléments jQuery
$.fn.click_foreach = function(callback) {
    this.each(function() {
        $(this).click(callback)
    })
}

// Permet d'insérer la sous-chaîne string à l'index en paramètre
String.prototype.insert = function(string, index) {
    return this.slice(0, index) + string + this.slice(index);
};

String.prototype.count = function(char) {
    var count = 0;
    for (var i = 0; i < this.length; i++) {
        if (this[i] == char) {
            count ++;
        }
    }
    
    return count;
}

// Retourne la chaîne répétée n fois
String.prototype.repeat = function(n) {
    var result = "";
    for (var i = 0; i < n; i++) {
        result += this;
    }
    
    return result;
};

// Enlève les espaces et les retours à la ligne au début et à la fin de la chaîne
String.prototype.clean = function() {
    var string = "" + this;
    
    while (string.charAt(0) == " " || string.charAt(0) == "\n") {
        string = string.substring(1);
    }
    
    while (string.charAt(string.length-1) == " " || string.charAt(string.length-1) == "\n") {
        string = string.substring(0, string.length-1);
    }
    
    return string;
};

// Permet de masquer un panel Bootstrap lors du clic
$( document ).ready(function() {
    $(".panel-click .panel-heading").click(function() {
            if ($(this).parent().hasClass("content-hidden")) {
                // Si le panel était masqué, il s'affiche
                $(this).next().show();
                $(this).parent().removeClass("content-hidden");
            }
            else {
                // Sinon, il est masqué
                $(this).next().hide();
                $(this).parent().addClass("content-hidden");
            }
    });
});