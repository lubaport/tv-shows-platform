import httpx
from datetime import datetime

TVMAZE_API = 'https://api.tvmaze.com'


async def search_shows(query: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{TVMAZE_API}/search/shows', params={'q': query})
        if response.status_code != 200:
            return []

        results = response.json()
        return [
            {
                'id': result['show']['id'],
                'name': result['show']['name'],
                'year': result['show']['premiered'][:4] if result['show'].get('premiered') else 'N/A'
            }
            for result in results[:10]
        ]


async def get_next_episode(show_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'{TVMAZE_API}/shows/{show_id}/nextepisode')

        if response.status_code == 200:
            episode = response.json()
            return {
                'season': episode['season'],
                'number': episode['number'],
                'name': episode['name'],
                'airdate': episode['airdate']
            }

        # Fallback: get all episodes and filter
        response = await client.get(f'{TVMAZE_API}/shows/{show_id}/episodes')
        if response.status_code != 200:
            return None

        episodes = response.json()
        today = datetime.now().date()

        # Try to find upcoming episode first
        upcoming = [
            ep for ep in episodes
            if ep.get('airdate') and datetime.strptime(ep['airdate'], '%Y-%m-%d').date() > today
        ]

        if upcoming:
            ep = upcoming[0]
            return {
                'season': ep['season'],
                'number': ep['number'],
                'name': ep['name'],
                'airdate': ep['airdate']
            }

        # Fallback to last aired episode
        aired = [
            ep for ep in episodes
            if ep.get('airdate') and datetime.strptime(ep['airdate'], '%Y-%m-%d').date() <= today
        ]

        if aired:
            ep = aired[-1]
            return {
                'season': ep['season'],
                'number': ep['number'],
                'name': ep['name'],
                'airdate': ep['airdate']
            }

        return None
