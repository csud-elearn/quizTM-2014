(function(){
    function main() {
        $("#search").click(search_quiz);
    }
    function search_quiz() {
        var id_quiz;
        id_quiz = $("#find-input").val();
        $.ajax({
            "url": "/findquiz/",
            "type": "GET",
            "dataType": "json",
            "data": "quiz=" + id_quiz,
            "success": update_url,
            "error": error
        });
    }
    function update_url(response, status) {
        var $message_box, title, url;
        $message_box = $("#message-quiz");
        $message_box.css({
            "display": "block"
        });
        $message_box.empty();
        $message_box.removeClass("alert-danger");
        $message_box.addClass("alert-success");
        title = response["title"];
        url = response["url"];
        $("<a>", {
            "href": url,
            "class": "alert-link"
        }).append(title).appendTo($message_box);
        $message_box.append(" (Cliquez pour accéder)");
    }
    function error(response, status) {
        var $message_box;
        $message_box = $("#message-quiz");
        $message_box.css({
            "display": "block"
        });
        $message_box.empty();
        $message_box.removeClass("alert-success");
        $message_box.addClass("alert-danger").append("Ce quiz n'existe pas ou a été supprimé");
    }
    jQuery(document).ready(main);
})();