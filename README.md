# NBA News Scraper

A web scraping and news display system that collects NBA news from UDN Sports (tw-nba.udn.com) and presents them through a clean web interface.

## Demo

https://github.com/user-attachments/assets/3273d380-45d1-4a54-8ac7-aed2702c3198

## Architecture

```mermaid
graph TB
    UDN[UDN NBA News<br/>Website] -->|Scrape| Scraper
    
    subgraph AWS[AWS EC2]
        Scraper -->|Store| DB
        API -->|Query| DB
        
        API[Go Backend API]
        subgraph Docker Container
            DB[(PostgreSQL)]
        end
        Scraper[Python Scraper]
    end

    Client[Web Browser] -->|HTTP Request| API
    API -->|JSON Response| Client
```

## Tech Stack

- **Backend**: Go (Gin Framework)
- **Database**: PostgreSQL
- **Scraper**: Python
- **Infrastructure**: Docker

## Features

- Automated web scraping of NBA news from UDN Sports
- RESTful API for news retrieval
- PostgreSQL database for data persistence
- Containerized deployment with Docker
- Environment-based configuration

## Setup Instructions

### Prerequisites

- Docker and Docker Compose
- Python 3.12+
- Go 1.21+

### Environment Setup

1. Clone the repository:

    ```bash
    git clone <repository-url>
    cd OneAI-mini-project
    ```

2. Set up environment variables:
    Create a `.env` file in the root directory, /scraper/ and /backend/ with the following content:

    ```env
    POSTGRES_DB=your_db_name
    POSTGRES_USER=your_user
    POSTGRES_PASSWORD=your_password
    POSTGRES_PORT=5432
    ```

    For the `.env` file in /scraper/, add one more variable:

    ```env
    INDEX_URL="https://tw-nba.udn.com/nba/cate/6754/0/newest"
    ```

3. Start the database:

    ```bash
    docker-compose up -d
    ```

4. Set up the scraper:

    ```bash
    cd scraper
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

5. Start the backend server:

    ```bash
    cd backend
    go mod download
    go run main.go
    ```

## API Documentation

### News Endpoints

#### Get Featured News List

```text
GET /index
```

Returns a list of featured news articles.

Response:

```json
{
  "data": [
    {
      "id": "string",
      "title": "string",
      "publish_at": "datetime"
    }
  ]
}
```

#### Get News Detail

```text
GET /story/{id}
```

Returns detailed information about a specific news article.

Response:

```json
{
  "data": {
    "id": "string",
    "title": "string",
    "content": "string",
    "url": "string",
    "publish_at": "datetime"
  }
}
```

## Project Structure

```bash
.
├── backend/           # Go backend service
├── database/         # Database related files
├── scraper/         # Python scraping service
└── docker-compose.yaml
```
