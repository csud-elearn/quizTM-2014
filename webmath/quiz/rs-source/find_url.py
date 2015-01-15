def main():
	$("#search").click(search_quiz)

def search_quiz():
	id_quiz = $("#find-input").val()
	$.ajax({
		"url" : "/quiz/findquiz/",
		"type" : "GET",
		"dataType" : "json",
		"data" : "quiz=" + id_quiz,
		"success" : update_url,
		"error" : error,
	})

def update_url(response, status):
	$message_box = $("#message-quiz")
	$message_box.css({"display" : "block"})
	$message_box.empty()

	$message_box.attr({"class" : "alert alert-success"})
	title = response["title"]
	url = response["url"]
	$("<a>", {"href" : url, "class" : "alert-link"}).append(title).appendTo($message_box)
	$message_box.append(" (Cliquez pour accéder)")
		

def error(response, status):
	$message_box = $("#message-quiz")
	$message_box.css({"display" : "block"})
	$message_box.empty()

	$message_box.attr({"class" : "alert alert-danger"}).append("Ce quiz n'existe pas ou a été supprimé")


jQuery(document).ready(main)