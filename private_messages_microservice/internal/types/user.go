package types

// Users Структура пользователя
type Users struct {
	ID        int    `json:"id"`
	Username  string `json:"username"`
	AvatarUrl string `json:"avatar_url"`
}

// CheckPrivateChat Структура для проверки наличия юзера в чате
type CheckPrivateChat struct {
	ID            int
	ChatStarter   int
	ChatRecipient int
}
