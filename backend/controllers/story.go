package controllers

import (
	"OneAI-mini-project/backend/config"
	"OneAI-mini-project/backend/models"
	"strconv"

	"github.com/gin-gonic/gin"
)

func GetStoryList(c *gin.Context) {
	pageStr := c.Param("page")
	page := 1
	if pageStr != "" {
		if p, err := strconv.Atoi(pageStr); err == nil && p > 0 {
			page = p
		}
	}
	offset := (page - 1) * 10

	storyList := []models.StoryListPublic{}

	config.DB.Model(&models.Story{}).Limit(10).Offset(offset).Find(&storyList)
	c.JSON(200, storyList)
}

func GetStoryDetail(c *gin.Context) {
	id := c.Param("id")
	storyDetail := models.StoryDetailPublic{}
	config.DB.First(&models.Story{}, id).Find(&storyDetail)
	c.JSON(200, storyDetail)
}
