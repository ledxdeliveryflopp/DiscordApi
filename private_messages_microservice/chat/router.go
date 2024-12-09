package chat

import "github.com/gorilla/mux"

func SetUpPrivateRouter(mainRouter *mux.Router) {
	chatRouter := mainRouter.PathPrefix("/private").Subrouter()
	chatRouter.HandleFunc("/{chat_id}/messages", GetLastMessageFromChat).Methods("GET")
	chatRouter.HandleFunc("/{chat_id}/info/", GetChatInfo).Methods("GET")
	chatRouter.HandleFunc("/add-message/{chat_id}/", AddMessageInChat).Methods("POST")
	chatRouter.HandleFunc("/start-chat/", StartPrivateChat).Methods("POST")
}
