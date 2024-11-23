package settings

import (
	"fmt"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"time"
)

func GetDb() *gorm.DB {
	// Подключится к бд
	database, err := gorm.Open(postgres.Open(GetDatabaseUrl()), &gorm.Config{})
	if err != nil {
		fmt.Println("Database connect error", err)
	}
	connections, connectionErr := database.DB()
	if connectionErr != nil {
		fmt.Println("Database connection error", err)
	}
	connections.SetMaxIdleConns(10)
	connections.SetMaxOpenConns(100)
	connections.SetConnMaxLifetime(time.Hour)
	return database
}
