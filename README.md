# 📺 TV Shows Manager

A modern web application to track your favorite TV shows and manage upcoming episodes.

## Features

- **Search & Add Shows** - Search for TV shows using the TVMaze API with autocomplete suggestions
- **Episode Tracking** - Automatically fetches and displays the next upcoming episode for each show
- **Smart Fallback** - Shows the last aired episode if no upcoming episodes are scheduled
- **Followed Shows List** - Keep track of all shows you're currently following
- **Responsive Design** - Works seamlessly on desktop and mobile devices
- **Real-time Autocomplete** - Get show suggestions as you type with year information

## How to Use

1. **Add a Show**
   - Type the show name in the search box
   - Select from the autocomplete suggestions that appear
   - Click "Search & Add" to add it to your list

2. **View Episodes**
   - Your followed shows appear in the main panel sorted by air date
   - Each show displays:
     - Show name
     - Episode name
     - Season and episode number
     - Air date
   - Remove shows using the "Remove Show" button

3. **Follow Shows**
   - All added shows appear in the "Following" list on the left
   - Click "Unfollow" to remove a show from your list

## Technologies

- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **API**: [TVMaze API](https://www.tvmaze.com/api)
- **Styling**: CSS Grid and Flexbox for responsive layout

## Getting Started

1. Clone the repository
2. Open `index.html` in your web browser
3. Start adding your favorite shows!

No installation or build process required - it's a pure frontend application.

## API Reference

This app uses the TVMaze API which is free and doesn't require authentication:
- Search shows: `GET /search/shows?q={query}`
- Get next episode: `GET /shows/{id}/nextepisode`
- Get all episodes: `GET /shows/{id}/episodes`

## License

MIT
