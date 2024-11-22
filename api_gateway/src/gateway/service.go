package gateway

import "net/http"

func GetTokenInfo(writer http.ResponseWriter, request *http.Request) {
	getInfoAboutToken(writer, request)
	writer.WriteHeader(http.StatusOK)
}
