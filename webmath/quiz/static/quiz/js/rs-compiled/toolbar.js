(function(){
    function len(obj) {
        if (obj instanceof Array || typeof obj === "string") return obj.length;
        else {
            var count = 0;
            for (var i in obj) {
                if (obj.hasOwnProperty(i)) count++;
            }
            return count;
        }
    }
    "\nLie les boutons de la barre d'outils aux actions correspondantes\n";
    function toolbar_main() {
        $(".tag-insert").click_foreach(insert_tag);
        $("#savedraft-btn").click(open_savedraft);
        $("#submitdraft-btn").click(submitdraft);
        $("#importdraft-btn").click(get_draftlist);
    }
    function insert_tag() {
        var selection, code, tag_after, tag_before;
        selection = $("#quizcode").range();
        code = $("#quizcode").val();
        tag_before = $(this).attr("data-tag-before");
        tag_after = $(this).attr("data-tag-after");
        if (!tag_after) {
            tag_after = "";
        }
        if ($(this).hasClass("lb-required")) {
            if (selection.start > 0 && code[selection.start - 1] !== "\n") {
                tag_before = "\n" + tag_before;
            }
        }
        $("#quizcode").range(tag_before + selection.text + tag_after);
        if (len(selection.text) > 0) {
            $("#quizcode").range(selection.start + len(tag_before), selection.end + len(tag_before));
        } else {
            $("#quizcode").caret(selection.start + len(tag_before));
        }
        show_lines();
    }
    function open_savedraft() {
        "\n    Ouvre une boîte de dialogue permettant d'enregistrer un brouillon\n    ";
        $("#draft-title").val($("#title").val());
        $("#save-status").hide();
        $("#submitdraft-btn").show();
        $("#savedraft-box").modal("show");
    }
    function submitdraft() {
        var csrftoken, quizcode, title;
        "\n    Enregistre le brouillon sur le serveur par requête ajax POST\n    ";
        csrftoken = utils.getcookie("csrftoken");
        quizcode = $("#quizcode").val();
        title = $("#draft-title").val();
        if (quizcode && title) {
            $.ajax({
                "url": "/quiz/savedraft/",
                "type": "POST",
                "dataType": "text",
                "data": {
                    "csrfmiddlewaretoken": csrftoken,
                    "title": title,
                    "code": quizcode
                },
                "success": savedraft_success,
                "error": savedraft_error
            });
        } else {
            savedraft_warning();
        }
    }
    function savedraft_message(message, bootstrap_color) {
        var $status_box;
        "\n    Affiche un message relatif à la sauvegarde (success/error/warning) dans la boîte de dialogue\n    ";
        $status_box = $("#save-status");
        $status_box.removeClass("alert-danger alert-warning alert-success");
        $status_box.addClass(bootstrap_color);
        $status_box.text(message);
        $status_box.css("display", "block");
    }
    function savedraft_success() {
        "Enregistrement réussi";
        savedraft_message("Brouillon enregistré", "alert-success");
        $("#submitdraft-btn").hide();
    }
    function savedraft_error() {
        "Échec de l'enregistrement";
        savedraft_message("L'enregistrement a échoué. Veuillez vérifier votre connexion", "alert-danger");
    }
    function savedraft_warning() {
        "Champs vides";
        savedraft_message("Vous devez entrer un titre et ajouter du contenu au quiz", "alert-warning");
    }
    function get_draftlist() {
        "\n    Récupère la liste des brouillons sur le serveur par requête ajax GET\n    ";
        $.ajax({
            "url": "/quiz/listdrafts/",
            "type": "GET",
            "dataType": "json",
            "success": show_draftlist
        });
    }
    function show_draftlist(data) {
        var $draftlist, draft;
        "\n    Affiche la liste des brouillons dans une boîte de dialogue\n    ";
        $draftlist = $("#list-drafts");
        console.log(data);
        if (len(data) > 0) {
            $draftlist.children().remove();
            var _$rapyd$_Iter0 = data;
            for (var _$rapyd$_Index0 = 0; _$rapyd$_Index0 < _$rapyd$_Iter0.length; _$rapyd$_Index0++) {
                draft = _$rapyd$_Iter0[_$rapyd$_Index0];
                $("<a>", {
                    "class": "list-group-item bold",
                    "data-id": draft["id"],
                    "data-dismiss": "modal"
                }).text(draft["title"]).appendTo($draftlist);
            }
            $draftlist.children().click_foreach(importdraft);
        }
        $("#importdraft-box").modal("show");
    }
    function importdraft() {
        var draft_id;
        "\n    Récupère les données du brouillon par requête ajax GET\n    ";
        draft_id = $(this).attr("data-id");
        $.ajax({
            "url": "/quiz/getdraft/",
            "type": "GET",
            "dataType": "json",
            "data": {
                "draft": draft_id
            },
            "success": importdraft_success
        });
    }
    function importdraft_success(data) {
        var title, code;
        "\n    Modifie les champs du quiz avec les données récupérés par ajax\n    ";
        title = data["title"];
        code = data["code"];
        $("#title").val(title);
        $("#quizcode").val(code);
        show_lines();
    }
    $(document).ready(toolbar_main);
})();