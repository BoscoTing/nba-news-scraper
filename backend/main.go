package main

import (
	"github.com/gin-gonic/gin"

	"OneAI-mini-project/backend/config"
	"OneAI-mini-project/backend/routes"
)

func main() {
	gin.SetMode(gin.ReleaseMode)

	router := gin.Default()
	router.LoadHTMLGlob("asset/*.html")
	router.Static("/asset", "asset")
	config.Connect()
	routes.StoryRoute(router)
	router.Run(":8080")
}
