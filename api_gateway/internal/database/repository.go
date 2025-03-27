package database

import (
	"api_gateway/internal/configs"
	"api_gateway/internal/types"
	"errors"
	log "github.com/sirupsen/logrus"
)

func GetTokenFromDatabase(token string) (types.JwtToken, error) {
	var tokenSchemas types.JwtToken
	result := configs.DatabaseConnection.QueryRow("SELECT * FROM Tokens WHERE Token = $1", token)
	err := result.Scan(&tokenSchemas.Token, &tokenSchemas.Expire)
	if err != nil {
		log.Errorf("Find token error: %s", err)
		return types.JwtToken{}, err
	}
	return tokenSchemas, nil
}

func DeleteTokenFromDatabase(token string) error {
	_, err := configs.DatabaseConnection.Exec("DELETE FROM Tokens WHERE Token =  $1", token)
	if err != nil {
		log.Errorf("Delete token error: %s", err)
		return errors.New("token delete error")
	}
	return nil
}
