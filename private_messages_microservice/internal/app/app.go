package app

import (
	log "github.com/sirupsen/logrus"
	"net/http"
	"private_messages_microservice/internal/configs"
	"private_messages_microservice/internal/transport"
)

////go:embed migrations/seeder/*.sql
//var fakeDbMigrations embed.FS

// StartApi Установка роутеров и запуск сервера
func StartApi(port string) {
	configs.InitLogrus()
	configs.InitSettings("user", "5432", "postgres", "admin", "user")
	configs.MigrateDatabase()
	//settings.SeedFakeDataInDB(fakeDbMigrations)
	mainRouter := transport.SetRouters()
	configs.ConnectToBd()
	defer configs.DatabaseConnection.Close()
	err := http.ListenAndServe(port, mainRouter)
	if err != nil {
		log.Panic(err)
	}
}
