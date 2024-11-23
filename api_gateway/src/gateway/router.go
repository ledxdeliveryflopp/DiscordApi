package gateway

import (
	"fmt"
	"github.com/gorilla/mux"
)

func InitGatewayRouter(router *mux.Router) {
	// Инициализация роутера api gateway
	tokenRouter := router.PathPrefix("/gateway").Subrouter()
	tokenRouter.HandleFunc("/get-token/", GetTokenInfo).Methods("Get")
	fmt.Println("Token router inited")
}
