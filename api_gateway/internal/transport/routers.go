package transport

import (
	"api_gateway/internal/services"
	"github.com/gorilla/mux"
)

func setHandler(router *mux.Router) {
	tokenRouter := router.PathPrefix("/gateway").Subrouter()
	tokenRouter.HandleFunc("/get-token/", services.GetInfoAboutToken).Methods("Get")
}

func SetRouters() *mux.Router {
	mainRouter := mux.NewRouter()
	setHandler(mainRouter)
	return mainRouter
}
