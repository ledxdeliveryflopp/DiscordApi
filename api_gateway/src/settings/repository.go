package settings

import (
	"errors"
	"fmt"
)

func GetTokenFromDatabase(token string) (TokenApi, error) {
	// Получить токен из бд
	database := GetDb()
	var tokenSchemas TokenApi
	queryStr := fmt.Sprintf("SELECT * FROM Tokens WHERE Token = '%s'\n", token)
	result := database.Raw(queryStr).Scan(&tokenSchemas)
	if result.Error != nil {
		fmt.Println("token get error", result.Error)
		return TokenApi{}, errors.New("token get error")
	}
	return tokenSchemas, nil
}

func DeleteTokenFromDatabase(token string) error {
	// удалить токен
	database := GetDb()
	var tokenSchemas TokenApi
	queryStr := fmt.Sprintf("DELETE FROM Tokens WHERE Token = '%s'\n", token)
	result := database.Raw(queryStr).Scan(&tokenSchemas)
	if result.Error != nil {
		fmt.Println("token delete error", result.Error)
		return errors.New("token delete error")
	}
	return nil
}
