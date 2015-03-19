$( document ).ready(function() {
    $(".show-question").click(function() {
        $(".hidden-question").hide();
        var id_question = $(this).attr("data-show")
        $(id_question).show()
    });
});