package database

import (
	"database/sql"
	"errors"
	"log"
	"private_messages_microservice/internal/configs"
	"private_messages_microservice/internal/types"
	"reflect"
)

func GetCurrentUserChat(userID int) ([]types.UserChatList, error) {
	rows, err := configs.DatabaseConnection.Query("SELECT private_chat.id FROM private_chat JOIN users ON (private_chat.chat_starter_id = users.id OR private_chat.chat_recipient_id = users.id) WHERE users.id = $1", userID)
	if err != nil {
		return nil, nil
	}
	var chatListSchemas []types.UserChatList
	for rows.Next() {
		var list types.UserChatList
		err := rows.Scan(&list.ID)
		if errors.Is(err, sql.ErrNoRows) {
			return nil, errors.New("empty chat list")
		}
		chatListSchemas = append(chatListSchemas, list)
	}
	return chatListSchemas, nil
}

func GetInfoAboutPrivateChat(chatID int, userID int) (types.PrivateChat, error) {
	row, err := configs.DatabaseConnection.Query("SELECT chat.id, starter.id, starter.username, recipient.id, recipient.username FROM private_chat chat JOIN users starter ON (chat.chat_starter_id = starter.id) JOIN users recipient ON (chat.chat_recipient_id = recipient.id) where chat.id = $1", chatID)
	if err != nil {
		return types.PrivateChat{}, err
	}
	defer row.Close()
	var chatSchemas types.PrivateChat
	for row.Next() {
		err := row.Scan(&chatSchemas.ID, &chatSchemas.ChatStarter.ID, &chatSchemas.ChatStarter.Username,
			&chatSchemas.ChatRecipient.ID, &chatSchemas.ChatRecipient.Username)
		if err != nil {
			return types.PrivateChat{}, err
		}
	}
	chatSchemasCheck := types.PrivateChat{}
	switch {
	case chatSchemas == chatSchemasCheck:
		return types.PrivateChat{}, errors.New("chat not found")
	case userID == chatSchemas.ChatRecipient.ID || userID == chatSchemas.ChatStarter.ID:
		return chatSchemas, nil
	case userID != chatSchemas.ChatRecipient.ID || userID != chatSchemas.ChatStarter.ID:
		return types.PrivateChat{}, errors.New("current user not in this chat")
	}
	return types.PrivateChat{}, errors.New("unknown error")
}

func checkUserInChat(userID int, chatID int) error {
	row := configs.DatabaseConnection.QueryRow("SELECT * FROM private_chat WHERE id = $1", chatID)
	var checkPrivateChat types.CheckPrivateChat
	err := row.Scan(&checkPrivateChat.ID, &checkPrivateChat.ChatStarter, &checkPrivateChat.ChatRecipient)
	switch {
	case errors.Is(err, sql.ErrNoRows):
		return errors.New("chat not found")
	case checkPrivateChat.ChatStarter == userID || checkPrivateChat.ChatRecipient == userID:
		return nil
	default:
		return errors.New("current user is not in this chat")
	}
}

func checkMessageExistForAnswer(chatID int, messageID int) error {
	switch {
	case reflect.ValueOf(messageID).IsZero() == false:
		row := configs.DatabaseConnection.QueryRow("SELECT id FROM message WHERE id = $1 AND chat_id = $2", messageID, chatID)
		var chatDbID int
		err := row.Scan(&chatDbID)
		if errors.Is(err, sql.ErrNoRows) {
			return errors.New("answer message not found")
		}
		return nil
	default:
		return nil
	}
}

func checkUserExist(userID int) error {
	row := configs.DatabaseConnection.QueryRow("SELECT id FROM users WHERE id = $1", userID)
	var userDbId int
	err := row.Scan(&userDbId)
	if errors.Is(err, sql.ErrNoRows) {
		return errors.New("recipient user not found")
	}
	return nil
}

func AddMessageInChatRepository(chatID int, userID int, message types.MessageCreate) error {
	checkAnswerErr := checkMessageExistForAnswer(chatID, message.Answer)
	if checkAnswerErr != nil {
		return checkAnswerErr
	}
	checkUserErr := checkUserInChat(userID, chatID)
	if checkUserErr != nil {
		return checkUserErr
	}
	tx, err := configs.DatabaseConnection.Begin()
	if err != nil {
		log.Printf("Begin tx error in add message: %s", err)
		return err
	}
	defer tx.Rollback()
	if reflect.ValueOf(message.Answer).IsZero() == true {
		_, err = tx.Exec("INSERT INTO message (text, owner_id, chat_id) VALUES ($1, $2, $3)", message.Text, userID, chatID)
		if err != nil {
			log.Printf("Add message exec error: %s", err)
			return err
		}
		return nil
	}
	_, err = tx.Exec("INSERT INTO message (text, answer, owner_id, chat_id) VALUES ($1, $2, $3, $4)", message.Text, message.Answer, userID, chatID)
	if err != nil {
		log.Printf("Add message exec error: %s", err)
		return err
	}
	return nil
}

func GetLastMessageFromChatRepository(chatID int, userID int, limit int, offset int) ([]types.Message, error) {
	checkUserErr := checkUserInChat(userID, chatID)
	if checkUserErr != nil {
		return nil, checkUserErr
	}
	rows, err := configs.DatabaseConnection.Query("SELECT message.id, message.text, message.chat_id, users.id, users.username, message.answer FROM message JOIN users ON (message.owner_id = users.id) WHERE message.chat_id = $1 ORDER BY message.id DESC LIMIT $2 OFFSET $3", chatID, limit, offset)
	if err != nil {
		log.Printf("query messages error: %s", err)
		return nil, err
	}
	defer rows.Close()
	var messagesSchemas []types.Message
	for rows.Next() {
		var m types.Message
		rows.Scan(&m.ID, &m.Text, &m.ChatId, &m.Owner.ID, &m.Owner.Username, &m.Answer)
		messagesSchemas = append(messagesSchemas, m)
	}
	if messagesSchemas != nil {
		return messagesSchemas, nil
	} else {
		return nil, errors.New("messages not found")
	}
}

func StartPrivateChatRepository(userID int, chatInfo types.PrivateChatCreate) (int, error) {
	checkUser := checkUserExist(chatInfo.RecipientID)
	if checkUser != nil {
		return 0, checkUser
	}
	tx, err := configs.DatabaseConnection.Begin()
	if err != nil {
		log.Printf("Begin tx error in start private chat: %s", err)
		return 0, errors.New("start chat error")
	}
	defer tx.Rollback()
	row := tx.QueryRow("SELECT * FROM private_chat WHERE chat_starter_id = $1 AND chat_recipient_id = $2 OR chat_recipient_id = $3 AND chat_starter_id = $4", userID, chatInfo.RecipientID, userID, chatInfo.RecipientID)
	var checkChat types.CheckPrivateChat
	row.Scan(&checkChat.ID, &checkChat.ChatStarter, &checkChat.ChatRecipient)
	if reflect.ValueOf(checkChat).IsZero() == true {
		row := tx.QueryRow("INSERT INTO private_chat (chat_starter_id, chat_recipient_id) VALUES ($1, $2) RETURNING id", userID, chatInfo.RecipientID)
		var chatID int
		err := row.Scan(&chatID)
		if err != nil {
			return 0, err
		}
		_, err = tx.Exec("INSERT INTO message (text, owner_id, chat_id) VALUES ($1, $2, $3)", chatInfo.Text, userID, chatID)
		if err != nil {
			return 0, err
		}
		err = tx.Commit()
		if err != nil {
			return 0, err
		}
		return chatID, nil
	}
	return 0, errors.New("current user already have chat with this recipient")
}
