package main

import (
	"api_gateway/src/gateway"
	"api_gateway/src/settings"
	"embed"
	"fmt"
	"github.com/gorilla/mux"
	"net/http"
)

//go:embed env/*
var env embed.FS

func main() {
	//Запуск приложения
	apiGatewayRouter := mux.NewRouter()
	gateway.InitGatewayRouter(apiGatewayRouter)
	EnvInit := settings.InitSettings(env)
	if EnvInit == false {
		return
	}
	fmt.Println("Start server")
	err := http.ListenAndServe("0.0.0.0:9000", apiGatewayRouter)
	if err != nil {
		fmt.Println("Start server error", err)
		return
	}
}
