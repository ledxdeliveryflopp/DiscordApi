package configs

import (
	"fmt"
	log "github.com/sirupsen/logrus"
	"io"
	"os"
)

func InitLogrus() {
	file, err := os.OpenFile("api.log", os.O_CREATE|os.O_WRONLY, 0666)
	if err != nil {
		fmt.Println("Cant create log file:", err)
		log.SetOutput(os.Stdout)
		log.Println("Using standard stdout for logging")
		return
	}
	mw := io.MultiWriter(os.Stdout, file)
	log.SetOutput(mw)
	log.Info("Logrus init in file and stdout")
}
