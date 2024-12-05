package chat

import (
	"chat_microservice/settings"
	"errors"
	"fmt"
	_ "github.com/lib/pq"
)

func getInfoAboutPrivateChat(chatID int, userID int, chat chan PrivateChat, chatError chan error) {
	db := settings.ConnectToBd()
	queryStr := fmt.Sprintf("SELECT chat.id, starter.id, starter.username, recipient.id, recipient.username FROM private_chat chat JOIN users starter ON (chat.chat_starter_id = starter.id) JOIN users recipient ON (chat.chat_recipient_id = recipient.id) where chat.id = %d", chatID)
	row, err := db.Query(queryStr)
	if err != nil {
		chatError <- err
	}
	defer row.Close()
	var chatSchemas PrivateChat
	for row.Next() {
		err := row.Scan(&chatSchemas.ID, &chatSchemas.ChatStarter.ID, &chatSchemas.ChatStarter.Username,
			&chatSchemas.ChatRecipient.ID, &chatSchemas.ChatRecipient.Username)
		if err != nil {
			chatError <- err
		}
	}
	chatSchemasCheck := PrivateChat{}
	switch {
	case chatSchemas == chatSchemasCheck:
		chatError <- errors.New("chat not found")
	case userID == chatSchemas.ChatRecipient.ID || userID == chatSchemas.ChatStarter.ID:
		chat <- chatSchemas
	case userID != chatSchemas.ChatRecipient.ID || userID != chatSchemas.ChatStarter.ID:
		chatError <- errors.New("current user not in this chat")
	}
}

func addMessageInChatRepository(chatID int, userID int, message MessageCreate, success chan int, messageErr chan error) {
	db := settings.ConnectToBd()
	queryStr := fmt.Sprintf("INSERT INTO message (text, owner_id, chat_id) VALUES ('%s', %d, %d)", message.Text, userID, chatID)
	_, err := db.Query(queryStr)
	if err != nil {
		messageErr <- err
	}
	success <- 0
}

func getLastMessageFromChatRepository(chatID int, limit int, offset int, messages chan []Message, messagesErr chan error) {
	db := settings.ConnectToBd()
	queryStr := fmt.Sprintf("SELECT m.id, m.text, m.chat_id, u.id, u.username FROM message m JOIN users u ON (m.owner_id = u.id) WHERE m.chat_id = %d ORDER BY m.id DESC LIMIT %d OFFSET %d", chatID, limit, offset)
	rows, err := db.Query(queryStr)
	if err != nil {
		messagesErr <- err
	}
	defer rows.Close()
	var messagesSchemas []Message
	for rows.Next() {
		var m Message
		err := rows.Scan(&m.ID, &m.Text, &m.ChatId, &m.Owner.ID, &m.Owner.Username)
		if err != nil {
			messagesErr <- err
		}
		messagesSchemas = append(messagesSchemas, m)
	}
	if messagesSchemas != nil {
		messages <- messagesSchemas
	} else {
		messagesErr <- errors.New("empty messages list, maybe bad chat id")
	}
}
