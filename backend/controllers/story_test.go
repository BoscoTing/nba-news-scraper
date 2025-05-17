package controllers

import (
	"net/http/httptest"
	"testing"

	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
)

func TestGetPage(t *testing.T) {
	tests := []struct {
		name     string
		pageStr  string
		expected int
	}{
		{
			name:     "Valid page number",
			pageStr:  "2",
			expected: 2,
		},
		{
			name:     "Empty page string",
			pageStr:  "",
			expected: 1,
		},
		{
			name:     "Invalid page number",
			pageStr:  "abc",
			expected: 1,
		},
		{
			name:     "Zero page number",
			pageStr:  "0",
			expected: 1,
		},
		{
			name:     "Negative page number",
			pageStr:  "-1",
			expected: 1,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			// Create a new Gin context
			w := httptest.NewRecorder()
			c, _ := gin.CreateTestContext(w)

			// Set up the page parameter
			c.Params = []gin.Param{{Key: "page", Value: tt.pageStr}}

			// Call the function
			result := getPage(c)

			// Assert the result
			assert.Equal(t, tt.expected, result)
		})
	}
}

func TestGetOffset(t *testing.T) {
	tests := []struct {
		name     string
		page     int
		expected int
	}{
		{
			name:     "First page",
			page:     1,
			expected: 0,
		},
		{
			name:     "Second page",
			page:     2,
			expected: 10,
		},
		{
			name:     "Third page",
			page:     3,
			expected: 20,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := getOffset(tt.page)
			assert.Equal(t, tt.expected, result)
		})
	}
}
