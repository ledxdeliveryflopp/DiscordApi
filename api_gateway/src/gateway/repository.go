package gateway

import (
	"api_gateway/src/settings"
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

func getInfoAboutToken(writer http.ResponseWriter, request *http.Request) {
	// Получение информации о токене
	tokenFromHeader := request.Header.Get("Authorization")
	writer.Header().Set("Content-Type", "application/json")
	token, tokenErr := settings.GetTokenFromDatabase(tokenFromHeader)
	if tokenErr != nil || token.Token == "" {
		settings.BadToken(writer, request)
		return
	}
	expireTime := token.Expire
	currTime := time.Now().Round(0)
	tokenExpired := expireTime.After(currTime)
	if tokenExpired == false {
		err := settings.DeleteTokenFromDatabase(token.Token)
		if err != nil {
			settings.DeleteError(writer, request)
			return
		}
		settings.BadToken(writer, request)
		return
	}
	err := json.NewEncoder(writer).Encode(token)
	if err != nil {
		fmt.Println("encode error", err)
	}
}
