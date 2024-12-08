package settings

import (
	"encoding/json"
	"net/http"
)

func ErrorNotFoundHandler(writer http.ResponseWriter, request *http.Request) {
	writer.Header().Set("Content-Type", "application/json")
	jsonEncoder := json.NewEncoder(writer)
	var errSchemas ErrorSchemas
	errSchemas.Detail = "Not found."
	jsonEncoder.Encode(errSchemas)
	return
}

func ErrorBadRequestHandler(writer http.ResponseWriter, request *http.Request) {
	writer.Header().Set("Content-Type", "application/json")
	jsonEncoder := json.NewEncoder(writer)
	var errSchemas ErrorSchemas
	errSchemas.Detail = "Bad request method."
	jsonEncoder.Encode(errSchemas)
	return
}
