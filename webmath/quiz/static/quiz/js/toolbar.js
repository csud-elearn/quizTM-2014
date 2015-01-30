(function() {
$( document ).ready(function(){
    $(".tag-insert").each(function(){
        $(this).click(function(){
            // Récupération du tag associé au bouton
            if ($(this).hasClass("tag-q")) {
                // bool_linebrak vaut true car il faut s'assurer qu'il y ait une ligne vide avant
                insertTag($(this).attr("data-tag"), 2);
            }
            else if ($(this).hasClass("tag-p")) {
                insertTag($(this).attr("data-tag"), 1);
            }
        });
    });
});

function insertTag(tag, n_linebreaks) {
    var pos = $("#zonetexte").caret(); // Position du curseur dans la textarea
    var text = $("#zonetexte").val();
    
    var new_text = text;
    
    // Check des caractères à ajouter avant (retours à la ligne)
    while (new_text.slice(pos-n_linebreaks, pos) != "\n".repeat(n_linebreaks) && pos-n_linebreaks > 0 && pos < 100) {
        new_text = new_text.insert("\n", pos);
        pos ++;
    }
    
    // Ajout du contenu du tag
    new_text = new_text.insert(tag, pos);
    pos += tag.length;
    
    // Check des caractères à ajouter après (espaces)
    
    if (new_text.charAt(pos) != " ") {
        new_text = new_text.insert(" ", pos);
        pos ++;
    }
    
    $("#zonetexte").caret(pos);
    $("#zonetexte").val(new_text);
}

String.prototype.insert = function(string, index) {
    // Permet d'insérer la sous-chaîne string à l'index en paramètre
    return this.slice(0, index) + string + this.slice(index);
};

String.prototype.repeat = function(n) {
    // Concatène la même chaîne n fois
    var result = "";
    for (var i = 0; i < n; i++) {
        result += this;
    }
    
    return result;
};

})();