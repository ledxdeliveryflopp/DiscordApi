package configs

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
	return
}

func UnknownError(writer http.ResponseWriter, request *http.Request) {
	writer.Header().Set("Content-Type", "application/json")
	writer.WriteHeader(http.StatusForbidden)
	message := Error{
		Detail: "Unknow error.",
	}
	json.NewEncoder(writer).Encode(message)
	return
}

func DeleteError(writer http.ResponseWriter, request *http.Request) {
	writer.Header().Set("Content-Type", "application/json")
	writer.WriteHeader(http.StatusForbidden)
	message := Error{
		Detail: "Deletion error.",
	}
	json.NewEncoder(writer).Encode(message)
	return
}
