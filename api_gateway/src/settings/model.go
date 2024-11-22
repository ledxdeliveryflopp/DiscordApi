package settings

import (
	"time"
)

type Token struct {
	Id     int       `gorm:"primarykey"`
	Token  string    `json:"token"`
	Expire time.Time `json:"expire"`
}
