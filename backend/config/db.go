package config

import (
	"OneAI-mini-project/backend/models"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

var DB *gorm.DB

func Connect() {
	db, err := gorm.Open(
		postgres.Open("postgres://orca:orca@localhost:5432/postgres"),
		&gorm.Config{},
	)
	if err != nil {
		panic(err)
	}
	db.AutoMigrate(&models.Story{})
	DB = db
}
