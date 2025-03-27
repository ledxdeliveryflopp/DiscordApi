package app

import (
	"api_gateway/internal/configs"
	"api_gateway/internal/transport"
	log "github.com/sirupsen/logrus"
	"net/http"
)

func StartApi(port string) {
	configs.InitSettings("token_database", "5432", "postgres", "admin", "token",
		"1ca26a466e6327dfd6e51599fd2892e59ba1a2885ab3d9b09f48baaa3ca2251c")
	configs.ConnectToBd()
	mainRouter := transport.SetRouters()
	err := http.ListenAndServe(port, mainRouter)
	if err != nil {
		log.Errorf("Error while starting api: %s", err)
		return
	}
}
