$( document ).ready(function() {
    $(".panel-click .panel-heading").click(function() {
            if ($(this).parent().hasClass("content-hidden")) {
                $(this).next().show();
                $(this).parent().removeClass("content-hidden");
            }
            else {
                $(this).next().hide();
                $(this).parent().addClass("content-hidden");
            }
    });
});