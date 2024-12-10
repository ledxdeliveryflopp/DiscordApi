package chat

import (
	"chat_microservice/settings"
	"context"
	"database/sql"
	"errors"
	"fmt"
	_ "github.com/lib/pq"
	"log"
	"reflect"
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

func checkUserInChat(userID int, chatID int, checkUserSuccess chan int, checkUserError chan error) {
	db := settings.ConnectToBd()
	queryStr := fmt.Sprintf("SELECT * FROM private_chat WHERE id = %d", chatID)
	row := db.QueryRow(queryStr)
	var checkPrivateChat CheckPrivateChat
	err := row.Scan(&checkPrivateChat.ID, &checkPrivateChat.ChatStarter, &checkPrivateChat.ChatRecipient)
	switch {
	case err == sql.ErrNoRows:
		checkUserError <- errors.New("chat not found")
	case checkPrivateChat.ChatStarter == userID || checkPrivateChat.ChatRecipient == userID:
		checkUserSuccess <- 0
	default:
		checkUserError <- errors.New("current user is not in this chat")
	}
}

func addMessageInChatRepository(ctx context.Context, chatID int, userID int, message MessageCreate, success chan int, messageErr chan error) {
	checkUserSuccess := make(chan int)
	checkUserError := make(chan error)
	go checkUserInChat(userID, chatID, checkUserSuccess, checkUserError)
	select {
	case <-checkUserSuccess:
		db := settings.ConnectToBd()
		tx, err := db.BeginTx(ctx, nil)
		if err != nil {
			log.Printf("Begin tx error in add message: %s", err)
			messageErr <- err
		}
		defer tx.Rollback()
		queryStr := fmt.Sprintf("INSERT INTO message (text, owner_id, chat_id) VALUES ('%s', %d, %d)", message.Text, userID, chatID)
		_, err = db.ExecContext(ctx, queryStr)
		if err != nil {
			log.Printf("Add message exec error: %s", err)
			messageErr <- err
		}
		success <- 0
	case err := <-checkUserError:
		messageErr <- err
	}
}

func getLastMessageFromChatRepository(chatID int, userID int, limit int, offset int, messages chan []Message, messagesErr chan error) {
	checkUserSuccess := make(chan int)
	checkUserError := make(chan error)
	go checkUserInChat(userID, chatID, checkUserSuccess, checkUserError)
	select {
	case <-checkUserSuccess:
		db := settings.ConnectToBd()
		queryStr := fmt.Sprintf("SELECT message.id, message.text, message.chat_id, users.id, users.username FROM message JOIN users ON (message.owner_id = users.id) WHERE message.chat_id = %d ORDER BY message.id DESC LIMIT %d OFFSET %d", chatID, limit, offset)
		rows, err := db.Query(queryStr)
		if err != nil {
			log.Printf("query messages error: %s", err)
			messagesErr <- err
		}
		defer rows.Close()
		var messagesSchemas []Message
		for rows.Next() {
			var m Message
			rows.Scan(&m.ID, &m.Text, &m.ChatId, &m.Owner.ID, &m.Owner.Username)
			messagesSchemas = append(messagesSchemas, m)
		}
		if messagesSchemas != nil {
			messages <- messagesSchemas
		} else {
			messagesErr <- errors.New("messages not found")
		}
	case err := <-checkUserError:
		messagesErr <- err
	}
}

func startPrivateChatRepository(ctx context.Context, userID int, chatInfo PrivateChatCreate, newChatID chan int, chatError chan error) {
	db := settings.ConnectToBd()
	tx, err := db.BeginTx(ctx, nil)
	if err != nil {
		log.Printf("Begin tx error in start private chat: %s", err)
		chatError <- errors.New("start chat error")
	}
	defer tx.Rollback()
	queryStr := fmt.Sprintf("SELECT * FROM private_chat WHERE chat_starter_id = %d AND chat_recipient_id = %d OR chat_recipient_id = %d AND chat_starter_id = %d", userID, chatInfo.RecipientID, userID, chatInfo.RecipientID)
	chatRow := tx.QueryRowContext(ctx, queryStr)
	var checkChat CheckPrivateChat
	chatRow.Scan(&checkChat.ID, &checkChat.ChatStarter, &checkChat.ChatRecipient)
	switch {
	case chatInfo.Text != "" && reflect.ValueOf(checkChat).IsZero() == true:
		queryStr = fmt.Sprintf("INSERT INTO private_chat (chat_starter_id, chat_recipient_id) VALUES (%d, %d) RETURNING id", userID, chatInfo.RecipientID)
		row := tx.QueryRowContext(ctx, queryStr)
		var chatID int
		err := row.Scan(&chatID)
		if err != nil {
			chatError <- err
		}
		queryStr = fmt.Sprintf("INSERT INTO message (text, owner_id, chat_id) VALUES ('%s', %d, %d)", chatInfo.Text, userID, chatID)
		_, err = tx.ExecContext(ctx, queryStr)
		if err != nil {
			log.Println("err", err)
			chatError <- err
		}
		err = tx.Commit()
		if err != nil {
			chatError <- err
		}
		newChatID <- chatID
	case chatInfo.Text == "" && reflect.ValueOf(checkChat).IsZero() == true:
		queryStr = fmt.Sprintf("INSERT INTO private_chat (chat_starter_id, chat_recipient_id) VALUES (%d, %d) RETURNING id", userID, chatInfo.RecipientID)
		row := tx.QueryRowContext(ctx, queryStr)
		var chatID int
		err := row.Scan(&chatID)
		if err != nil {
			chatError <- err
		}
		err = tx.Commit()
		if err != nil {
			chatError <- err
		}
		newChatID <- chatID
	default:
		chatError <- errors.New("current user already have chat with this recipient")
	}
}
