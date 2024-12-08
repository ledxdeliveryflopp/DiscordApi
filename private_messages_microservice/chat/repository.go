package chat

import (
	"chat_microservice/settings"
	"errors"
	"fmt"
	_ "github.com/lib/pq"
	"log"
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

func checkUserInChat(userID int, chatID int) (bool, error) {
	db := settings.ConnectToBd()
	queryStr := fmt.Sprintf("SELECT * FROM private_chat WHERE id = %d", chatID)
	row, err := db.Query(queryStr)
	if err != nil {
		return false, err
	}
	defer row.Close()
	var checkPrivateChat CheckPrivateChat
	for row.Next() {
		err := row.Scan(&checkPrivateChat.ID, &checkPrivateChat.ChatStarter, &checkPrivateChat.ChatRecipient)
		if err != nil {
			return false, err
		}
	}
	log.Println("chat starter", checkPrivateChat.ChatStarter)
	log.Println("chat recipient ", checkPrivateChat.ChatRecipient)
	log.Println("user id ", userID)
	if checkPrivateChat.ChatStarter == userID || checkPrivateChat.ChatRecipient == userID {
		return true, nil
	} else {
		return false, nil
	}
}

func getLastMessageFromChatRepository(chatID int, userID int, limit int, offset int, messages chan []Message, messagesErr chan error) {
	checkUser, err := checkUserInChat(userID, chatID)
	if err != nil {
		messagesErr <- err
	}
	if checkUser == true {
		db := settings.ConnectToBd()
		queryStr := fmt.Sprintf("SELECT message.id, message.text, message.chat_id, users.id, users.username FROM message JOIN users ON (message.owner_id = users.id) WHERE message.chat_id = %d ORDER BY message.id DESC LIMIT %d OFFSET %d", chatID, limit, offset)
		rows, err := db.Query(queryStr)
		if err != nil {
			messagesErr <- err
		}
		defer rows.Close()
		var messagesSchemas []Message
		for rows.Next() {
			var m Message
			err := rows.Scan(&m.ID, &m.Text, &m.ChatId, &m.Owner.ID, &m.Owner.Username)
			log.Println("err rows", err)
			if err != nil {
				messagesErr <- err
			}
			log.Println("Message", m)
			messagesSchemas = append(messagesSchemas, m)
		}
		log.Print(messagesSchemas)
		if messagesSchemas != nil {
			messages <- messagesSchemas
		} else {
			log.Println("Db rows", rows)
			messagesErr <- errors.New("empty messages list, maybe bad chat id")
		}
	} else if checkUser == false {
		messagesErr <- errors.New("current user is not in this chat")
	}
}
