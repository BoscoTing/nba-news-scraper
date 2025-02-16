package routes

import (
	"OneAI-mini-project/backend/controllers"

	"github.com/gin-gonic/gin"
)

func StoryRoute(router *gin.Engine) {
	router.GET("/index/", func(c *gin.Context) {
		c.Redirect(301, "/index/1")
	})
	router.GET("/index/:page", controllers.GetStoryList)
	router.GET("/story/:id", controllers.GetStoryDetail)
}
