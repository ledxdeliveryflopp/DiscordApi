package settings

import (
	"embed"
	"fmt"
	"github.com/driftprogramming/godotenv"
)

func InitSettings(envPath embed.FS) bool {
	// инициализация env
	err := godotenv.Load(envPath, "env/.env")
	if err != nil {
		fmt.Println("init settings error", err)
		return false
	}
	fmt.Println("Env inited")
	return true
}

func GetTokenSettings() []byte {
	// секретный ключ из env
	secret := godotenv.Get("SECRET")
	return []byte(secret)
}

func GetDatabaseUrl() string {
	// Создать url БД
	host := godotenv.Get("HOST")
	port := godotenv.Get("PORT")
	user := godotenv.Get("USER")
	password := godotenv.Get("PASSWORD")
	dbname := godotenv.Get("NAME")
	databaseUrl := fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s sslmode=disable\n",
		host, user, password, dbname, port)
	return databaseUrl
}
