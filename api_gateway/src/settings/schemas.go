package settings

import "time"

type TokenApi struct {
	Token  string    `json:"token"`
	Expire time.Time `json:"expire"`
}
