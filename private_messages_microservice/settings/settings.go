package settings

import (
	"embed"
	"fmt"
	"github.com/driftprogramming/godotenv"
	"log"
)

// InitSettings инициализация настроек приложения
func InitSettings(envPath embed.FS) bool {
	err := godotenv.Load(envPath, "environment/.env")
	if err != nil {
		panic(err)
	}
	log.Print("Env inited")
	return true
}

// GetDatabaseUrl Создать url БД
func GetDatabaseUrl() string {
	host := godotenv.Get("HOST")
	port := godotenv.Get("PORT")
	user := godotenv.Get("USER")
	password := godotenv.Get("PASSWORD")
	dbname := godotenv.Get("NAME")
	databaseUrl := fmt.Sprintf("host=%s user=%s port=%s password=%s dbname=%s sslmode=disable\n",
		host, user, port, password, dbname)
	return databaseUrl
}
