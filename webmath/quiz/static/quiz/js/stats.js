$( document ).ready(function() {
    
    bind_show();
    // Ajout de nouvelles réponses 
    $(".add-correct-answer").click(function() {
        // Variable pour la vérification avec les requêtes POST Django
        var csrftoken = utils.getcookie("csrftoken");
        var $button = $(this); 
        $.ajax({
            "url": "/quiz/add-correct-answer/",
            "type": "POST",
            "data" : {
                "answer" : $(this).attr("data-answer-id"),
                "csrfmiddlewaretoken" : csrftoken,
            },
            "success": function() {
                // Changement de couleur du bouton
                $button.removeClass("btn-danger").addClass("btn-success disabled");
                utils.alert_dialog("Solution ajoutée", "La réponse a bien été ajoutée dans les solutions correcte de la question");
                
                // Le div contenant le tableau de données et à nouveau demandé au serveur
                // par Ajax et le contenu est mis à jour grâce à la méthode load de jQuery
                $("#tables-container" ).load("quiz/" + quiz_id + "/advanced-stats #stats-tables", function() {
                    bind_show();
                });
            }
        });
    });
});

function bind_show() {
    // Lorsqu'on clique sur un bouton bleu, la réponse correspondante s'affiche
    $(".show-question").click(function() {
        $(".hidden-question").hide();
        
        // L'id de la question correspondante se trouve dans l'attribut data-show
        // du bouton
        var id_question = $(this).attr("data-show");
        $(id_question).show();
    });
    
    // Affichage de toutes les questions lors du cliq sur le bouton "Afficher toutes les questions"
    $("#show-all").click(function() {
        $(".hidden-question").show();
    })
}