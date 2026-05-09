from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
import os
import sys
from pydantic import BaseModel

sys.path.insert(0, os.path.dirname(__file__))

from database import init_db, add_follow, get_follows, delete_follow
from tvmaze import search_shows, get_next_episode
import httpx

app = FastAPI()


@app.on_event('startup')
async def startup():
    await init_db()


class ShowData(BaseModel):
    tvmaze_id: int
    show_name: str
    season: int
    number: int
    episode_name: str
    air_date: str


@app.get('/api/shows/search')
async def search(q: str):
    if not q or len(q) < 2:
        return []
    results = await search_shows(q)
    return results


@app.get('/api/shows/{show_id}/next-episode')
async def get_episode(show_id: int):
    episode = await get_next_episode(show_id)
    if not episode:
        raise HTTPException(status_code=404, detail='No episode data found')
    return episode


@app.get('/api/follows')
async def list_follows():
    return await get_follows()


@app.post('/api/follows')
async def create_follow(data: ShowData):
    await add_follow(
        data.tvmaze_id,
        data.show_name,
        data.season,
        data.number,
        data.episode_name,
        data.air_date
    )
    return {'status': 'ok'}


@app.delete('/api/follows/{follow_id}')
async def remove_follow(follow_id: int):
    await delete_follow(follow_id)
    return {'status': 'ok'}


# Serve frontend
frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')
app.mount('/', StaticFiles(directory=frontend_path, html=True), name='frontend')
