package transport

import (
	"github.com/gorilla/mux"
	"net/http"
	"private_messages_microservice/internal/configs"
	"private_messages_microservice/internal/services"
)

func setHandler(mainRouter *mux.Router) {
	chatRouter := mainRouter.PathPrefix("/private").Subrouter()
	chatRouter.HandleFunc("/{chat_id}/messages", services.GetLastMessageFromChat).Methods("GET")
	chatRouter.HandleFunc("/{chat_id}/info/", services.GetChatInfo).Methods("GET")
	chatRouter.HandleFunc("/chat-list/", services.GetUserChatList).Methods("GET")
	chatRouter.HandleFunc("/add-message/{chat_id}/", services.AddMessageInChat).Methods("POST")
	chatRouter.HandleFunc("/start-chat/", services.StartPrivateChat).Methods("POST")
}

func SetRouters() *mux.Router {
	mainRouter := mux.NewRouter()
	mainRouter.NotFoundHandler = http.HandlerFunc(configs.ErrorNotFoundHandler)
	mainRouter.MethodNotAllowedHandler = http.HandlerFunc(configs.ErrorBadRequestHandler)
	setHandler(mainRouter)
	return mainRouter
}
