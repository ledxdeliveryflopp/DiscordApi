package settings

import "fmt"

func GetTokenFromDatabase(token string) interface{} {
	// Получить объект из бд
	database := GetDb()
	var tokenModel Token
	result := database.First(&tokenModel, "token = ?", token)
	if result.Error != nil {
		fmt.Println("token get error", result.Error)
		return false
	}
	fmt.Println("token from db", tokenModel)
	return tokenModel
}
