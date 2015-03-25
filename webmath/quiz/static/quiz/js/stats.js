$( document ).ready(function() {
    $(".show-question").click(function() {
        $(".hidden-question").hide();
        var id_question = $(this).attr("data-show");
        $(id_question).show();
    });
    
    $(".add-correct-answer").click(function() {
        var csrftoken = utils.getcookie("csrftoken");
        $.ajax({
            "url": "/quiz/add-correct-answer/",
            "type": "POST",
            "data" : {
                "answer" : $(this).attr("data-answer-id"),
                "csrfmiddlewaretoken" : csrftoken,
            },
            "dataType": "text",
        });
    });
});