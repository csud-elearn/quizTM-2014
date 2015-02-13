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

// Retourne la chaîne répétée n fois
String.prototype.repeat = function(n) {
    var result = "";
    for (var i = 0; i < n; i++) {
        result += this;
    }
    
    return result;
};