# Clipboard Share

A simple web app for sharing clipboard content across devices on a local network. No authentication required - just paste and share.

## Features

- View all shared clipboard entries
- Add new text snippets
- Delete snippets
- Auto-refresh every 10 seconds
- Clean, minimal UI
- Persistent SQLite storage

## Quick Start

### Docker Compose

```bash
docker compose up -d --build
```

The app will be available at `http://localhost:80`.

### Development

Run the backend locally:

```bash
pip install -r requirements.txt
DB_PATH=./clipboard.db python main.py
```

The API will be available at `http://localhost:3000`.

## Architecture

- **Backend**: FastAPI (Python) serving a REST API on port 3000
- **Frontend**: Vanilla HTML/CSS/JS served by Nginx on port 80
- **Storage**: SQLite database persisted via Docker volume

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/snippets` | List all snippets |
| POST | `/api/snippets` | Create a new snippet |
| DELETE | `/api/snippets/{id}` | Delete a snippet |

## Deployment

### Portainer

Use the included `docker-compose.yml` as a Portainer stack. The stack creates:

- `backend` service - FastAPI API server
- `frontend` service - Nginx serving the UI
- `clipboard-data` volume - persistent SQLite storage

### GitHub Container Registry

Images are automatically built and pushed to GHCR on every push to `main`:

- Backend: `ghcr.io/<owner>/clipboard-share/backend`
- Frontend: `ghcr.io/<owner>/clipboard-share/frontend`

## License

MIT
