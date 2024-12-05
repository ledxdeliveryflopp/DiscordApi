package chat

// Users Структура пользователя
type Users struct {
	ID       int    `json:"ID" db:"id"`
	Username string `json:"Username" db:"username"`
}

// PrivateChat Структура личного чата
type PrivateChat struct {
	ID            int   `json:"ID" db:"id"`
	ChatStarter   Users `json:"ChatStarter"`
	ChatRecipient Users `json:"ChatRecipient"`
}

// Message Структура сообщения
type Message struct {
	ID     int    `json:"ID" db:"id"`
	Text   string `json:"Text" validate:"required" db:"text"`
	ChatId int    `json:"chat_id" validate:"required" db:"chat_id"`
	Owner  Users  `json:"User"`
	//OwnerId int `json:"OwnerId" db:"owner_id"`
}

type MessageCreate struct {
	Text string `json:"Text" validate:"required,gte=0,lte=2000" db:"text"`
}
