package configs

import (
	"fmt"
	log "github.com/sirupsen/logrus"
)

type DatabaseSettings struct {
	url string
}

type BaseSettings struct {
	database DatabaseSettings
}

var Settings *BaseSettings

func (s *BaseSettings) Init(host string, port string, user string, password string, name string) {
	s.database.url = fmt.Sprintf("host=%s user=%s port=%s password=%s dbname=%s sslmode=disable\n",
		host, user, port, password, name)
}

func InitSettings(host string, port string, user string, password string, name string) {
	var s BaseSettings
	s.Init(host, port, user, password, name)
	Settings = &s
	log.Infof("Seetings database url: %s", Settings.database.url)
	return
}
