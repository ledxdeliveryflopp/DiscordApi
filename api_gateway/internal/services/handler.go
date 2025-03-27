package services

import (
	"api_gateway/internal/configs"
	"api_gateway/internal/database"
	"encoding/json"
	log "github.com/sirupsen/logrus"
	"net/http"
	"time"
)

func GetInfoAboutToken(writer http.ResponseWriter, request *http.Request) {
	tokenFromHeader := request.Header.Get("Authorization")
	writer.Header().Set("Content-Type", "application/json")
	token, tokenErr := database.GetTokenFromDatabase(tokenFromHeader)
	if tokenErr != nil {
		configs.BadToken(writer, request)
		return
	}
	expireTime := token.Expire
	currTime := time.Now().Round(0)
	tokenExpired := expireTime.After(currTime)
	if tokenExpired == false {
		err := database.DeleteTokenFromDatabase(token.Token)
		if err != nil {
			configs.DeleteError(writer, request)
			return
		}
		configs.BadToken(writer, request)
		return
	}
	err := json.NewEncoder(writer).Encode(token)
	if err != nil {
		log.Errorf("Token encode error: %s", err)
		configs.UnknownError(writer, request)
		return
	}
}
