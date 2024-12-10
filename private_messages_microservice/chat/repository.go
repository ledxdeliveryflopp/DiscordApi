package chat

import (
	"chat_microservice/settings"
	"database/sql"
	"errors"
	"fmt"
	_ "github.com/lib/pq"
	"log"
	"reflect"
)

func GetCurrentUserChat(userID int, chatList chan []UserChatList, chatListError chan error) {
	db := settings.ConnectToBd()
	queryStr := fmt.Sprintf("SELECT private_chat.id FROM private_chat JOIN users ON (private_chat.chat_starter_id = users.id OR private_chat.chat_recipient_id = users.id) WHERE users.id = %d", userID)
	rows, err := db.Query(queryStr)
	if err != nil {
		chatListError <- err
		return
	}
	var chatListSchemas []UserChatList
	for rows.Next() {
		var list UserChatList
		err := rows.Scan(&list.ID)
		if err == sql.ErrNoRows {
			chatListError <- errors.New("empty chat list")
			return
		}
		chatListSchemas = append(chatListSchemas, list)
	}
	chatList <- chatListSchemas
}

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

func checkUserInChat(userID int, chatID int) error {
	db := settings.ConnectToBd()
	queryStr := fmt.Sprintf("SELECT * FROM private_chat WHERE id = %d", chatID)
	row := db.QueryRow(queryStr)
	var checkPrivateChat CheckPrivateChat
	err := row.Scan(&checkPrivateChat.ID, &checkPrivateChat.ChatStarter, &checkPrivateChat.ChatRecipient)
	switch {
	case err == sql.ErrNoRows:
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
		db := settings.ConnectToBd()
		queryStr := fmt.Sprintf("SELECT id FROM message WHERE id = %d AND chat_id = %d", messageID, chatID)
		row := db.QueryRow(queryStr)
		var chatDbID int
		err := row.Scan(&chatDbID)
		if err == sql.ErrNoRows {
			return errors.New("answer message not found")
		}
		return nil
	default:
		return nil
	}
}

func checkUserExist(userID int) error {
	db := settings.ConnectToBd()
	queryStr := fmt.Sprintf("SELECT id FROM users WHERE id = %d", userID)
	row := db.QueryRow(queryStr)
	var userDbId int
	err := row.Scan(&userDbId)
	if err == sql.ErrNoRows {
		return errors.New("recipient user not found")
	}
	return nil
}

func addMessageInChatRepository(chatID int, userID int, message MessageCreate, success chan int, messageErr chan error) {
	checkAnswerErr := checkMessageExistForAnswer(chatID, message.Answer)
	if checkAnswerErr != nil {
		messageErr <- checkAnswerErr
		return
	}
	checkUserErr := checkUserInChat(userID, chatID)
	if checkUserErr != nil {
		messageErr <- checkUserErr
		return
	}
	db := settings.ConnectToBd()
	tx, err := db.Begin()
	if err != nil {
		log.Printf("Begin tx error in add message: %s", err)
		messageErr <- err
		return
	}
	defer tx.Rollback()
	switch {
	case reflect.ValueOf(message.Answer).IsZero() == true:
		queryStr := fmt.Sprintf("INSERT INTO message (text, owner_id, chat_id) VALUES ('%s', %d, %d)", message.Text, userID, chatID)
		_, err = tx.Exec(queryStr)
		switch {
		case err != nil:
			log.Printf("Add message exec error: %s", err)
			messageErr <- err
			return
		default:
			success <- 0
			return
		}
	default:
		queryStr := fmt.Sprintf("INSERT INTO message (text, answer, owner_id, chat_id) VALUES ('%s', %d, %d, %d)", message.Text, message.Answer, userID, chatID)
		_, err = tx.Exec(queryStr)
		switch {
		case err != nil:
			log.Printf("Add message exec error: %s", err)
			messageErr <- err
			return
		default:
			success <- 0
			return
		}
	}
}

func getLastMessageFromChatRepository(chatID int, userID int, limit int, offset int, messages chan []Message, messagesErr chan error) {
	checkUserErr := checkUserInChat(userID, chatID)
	if checkUserErr != nil {
		messagesErr <- checkUserErr
		return
	}
	db := settings.ConnectToBd()
	queryStr := fmt.Sprintf("SELECT message.id, message.text, message.chat_id, users.id, users.username, message.answer FROM message JOIN users ON (message.owner_id = users.id) WHERE message.chat_id = %d ORDER BY message.id DESC LIMIT %d OFFSET %d", chatID, limit, offset)
	rows, err := db.Query(queryStr)
	if err != nil {
		log.Printf("query messages error: %s", err)
		messagesErr <- err
		return
	}
	defer rows.Close()
	var messagesSchemas []Message
	for rows.Next() {
		var m Message
		rows.Scan(&m.ID, &m.Text, &m.ChatId, &m.Owner.ID, &m.Owner.Username, &m.Answer)
		messagesSchemas = append(messagesSchemas, m)
	}
	if messagesSchemas != nil {
		messages <- messagesSchemas
		return
	} else {
		messagesErr <- errors.New("messages not found")
		return
	}
}

func startPrivateChatRepository(userID int, chatInfo PrivateChatCreate, newChatID chan int, chatError chan error) {
	checkUser := checkUserExist(chatInfo.RecipientID)
	if checkUser != nil {
		chatError <- checkUser
		return
	}
	db := settings.ConnectToBd()
	tx, err := db.Begin()
	if err != nil {
		log.Printf("Begin tx error in start private chat: %s", err)
		chatError <- errors.New("start chat error")
		return
	}
	defer tx.Rollback()
	queryStr := fmt.Sprintf("SELECT * FROM private_chat WHERE chat_starter_id = %d AND chat_recipient_id = %d OR chat_recipient_id = %d AND chat_starter_id = %d", userID, chatInfo.RecipientID, userID, chatInfo.RecipientID)
	chatRow := tx.QueryRow(queryStr)
	var checkChat CheckPrivateChat
	chatRow.Scan(&checkChat.ID, &checkChat.ChatStarter, &checkChat.ChatRecipient)
	switch {
	case chatInfo.Text != "" && reflect.ValueOf(checkChat).IsZero() == true:
		queryStr = fmt.Sprintf("INSERT INTO private_chat (chat_starter_id, chat_recipient_id) VALUES (%d, %d) RETURNING id", userID, chatInfo.RecipientID)
		row := tx.QueryRow(queryStr)
		var chatID int
		err := row.Scan(&chatID)
		if err != nil {
			chatError <- err
			return
		}
		queryStr = fmt.Sprintf("INSERT INTO message (text, owner_id, chat_id) VALUES ('%s', %d, %d)", chatInfo.Text, userID, chatID)
		_, err = tx.Exec(queryStr)
		if err != nil {
			chatError <- err
			return
		}
		err = tx.Commit()
		if err != nil {
			chatError <- err
			return
		}
		newChatID <- chatID
	case chatInfo.Text == "" && reflect.ValueOf(checkChat).IsZero() == true:
		queryStr = fmt.Sprintf("INSERT INTO private_chat (chat_starter_id, chat_recipient_id) VALUES (%d, %d) RETURNING id", userID, chatInfo.RecipientID)
		row := tx.QueryRow(queryStr)
		var chatID int
		err := row.Scan(&chatID)
		if err != nil {
			chatError <- err
			return
		}
		err = tx.Commit()
		if err != nil {
			chatError <- err
			return
		}
		newChatID <- chatID
	default:
		chatError <- errors.New("current user already have chat with this recipient")
	}
}
