package settings

import (
	"encoding/json"
	"net/http"
)

type Error struct {
	Detail string `json:"detail"`
}

func BadToken(writer http.ResponseWriter, request *http.Request) {
	writer.Header().Set("Content-Type", "application/json")
	writer.WriteHeader(http.StatusForbidden)
	message := Error{
		Detail: "Bad token.",
	}
	json.NewEncoder(writer).Encode(message)
}

func UnknownError(writer http.ResponseWriter, request *http.Request) {
	writer.Header().Set("Content-Type", "application/json")
	writer.WriteHeader(http.StatusForbidden)
}
