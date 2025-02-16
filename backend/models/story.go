package models

import (
	"time"

	"gorm.io/gorm"
)

type StoryListPublic struct {
	Id        int       `json:"id"`
	Title     string    `json:"title"`
	PublishAt time.Time `json:"publish_at"`
}

type StoryDetailPublic struct {
	Id        int       `json:"id"`
	Title     string    `json:"title"`
	Content   string    `json:"content"`
	PublishAt time.Time `json:"publish_at"`
	Url       string    `json:"url"`
}

type Story struct {
	gorm.Model
	Id        int       `gorm:"column:id"`
	Title     string    `gorm:"column:title"`
	Content   string    `gorm:"column:content"`
	Url       string    `gorm:"column:url"`
	PublishAt time.Time `gorm:"column:publish_at"`
	CreateAt  time.Time `gorm:"column:create_at"`
}

func (Story) TableName() string {
	return "story"
}
