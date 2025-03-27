package configs

import (
	"fmt"
	log "github.com/sirupsen/logrus"
)

type JwtTokenSettings struct {
	secretKey string
}

type DatabaseSettings struct {
	url string
}

type BaseSettings struct {
	database DatabaseSettings
	token    JwtTokenSettings
}

var Settings *BaseSettings

func (s *BaseSettings) Init(host string, port string, user string, password string, name string, jwtSecret string) {
	s.database.url = fmt.Sprintf("host=%s user=%s port=%s password=%s dbname=%s sslmode=disable\n",
		host, user, port, password, name)
	s.token.secretKey = jwtSecret
}

func InitSettings(host string, port string, user string, password string, name string, jwtSecret string) {
	var s BaseSettings
	s.Init(host, port, user, password, name, jwtSecret)
	Settings = &s
	log.Infof("Settings database url: %s", Settings.database.url)
	log.Infof("Settings jwt token secret: %s", Settings.token.secretKey)
	return
}
