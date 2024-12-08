package settings

import (
	"encoding/json"
	"net/http"
)

type ErrorSchemas struct {
	Detail string `json:"Detail"`
}

func RaiseError(writer http.ResponseWriter, errorDetail string, code int) {
	writer.Header().Set("Content-Type", "application/json")
	writer.WriteHeader(code)
	var errorSchemas ErrorSchemas
	errorSchemas.Detail = errorDetail
	json.NewEncoder(writer).Encode(errorSchemas)
	return
}
