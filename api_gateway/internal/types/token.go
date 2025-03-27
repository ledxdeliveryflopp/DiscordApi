package types

import "time"

type JwtToken struct {
	Token  string    `json:"token"`
	Expire time.Time `json:"expire"`
}
