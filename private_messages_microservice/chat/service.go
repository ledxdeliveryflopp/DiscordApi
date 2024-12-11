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

func GetUserChatList(writer http.ResponseWriter, request *http.Request) {
	jsonEncoder := json.NewEncoder(writer)
	writer.Header().Set("Content-Type", "application/json")
	token := request.Header.Get("Authorization")
	userId, tokenErr := GetTokenPayload(token)
	if tokenErr != nil {
		log.Printf("Bad jwt token: %s", tokenErr)
		settings.RaiseError(writer, "Bad token.", 400)
		return
	}
	chatList := make(chan []UserChatList)
	chatListError := make(chan error)
	go GetCurrentUserChat(userId, chatList, chatListError)
	select {
	case list := <-chatList:
		jsonEncoder.Encode(list)
		close(chatList)
		close(chatListError)
		return
	case err := <-chatListError:
		errorStr := fmt.Sprintf("%s", err)
		settings.RaiseError(writer, errorStr, 400)
		close(chatList)
		close(chatListError)
		return
	}
}

func GetChatInfo(writer http.ResponseWriter, request *http.Request) {
	jsonEncoder := json.NewEncoder(writer)
	writer.Header().Set("Content-Type", "application/json")
	token := request.Header.Get("Authorization")
	chatID, chatIDErr := strconv.Atoi(mux.Vars(request)["chat_id"])
	userId, tokenErr := GetTokenPayload(token)
	switch {
	case chatIDErr != nil:
		log.Printf("Query chat error: %s", chatIDErr)
		settings.RaiseError(writer, "Bad chat id.", 400)
		return
	case tokenErr != nil:
		log.Printf("Bad jwt token: %s", tokenErr)
		settings.RaiseError(writer, "Bad token.", 400)
		return
	}
	chat := make(chan PrivateChat)
	chatError := make(chan error)
	go getInfoAboutPrivateChat(chatID, userId, chat, chatError)
	select {
	case err := <-chatError:
		errStr := fmt.Sprintf("%s", err)
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
	chatID, chatIDErr := strconv.Atoi(mux.Vars(request)["chat_id"])
	userId, tokenErr := GetTokenPayload(token)
	switch {
	case chatIDErr != nil:
		log.Printf("Query chat error: %s", chatIDErr)
		settings.RaiseError(writer, "Bad chat id.", 400)
		return
	case tokenErr != nil:
		log.Printf("Bad jwt token: %s", tokenErr)
		settings.RaiseError(writer, "Bad token.", 400)
		return
	}
	var messageSchemas MessageCreate
	decodeErr := json.NewDecoder(request.Body).Decode(&messageSchemas)
	validate := validator.New()
	validationErr := validate.Struct(messageSchemas)
	switch {
	case decodeErr != nil:
		log.Printf("Request body decode err: %s", decodeErr)
		settings.RaiseError(writer, "Read request body error.", 400)
		return
	case validationErr != nil:
		errors := fmt.Sprintf("Validation error: %s", validationErr.(validator.ValidationErrors))
		errSchemas.Detail = errors
		jsonEncoder.Encode(errSchemas)
		return
	}
	messageErr := make(chan error)
	success := make(chan int)
	go addMessageInChatRepository(chatID, userId, messageSchemas, success, messageErr)
	select {
	case err := <-messageErr:
		errorStr := fmt.Sprintf("%s", err)
		settings.RaiseError(writer, errorStr, 400)
		close(messageErr)
		close(success)
		return
	case <-success:
		var message struct {
			Detail string `json:"detail"`
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
		errorStr := fmt.Sprintf("%s", err)
		settings.RaiseError(writer, errorStr, 400)
		close(messagesErr)
		close(messages)
		return
	}
}

func StartPrivateChat(writer http.ResponseWriter, request *http.Request) {
	encoder := json.NewEncoder(writer)
	writer.Header().Set("Content-Type", "application/json")
	token := request.Header.Get("Authorization")
	userId, err := GetTokenPayload(token)
	if err != nil {
		settings.RaiseError(writer, "bad token", 400)
		return
	}
	var chatCreateSchemas PrivateChatCreate
	decodeErr := json.NewDecoder(request.Body).Decode(&chatCreateSchemas)
	validate := validator.New()
	validationErr := validate.Struct(chatCreateSchemas)
	switch {
	case decodeErr != nil:
		errors := fmt.Sprintf("Decode error: %s", err)
		settings.RaiseError(writer, errors, 400)
		return
	case validationErr != nil:
		errors := fmt.Sprintf("Validation error: %s", err)
		settings.RaiseError(writer, errors, 400)
		return
	case chatCreateSchemas.RecipientID == userId:
		settings.RaiseError(writer, "current user cannot by recipient", 400)
		return
	}
	chatError := make(chan error)
	newChatID := make(chan int)
	go startPrivateChatRepository(userId, chatCreateSchemas, newChatID, chatError)
	select {
	case chatID := <-newChatID:
		var message struct {
			ChatId string `json:"chat_id"`
		}
		message.ChatId = fmt.Sprintf("%d", chatID)
		encoder.Encode(message)
		close(newChatID)
		close(chatError)
		return
	case err := <-chatError:
		chatErr := fmt.Sprintf("%s", err)
		settings.RaiseError(writer, chatErr, 400)
		close(newChatID)
		close(chatError)
		return
	}

}
