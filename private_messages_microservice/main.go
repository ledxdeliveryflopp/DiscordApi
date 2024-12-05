package main

import (
	"chat_microservice/chat"
	"chat_microservice/settings"
	"embed"
	"github.com/gorilla/mux"
	"net/http"
)

//go:embed environment/*
var env embed.FS

////go:embed migrations/*.sql
//var dbMigrations embed.FS

//go:embed migrations/seeder/*.sql
var fakeDbMigrations embed.FS

// Установка роутеров и запуск сервера
func startServer(port string) {
	settings.InitSettings(env)
	//settings.MigrateDatabase(dbMigrations)
	settings.SeedFakeDataInDB(fakeDbMigrations)
	mainRouter := mux.NewRouter()
	mainRouter.NotFoundHandler = http.HandlerFunc(settings.ErrorNotFoundHandler)
	mainRouter.MethodNotAllowedHandler = http.HandlerFunc(settings.ErrorBadRequestHandler)
	chat.SetUpPrivateRouter(mainRouter)
	err := http.ListenAndServe(port, mainRouter)
	if err != nil {
		panic(err)
	}
}

func main() {
	startServer(":6000")
}
