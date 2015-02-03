var utils = {

// Affiche une boîte de dialogue basique
alert_dialog : function(title, message) {
    $("#generic-dialog-title").text(title);
    $("#generic-dialog-message").text(message);
    $("#generic-dialog").modal("show");
}

};