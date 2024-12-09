package chat

// Users Структура пользователя
type Users struct {
	ID        int    `json:"ID" db:"id"`
	Username  string `json:"Username" db:"username"`
	AvatarUrl string `json:"AvatarUrl" db:"avatar_url"`
}

// PrivateChat Структура личного чата
type PrivateChat struct {
	ID            int   `json:"ID" db:"id"`
	ChatStarter   Users `json:"ChatStarter"`
	ChatRecipient Users `json:"ChatRecipient"`
}

// CheckPrivateChat Структура для проверки наличия юзера в чате
type CheckPrivateChat struct {
	ID            int
	ChatStarter   int
	ChatRecipient int
}

// Message Структура сообщения
type Message struct {
	ID     int    `json:"ID" db:"id"`
	Text   string `json:"Text" validate:"required" db:"text"`
	ChatId int    `json:"chat_id" validate:"required" db:"chat_id"`
	Owner  Users  `json:"User"`
}

type MessageCreate struct {
	Text string `json:"Text" validate:"required,gte=0,lte=2000" db:"text"`
}

type PrivateChatCreate struct {
	RecipientID int    `json:"recipient_id" validate:"required"`
	Text        string `json:"text" validate:"lte=2000"`
}
