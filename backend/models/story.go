package models

import (
	"time"
)

type StoryListPublic struct {
	Id          int       `json:"id"`
	Title       string    `json:"title"`
	PublishedAt time.Time `json:"published_at"`
}

type StoryDetailPublic struct {
	Id          int       `json:"id"`
	Title       string    `json:"title"`
	Content     string    `json:"content"`
	PublishedAt time.Time `json:"published_at"`
	Url         string    `json:"url"`
}

type Story struct {
	Id          int       `gorm:"column:id"`
	Title       string    `gorm:"column:title"`
	Content     string    `gorm:"column:content"`
	Url         string    `gorm:"column:url"`
	PublishedAt time.Time `gorm:"column:published_at"`
	CreatedAt   time.Time `gorm:"column:create_at"`
}

func (Story) TableName() string {
	return "story"
}
