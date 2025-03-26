package configs

import (
	"database/sql"
	"embed"
	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"
	"github.com/rubenv/sql-migrate"
	log "github.com/sirupsen/logrus"
)

var DatabaseConnection *sqlx.DB

//go:embed migrations/*.sql
var dbMigrations embed.FS

func MigrateDatabase() {
	migrationsFolder := &migrate.EmbedFileSystemMigrationSource{FileSystem: dbMigrations, Root: "migrations"}

	db, err := sql.Open("postgres", Settings.database.url)
	if err != nil {
		log.Error(err)
	}
	migration, err := migrate.Exec(db, "postgres", migrationsFolder, migrate.Up)
	if err != nil {
		log.Error(err)
	}
	log.Printf("Apllied %d migration.", migration)
}

func SeedFakeDataInDB(FakeMigrationsPath embed.FS) {
	migrationsFolder := &migrate.EmbedFileSystemMigrationSource{FileSystem: FakeMigrationsPath, Root: "migrations/seeder"}
	db, err := sql.Open("postgres", Settings.database.url)
	if err != nil {
		log.Error(err)
	}
	migration, err := migrate.Exec(db, "postgres", migrationsFolder, migrate.Up)
	if err != nil {
		log.Error(err)
	}
	log.Printf("Apllied %d seed migration.", migration)
}

// ConnectToBd Подключение к бд
func ConnectToBd() {
	db, err := sqlx.Open("postgres", Settings.database.url)
	if err != nil {
		log.Error(err)
	}
	DatabaseConnection = db
	return
}
