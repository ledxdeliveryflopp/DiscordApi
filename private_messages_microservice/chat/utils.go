package chat

import (
	"github.com/golang-jwt/jwt/v5"
	"log"
)

type TokenSchemas struct {
	Token string `json:"Token"`
}

var secretKey = []byte("1ca26a466e6327dfd6e51599fd2892e59ba1a2885ab3d9b09f48baaa3ca2251c")

func GetTokenPayload(headerToken string) (int, error) {
	token, err := jwt.Parse(headerToken, func(token *jwt.Token) (interface{}, error) {
		return secretKey, nil
	})
	if err != nil {
		log.Println("Jwt parse error: ", err)
		return 0, err
	}
	if claims, ok := token.Claims.(jwt.MapClaims); ok {
		userID := int(claims["user_id"].(float64))
		return userID, nil
	} else {
		return 0, err
	}
}
