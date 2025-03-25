package main

import (
	log "github.com/sirupsen/logrus"
	"private_messages_microservice/internal/app"
)

func main() {
	log.Println("Starting api in 6000 port")
	app.StartApi(":6000")
}
