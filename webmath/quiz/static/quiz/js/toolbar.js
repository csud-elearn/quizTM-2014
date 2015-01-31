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
});

function insertTag(tag, n_linebreaks) {
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
    update_lines(count(new_text));
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

})();