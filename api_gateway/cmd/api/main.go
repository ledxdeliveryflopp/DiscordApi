package main

import (
	"api_gateway/internal/app"
	log "github.com/sirupsen/logrus"
)

func main() {
	log.Println("Starting api in 9000 port")
	app.StartApi(":9000")
}
