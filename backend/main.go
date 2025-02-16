package main

import (
	"github.com/gin-gonic/gin"

	"OneAI-mini-project/backend/config"
	"OneAI-mini-project/backend/routes"
)

func main() {
	router := gin.Default()
	config.Connect()
	routes.StoryRoute(router)
	router.Run(":8080")
}
