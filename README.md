# 📺 TV Shows Manager

A modern web application to track your favorite TV shows and manage upcoming episodes with a Python FastAPI backend and SQLite persistence.

## Architecture

```
tv-shows-platform/
├── backend/              # Python FastAPI server
│   ├── main.py          # FastAPI app with REST routes
│   ├── database.py      # SQLite setup and queries
│   ├── tvmaze.py        # TVMaze API client
│   └── requirements.txt  # Python dependencies
├── frontend/            # Static frontend served by backend
│   └── index.html       # Single-page app (vanilla JS)
└── README.md
```

## Features

- **Search & Add Shows** - Search for TV shows using autocomplete with TVMaze data
- **Episode Tracking** - Automatically fetches and displays the next upcoming episode for each show
- **Smart Fallback** - Shows the last aired episode if no upcoming episodes are scheduled
- **Persistent Storage** - Followed shows are saved to SQLite and survive page refreshes
- **Responsive Design** - Works seamlessly on desktop and mobile devices
- **Real-time Autocomplete** - Get show suggestions as you type with year information

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/lubaport/tv-shows-platform.git
cd tv-shows-platform
```

2. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Run the server:
```bash
uvicorn main:app --reload
```

4. Open your browser and go to `http://localhost:8000`

## How to Use

1. **Add a Show**
   - Type the show name in the search box
   - Select from the autocomplete suggestions that appear
   - Click "Search & Add" to add it to your list

2. **View Episodes**
   - Your followed shows appear sorted by air date
   - Each show displays:
     - Show name
     - Episode name
     - Season and episode number
     - Air date
   - Remove shows using the "Remove Show" button

3. **Data Persistence**
   - All followed shows are saved in SQLite (`backend/shows.db`)
   - Your list persists even after closing the app

## Backend API Routes

| Method | Route | Description |
|---|---|---|
| GET | `/api/shows/search?q=` | Search for shows (autocomplete) |
| GET | `/api/shows/{id}/next-episode` | Get next or last aired episode |
| GET | `/api/follows` | Get all followed shows |
| POST | `/api/follows` | Add a show to follows |
| DELETE | `/api/follows/{id}` | Remove a show from follows |

## Technologies

- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Backend**: FastAPI with Python
- **Database**: SQLite via aiosqlite
- **API Client**: httpx (async HTTP client)
- **External API**: [TVMaze API](https://www.tvmaze.com/api)

## License

MIT
