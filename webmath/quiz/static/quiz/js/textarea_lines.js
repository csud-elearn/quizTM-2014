var old_lines_numbers = 0;
$( document ).ready(function() {
	var initial_n_lines = parseInt($(".linedarea").attr("rows"))
	$(".linedarea").on("input", function() { //La fonction est appelé à chaque fois qu'il y a un changement dans la textarea
		var lines_numbers = count($(".linedarea").val()); //Nombres de lignes écrites dans la textarea
		if (lines_numbers > initial_n_lines) {
			$(".linedarea").attr("rows", lines_numbers); //Changement du nombre de lignes de la textarea pour l'adapter en fonction du contenu
		}

		if (lines_numbers != old_lines_numbers) { //Si le nombre de lignes n'a pas changé depuis la dernière fois, il est inutile de réafficher les numéros
			update_lines(lines_numbers);
		}
		old_lines_numbers = lines_numbers;
	});
});

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