var old_n_lines = 1;
var initial_n_lines = 0;

$( document ).ready(function() {
    initial_n_lines = parseInt($(".linedarea").attr("rows"));
    $(".linedarea").on("input", show_lines);
});

function show_lines() {
    var n_lines = count($(".linedarea").val()); //Nombres de lignes écrites dans la textarea
    if (n_lines > initial_n_lines) {
        $(".linedarea").attr("rows", n_lines); //Changement du nombre de lignes de la textarea pour l'adapter en fonction du contenu
    }

    if (n_lines != old_n_lines) { //Si le nombre de lignes n'a pas changé depuis la dernière fois, il est inutile de réafficher les numéros
        update_lines(n_lines);
    }
    old_n_lines = n_lines;
}

//Compte le nombre de lignes saisies par l'utilisateur
function count(text) {
    var c = 0;
    for(var i = 0; i < text.length; i++) {
        if (text.charAt(i) == "\n") {
            c ++;
        }
    }
    return c + 1;
}

function update_lines(n_lines) { //Affiche les numéros de ligne dans le div #lines
    var text = "";
    var n = 1;
    while (n <= n_lines) {
        text += (n + "<br />");
        n++;
    }
    $(".lines").html(text);
}