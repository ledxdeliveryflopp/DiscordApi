package chat

import (
	"chat_microservice/settings"
	"encoding/json"
	"fmt"
	"github.com/go-playground/validator/v10"
	"github.com/gorilla/mux"
	"log"
	"net/http"
	"strconv"
)

func GetChatInfo(writer http.ResponseWriter, request *http.Request) {
	jsonEncoder := json.NewEncoder(writer)
	writer.Header().Set("Content-Type", "application/json")
	token := request.Header.Get("Authorization")
	var errSchemas settings.Error
	chatID, err := strconv.Atoi(mux.Vars(request)["chat_id"])
	if err != nil {
		log.Printf("Query chat error: %s", err)
		errSchemas.Detail = "Bad chat param."
		jsonEncoder.Encode(errSchemas)
		return
	}
	userId, err := GetTokenPayload(token)
	if err != nil {
		log.Printf("Bad jwt token: %s", err)
		errSchemas.Detail = "Bad token."
		jsonEncoder.Encode(errSchemas)
		return
	}
	chat := make(chan PrivateChat)
	chatError := make(chan error)
	go getInfoAboutPrivateChat(chatID, userId, chat, chatError)
	select {
	case err = <-chatError:
		log.Printf("Find chat error: %s", err)
		errSchemas.Detail = fmt.Sprintf("Error: %s", err)
		jsonEncoder.Encode(errSchemas)
		close(chatError)
		close(chat)
	case chatData := <-chat:
		jsonEncoder.Encode(chatData)
		close(chatError)
		close(chat)
		return
	}
}

func AddMessageInChat(writer http.ResponseWriter, request *http.Request) {
	jsonEncoder := json.NewEncoder(writer)
	writer.Header().Set("Content-Type", "application/json")
	token := request.Header.Get("Authorization")
	var errSchemas settings.Error
	chatID, err := strconv.Atoi(mux.Vars(request)["chat_id"])
	if err != nil {
		log.Printf("Query chat error: %s", err)
		errSchemas.Detail = "Bad chat param."
		jsonEncoder.Encode(errSchemas)
		return
	}
	userId, err := GetTokenPayload(token)
	if err != nil {
		log.Printf("Bad jwt token: %s", err)
		errSchemas.Detail = "Bad token."
		jsonEncoder.Encode(errSchemas)
		return
	}
	var messageSchemas MessageCreate
	err = json.NewDecoder(request.Body).Decode(&messageSchemas)
	if err != nil {
		log.Printf("Request body decode err: %s", err)
		errSchemas.Detail = "Read request body error."
		jsonEncoder.Encode(errSchemas)
		return
	}
	validate := validator.New()
	err = validate.Struct(messageSchemas)
	if err != nil {
		errors := fmt.Sprintf("Validation error: %s", err.(validator.ValidationErrors))
		errSchemas.Detail = errors
		jsonEncoder.Encode(errSchemas)
		return
	}
	messageErr := make(chan error)
	success := make(chan int)
	go addMessageInChatRepository(chatID, userId, messageSchemas, success, messageErr)
	select {
	case err = <-messageErr:
		log.Printf("Add message error: %s", err)
		errSchemas.Detail = "Add message error."
		jsonEncoder.Encode(errSchemas)
		close(messageErr)
		close(success)
		return
	case <-success:
		var message struct {
			Detail string `json:"Detail"`
		}
		message.Detail = "Success add."
		jsonEncoder.Encode(message)
		close(messageErr)
		close(success)
		return
	}
}

func GetLastMessageFromChat(writer http.ResponseWriter, request *http.Request) {
	jsonEncoder := json.NewEncoder(writer)
	writer.Header().Set("Content-Type", "application/json")
	var errSchemas settings.Error
	chatID, chatIdErr := strconv.Atoi(mux.Vars(request)["chat_id"])
	limit, limitErr := strconv.Atoi(request.URL.Query().Get("limit"))
	offset, offsetErr := strconv.Atoi(request.URL.Query().Get("offset"))
	switch {
	case chatIdErr != nil:
		log.Printf("Query chat error: %s", chatIdErr)
		errSchemas.Detail = "Bad chat param."
		jsonEncoder.Encode(errSchemas)
		return
	case limitErr != nil:
		log.Printf("Query limit error: %s", limitErr)
		errSchemas.Detail = "Bad limit param."
		jsonEncoder.Encode(errSchemas)
		return
	case offsetErr != nil:
		log.Printf("Query offset error: %s", offsetErr)
		errSchemas.Detail = "Bad offset param."
		jsonEncoder.Encode(errSchemas)
		return
	case offset > limit:
		errSchemas.Detail = "offset cannot be greater than limit."
		jsonEncoder.Encode(errSchemas)
		return
	}
	messages := make(chan []Message)
	messagesErr := make(chan error)
	go getLastMessageFromChatRepository(chatID, limit, offset, messages, messagesErr)
	select {
	case msg := <-messages:
		jsonEncoder.Encode(msg)
		close(messagesErr)
		close(messages)
	case err := <-messagesErr:
		log.Printf("Find messages error: %s", err)
		errSchemas.Detail = "Find messages error, maybe bad chat id."
		jsonEncoder.Encode(errSchemas)
		close(messagesErr)
		close(messages)
	}
}
