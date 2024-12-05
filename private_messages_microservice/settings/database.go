package settings

import (
	"database/sql"
	"embed"
	"github.com/jmoiron/sqlx"
	_ "github.com/lib/pq"
	"github.com/rubenv/sql-migrate"
	"log"
)

func MigrateDatabase(migrationsPath embed.FS) {
	migrationsFolder := &migrate.EmbedFileSystemMigrationSource{FileSystem: migrationsPath, Root: "migrations"}

	db, err := sql.Open("postgres", GetDatabaseUrl())
	if err != nil {
		panic(err)
	}
	migration, err := migrate.Exec(db, "postgres", migrationsFolder, migrate.Up)
	if err != nil {
		panic(err)
	}
	log.Printf("Apllied %d migration.", migration)
}

func SeedFakeDataInDB(FakeMigrationsPath embed.FS) {
	migrationsFolder := &migrate.EmbedFileSystemMigrationSource{FileSystem: FakeMigrationsPath, Root: "migrations/seeder"}
	db, err := sql.Open("postgres", GetDatabaseUrl())
	if err != nil {
		panic(err)
	}
	migration, err := migrate.Exec(db, "postgres", migrationsFolder, migrate.Up)
	if err != nil {
		panic(err)
	}
	log.Printf("Apllied %d seed migration.", migration)
}

// ConnectToBd Подключение к бд
func ConnectToBd() *sqlx.DB {
	db, err := sqlx.Open("postgres", GetDatabaseUrl())
	if err != nil {
		panic(err)
	}
	return db
}
