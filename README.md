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
docker compose up -d
```

The app will be available at `http://localhost:80`.

### Development

Run locally:

```bash
pip install -r requirements.txt
DB_PATH=./clipboard.db python main.py
```

The app will be available at `http://localhost:80`.

## Architecture

- **Backend**: FastAPI (Python) serving both the REST API and the static frontend on port 80
- **Frontend**: Vanilla HTML/CSS/JS served as static files by FastAPI
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

- `app` service - FastAPI server (API + frontend)
- `clipboard-data` volume - persistent SQLite storage

### GitHub Container Registry

The image is automatically built and pushed to GHCR on every push to `main`:

- `ghcr.io/<owner>/clipboard-share`

## License

MIT
