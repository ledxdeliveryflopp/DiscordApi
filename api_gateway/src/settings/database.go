package settings

import (
	"fmt"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

func GetDb() *gorm.DB {
	// Подключится к бд
	database, err := gorm.Open(postgres.Open(GetDatabaseUrl()), &gorm.Config{})
	if err != nil {
		fmt.Println("Database connect error", err)
	}
	return database
}
