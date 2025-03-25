package types

// Message Структура сообщения
type Message struct {
	ID     int    `json:"id" db:"id"`
	Text   string `json:"text"`
	Answer int    `json:"message_answer_id"`
	ChatId int    `json:"chat_id"`
	Owner  Users  `json:"message_owner"`
}

type MessageCreate struct {
	Text   string `json:"text" validate:"required,gte=0,lte=2000" db:"text"`
	Answer int    `json:"message_answer_id"`
}
