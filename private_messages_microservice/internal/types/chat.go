package types

// PrivateChat Структура личного чата
type PrivateChat struct {
	ID            int   `json:"id" db:"id"`
	ChatStarter   Users `json:"chat_starter"`
	ChatRecipient Users `json:"chat_recipient"`
}

// UserChatList структура списка чатов пользователя
type UserChatList struct {
	ID int `json:"id" db:"id"`
}

type PrivateChatCreate struct {
	RecipientID int    `json:"recipient_id" validate:"required"`
	Text        string `json:"text" validate:"lte=2000"`
}
