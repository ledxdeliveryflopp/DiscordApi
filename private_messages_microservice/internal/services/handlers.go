package services

import (
	"encoding/json"
	"fmt"
	"github.com/go-playground/validator/v10"
	"github.com/gorilla/mux"
	"log"
	"net/http"
	"private_messages_microservice/internal/configs"
	"private_messages_microservice/internal/database"
	"private_messages_microservice/internal/jwt_tokens"
	"private_messages_microservice/internal/types"
	"strconv"
)

func GetUserChatList(writer http.ResponseWriter, request *http.Request) {
	jsonEncoder := json.NewEncoder(writer)
	writer.Header().Set("Content-Type", "application/json")
	token := request.Header.Get("Authorization")
	userId, tokenErr := jwt_tokens.GetTokenPayload(token)
	if tokenErr != nil {
		log.Printf("Bad jwt token: %s", tokenErr)
		configs.RaiseError(writer, "Bad token.", 400)
		return
	}
	chatList, err := database.GetCurrentUserChat(userId)
	if err != nil {
		errorStr := fmt.Sprintf("%s", err)
		configs.RaiseError(writer, errorStr, 400)
		return
	}
	jsonEncoder.Encode(chatList)
	return
}

func GetChatInfo(writer http.ResponseWriter, request *http.Request) {
	jsonEncoder := json.NewEncoder(writer)
	writer.Header().Set("Content-Type", "application/json")
	token := request.Header.Get("Authorization")
	chatID, chatIDErr := strconv.Atoi(mux.Vars(request)["chat_id"])
	userId, tokenErr := jwt_tokens.GetTokenPayload(token)
	switch {
	case chatIDErr != nil:
		log.Printf("Query chat error: %s", chatIDErr)
		configs.RaiseError(writer, "Bad chat id.", 400)
		return
	case tokenErr != nil:
		log.Printf("Bad jwt token: %s", tokenErr)
		configs.RaiseError(writer, "Bad token.", 400)
		return
	}
	chat, err := database.GetInfoAboutPrivateChat(chatID, userId)
	if err != nil {
		errorStr := fmt.Sprintf("%s", err)
		configs.RaiseError(writer, errorStr, 400)
		return
	}
	jsonEncoder.Encode(chat)
	return
}

func AddMessageInChat(writer http.ResponseWriter, request *http.Request) {
	jsonEncoder := json.NewEncoder(writer)
	writer.Header().Set("Content-Type", "application/json")
	token := request.Header.Get("Authorization")
	var errSchemas configs.ErrorSchemas
	chatID, chatIDErr := strconv.Atoi(mux.Vars(request)["chat_id"])
	userId, tokenErr := jwt_tokens.GetTokenPayload(token)
	switch {
	case chatIDErr != nil:
		log.Printf("Query chat error: %s", chatIDErr)
		configs.RaiseError(writer, "Bad chat id.", 400)
		return
	case tokenErr != nil:
		log.Printf("Bad jwt token: %s", tokenErr)
		configs.RaiseError(writer, "Bad token.", 400)
		return
	}
	var messageSchemas types.MessageCreate
	decodeErr := json.NewDecoder(request.Body).Decode(&messageSchemas)
	validate := validator.New()
	validationErr := validate.Struct(messageSchemas)
	switch {
	case decodeErr != nil:
		log.Printf("Request body decode err: %s", decodeErr)
		configs.RaiseError(writer, "Read request body error.", 400)
		return
	case validationErr != nil:
		errors := fmt.Sprintf("Validation error: %s", validationErr.(validator.ValidationErrors))
		errSchemas.Detail = errors
		jsonEncoder.Encode(errSchemas)
		return
	}
	err := database.AddMessageInChatRepository(chatID, userId, messageSchemas)
	if err != nil {
		errorStr := fmt.Sprintf("%s", err)
		configs.RaiseError(writer, errorStr, 400)
		return
	}
	var message struct {
		Detail string `json:"detail"`
	}
	message.Detail = "Success add."
	jsonEncoder.Encode(message)
	return
}

func GetLastMessageFromChat(writer http.ResponseWriter, request *http.Request) {
	writer.Header().Set("Content-Type", "application/json")
	chatID, chatIdErr := strconv.Atoi(mux.Vars(request)["chat_id"])
	limit, limitErr := strconv.Atoi(request.URL.Query().Get("limit"))
	offset, offsetErr := strconv.Atoi(request.URL.Query().Get("offset"))
	token := request.Header.Get("Authorization")
	userId, err := jwt_tokens.GetTokenPayload(token)
	switch {
	case err != nil:
		log.Printf("Bad jwt token: %s", err)
		configs.RaiseError(writer, "Bad token.", 400)
		return
	case chatIdErr != nil:
		log.Printf("Query chat error: %s", chatIdErr)
		configs.RaiseError(writer, "Bad chat param.", 400)
		return
	case limitErr != nil:
		log.Printf("Query limit error: %s", limitErr)
		configs.RaiseError(writer, "Bad limit param.", 400)
		return
	case offsetErr != nil:
		log.Printf("Query offset error: %s", offsetErr)
		configs.RaiseError(writer, "Bad offset param.", 400)
		return
	case offset > limit:
		configs.RaiseError(writer, "offset cannot be greater than limit.", 400)
		return
	case offset < 0 || offset == 1:
		configs.RaiseError(writer, "offset cannot be less than 0 or equal to 1.", 400)
		return
	}
	messages, err := database.GetLastMessageFromChatRepository(chatID, userId, limit, offset)
	if err != nil {
		errorStr := fmt.Sprintf("%s", err)
		configs.RaiseError(writer, errorStr, 400)
		return
	}
	jsonEncoder := json.NewEncoder(writer)
	jsonEncoder.Encode(messages)
	return
}

func StartPrivateChat(writer http.ResponseWriter, request *http.Request) {
	encoder := json.NewEncoder(writer)
	writer.Header().Set("Content-Type", "application/json")
	token := request.Header.Get("Authorization")
	userId, err := jwt_tokens.GetTokenPayload(token)
	if err != nil {
		configs.RaiseError(writer, "bad token", 400)
		return
	}
	var chatCreateSchemas types.PrivateChatCreate
	decodeErr := json.NewDecoder(request.Body).Decode(&chatCreateSchemas)
	validate := validator.New()
	validationErr := validate.Struct(chatCreateSchemas)
	switch {
	case decodeErr != nil:
		errors := fmt.Sprintf("Decode error: %s", err)
		configs.RaiseError(writer, errors, 400)
		return
	case validationErr != nil:
		errors := fmt.Sprintf("Validation error: %s", err)
		configs.RaiseError(writer, errors, 400)
		return
	case chatCreateSchemas.RecipientID == userId:
		configs.RaiseError(writer, "current user cannot by recipient", 400)
		return
	}
	newChatID, err := database.StartPrivateChatRepository(userId, chatCreateSchemas)
	if err != nil {
		chatErr := fmt.Sprintf("%s", err)
		configs.RaiseError(writer, chatErr, 400)
		return
	}
	var message struct {
		ChatId string `json:"chat_id"`
	}
	message.ChatId = fmt.Sprintf("%d", newChatID)
	encoder.Encode(message)
	return
}
