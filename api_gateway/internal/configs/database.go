package configs

import (
	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"
	log "github.com/sirupsen/logrus"
)

var DatabaseConnection *sqlx.DB

// ConnectToBd Подключение к бд
func ConnectToBd() {
	db, err := sqlx.Open("postgres", Settings.database.url)
	if err != nil {
		log.Error(err)
	}
	DatabaseConnection = db
	return
}
