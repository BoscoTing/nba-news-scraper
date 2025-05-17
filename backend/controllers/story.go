package controllers

import (
	"OneAI-mini-project/backend/config"
	"OneAI-mini-project/backend/models"
	"net/http"
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

	config.DB.Model(&models.Story{}).Order("published_at DESC").Limit(10).Offset(offset).Find(&storyList)
	c.HTML(http.StatusOK, "index.html", gin.H{
		"storyList": storyList,
	})
}

func GetStoryDetail(c *gin.Context) {
	id := c.Param("id")
	storyDetail := models.StoryDetailPublic{}
	config.DB.First(&models.Story{}, id).Find(&storyDetail)
	c.HTML(http.StatusOK, "story.html", gin.H{
		"storyDetail": storyDetail,
	})
}
