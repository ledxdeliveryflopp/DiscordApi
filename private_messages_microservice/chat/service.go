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
	chatID, err := strconv.Atoi(mux.Vars(request)["chat_id"])
	if err != nil {
		log.Printf("Query chat error: %s", err)
		settings.RaiseError(writer, "Bad chat id.", 400)
		return
	}
	userId, err := GetTokenPayload(token)
	if err != nil {
		log.Printf("Bad jwt token: %s", err)
		settings.RaiseError(writer, "Bad token.", 400)
		return
	}
	chat := make(chan PrivateChat)
	chatError := make(chan error)
	go getInfoAboutPrivateChat(chatID, userId, chat, chatError)
	select {
	case err = <-chatError:
		log.Printf("Find chat error: %s", err)
		errStr := fmt.Sprintf("Error: %s", err)
		settings.RaiseError(writer, errStr, 400)
		close(chatError)
		close(chat)
		return
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
	var errSchemas settings.ErrorSchemas
	chatID, err := strconv.Atoi(mux.Vars(request)["chat_id"])
	if err != nil {
		log.Printf("Query chat error: %s", err)
		settings.RaiseError(writer, "Bad chat id.", 400)
		return
	}
	userId, err := GetTokenPayload(token)
	if err != nil {
		log.Printf("Bad jwt token: %s", err)
		settings.RaiseError(writer, "Bad token.", 400)
		return
	}
	var messageSchemas MessageCreate
	err = json.NewDecoder(request.Body).Decode(&messageSchemas)
	if err != nil {
		log.Printf("Request body decode err: %s", err)
		settings.RaiseError(writer, "Read request body error.", 400)
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
		settings.RaiseError(writer, "Add message error.", 400)
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
	chatID, chatIdErr := strconv.Atoi(mux.Vars(request)["chat_id"])
	limit, limitErr := strconv.Atoi(request.URL.Query().Get("limit"))
	offset, offsetErr := strconv.Atoi(request.URL.Query().Get("offset"))
	token := request.Header.Get("Authorization")
	userId, err := GetTokenPayload(token)
	switch {
	case err != nil:
		log.Printf("Bad jwt token: %s", err)
		settings.RaiseError(writer, "Bad token.", 400)
		return
	case chatIdErr != nil:
		log.Printf("Query chat error: %s", chatIdErr)
		settings.RaiseError(writer, "Bad chat param.", 400)
		return
	case limitErr != nil:
		log.Printf("Query limit error: %s", limitErr)
		settings.RaiseError(writer, "Bad limit param.", 400)
		return
	case offsetErr != nil:
		log.Printf("Query offset error: %s", offsetErr)
		settings.RaiseError(writer, "Bad offset param.", 400)
		return
	case offset > limit:
		settings.RaiseError(writer, "offset cannot be greater than limit.", 400)
		return
	case offset < 0 || offset == 1:
		settings.RaiseError(writer, "offset cannot be less than 0 or equal to 1.", 400)
		return
	}
	messages := make(chan []Message)
	messagesErr := make(chan error)
	go getLastMessageFromChatRepository(chatID, userId, limit, offset, messages, messagesErr)
	select {
	case msg := <-messages:
		jsonEncoder.Encode(msg)
		close(messagesErr)
		close(messages)
		return
	case err := <-messagesErr:
		log.Printf("Find messages error: %s", err)
		errorStr := fmt.Sprintf("Find messages error: %s", err)
		settings.RaiseError(writer, errorStr, 400)
		close(messagesErr)
		close(messages)
		return
	}
}
