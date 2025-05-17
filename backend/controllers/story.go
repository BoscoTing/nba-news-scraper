package controllers

import (
	"OneAI-mini-project/backend/config"
	"OneAI-mini-project/backend/models"
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

func getPage(c *gin.Context) int {
	pageStr := c.Param("page")
	page := 1
	if pageStr != "" {
		if p, err := strconv.Atoi(pageStr); err == nil && p > 0 {
			page = p
		}
	}
	return page
}

func getOffset(page int) int {
	return (page - 1) * 10
}

func GetStoryList(c *gin.Context) {
	page := getPage(c)
	offset := getOffset(page)
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
