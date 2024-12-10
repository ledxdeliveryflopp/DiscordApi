package chat

// Users Структура пользователя
type Users struct {
	ID        int    `json:"id"`
	Username  string `json:"username"`
	AvatarUrl string `json:"avatar_url"`
}

// PrivateChat Структура личного чата
type PrivateChat struct {
	ID            int   `json:"id" db:"id"`
	ChatStarter   Users `json:"chat_starter"`
	ChatRecipient Users `json:"chat_recipient"`
}

// CheckPrivateChat Структура для проверки наличия юзера в чате
type CheckPrivateChat struct {
	ID            int
	ChatStarter   int
	ChatRecipient int
}

// Message Структура сообщения
type Message struct {
	ID     int    `json:"id" db:"id"`
	Text   string `json:"text"`
	Answer int    `json:"message_answer_id"`
	ChatId int    `json:"chat_id"`
	Owner  Users  `json:"message_owner"`
}

// UserChatList структура списка чатов пользователя
type UserChatList struct {
	ID int `json:"id" db:"id"`
}

type MessageCreate struct {
	Text   string `json:"text" validate:"required,gte=0,lte=2000" db:"text"`
	Answer int    `json:"message_answer_id"`
}

type PrivateChatCreate struct {
	RecipientID int    `json:"recipient_id" validate:"required"`
	Text        string `json:"text" validate:"lte=2000"`
}
