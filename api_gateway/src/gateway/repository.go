package gateway

import (
	"api_gateway/src/settings"
	"encoding/json"
	"fmt"
	"net/http"
)

func getInfoAboutToken(writer http.ResponseWriter, request *http.Request) {
	// Получение информации о токене
	tokenFromHeader := request.Header.Get("Authorization")
	writer.Header().Set("Content-Type", "application/json")
	fmt.Println("Token from header", tokenFromHeader)
	token := settings.GetTokenFromDatabase(tokenFromHeader)
	if token == false {
		writer.WriteHeader(http.StatusForbidden)
		settings.BadToken(writer, request)
		return
	}
	err := json.NewEncoder(writer).Encode(token)
	if err != nil {
		fmt.Println("encode error", err)
	}
}
