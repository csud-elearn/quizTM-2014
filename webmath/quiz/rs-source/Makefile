OUTPUT_DIR = ../static/quiz/js/rs-compiled
RS_OPTS = -p --screw-ie8

interpreter: interpreter.pyj
	rapydscript interpreter.pyj -o $(OUTPUT_DIR)/interpreter.js $(RS_OPTS)

toolbar: toolbar.pyj
	rapydscript toolbar.pyj -o $(OUTPUT_DIR)/toolbar.js $(RS_OPTS)

find_url: find_url.pyj
	rapydscript find_url.pyj -o $(OUTPUT_DIR)/find_url.js $(RS_OPTS)

all: interpreter toolbar find_url
