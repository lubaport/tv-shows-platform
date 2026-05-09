import pytest
from fastapi.testclient import TestClient
import os
import tempfile
import shutil
from main import app
import database as db_module


@pytest.fixture
def test_db():
    """Create a fresh test database for each test"""
    test_dir = tempfile.mkdtemp()
    test_db_path = os.path.join(test_dir, 'test.db')

    # Monkey-patch the DB_PATH
    original_db_path = db_module.DB_PATH
    db_module.DB_PATH = test_db_path

    yield test_db_path

    # Cleanup
    db_module.DB_PATH = original_db_path
    shutil.rmtree(test_dir, ignore_errors=True)


@pytest.fixture
def client(test_db):
    """FastAPI test client with isolated database"""
    return TestClient(app)


@pytest.mark.asyncio
async def test_add_follow(test_db):
    """Test adding a followed show"""
    from database import init_db, add_follow, get_follows

    await init_db()
    await add_follow(
        tvmaze_id=1396,
        show_name="Breaking Bad",
        season=5,
        number=16,
        episode_name="Felina",
        air_date="2013-09-29"
    )

    follows = await get_follows()
    assert len(follows) == 1
    assert follows[0]['show_name'] == "Breaking Bad"
    assert follows[0]['tvmaze_id'] == 1396


@pytest.mark.asyncio
async def test_delete_follow(test_db):
    """Test deleting a followed show"""
    from database import init_db, add_follow, get_follows, delete_follow

    await init_db()
    await add_follow(1, "Test Show", 1, 1, "Episode 1", "2024-01-01")

    follows = await get_follows()
    assert len(follows) == 1

    await delete_follow(follows[0]['id'])

    follows = await get_follows()
    assert len(follows) == 0


def test_search_endpoint(client):
    """Test the search endpoint returns valid data"""
    response = client.get("/api/shows/search?q=breaking")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    # Check structure
    for show in data:
        assert 'id' in show
        assert 'name' in show
        assert 'year' in show


def test_search_no_results(client):
    """Test search with no results"""
    response = client.get("/api/shows/search?q=xyzabc123notarealshow")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_next_episode_endpoint():
    """Test the next episode endpoint with a known show"""
    from httpx import AsyncClient

    async with AsyncClient(app=app, base_url="http://test") as client:
        # Test with Breaking Bad (TVMaze ID: 1396)
        response = await client.get("/api/shows/1396/next-episode")
        # Breaking Bad has ended, so should return last episode or 404
        assert response.status_code in [200, 404]

        if response.status_code == 200:
            data = response.json()
            assert 'season' in data
            assert 'number' in data
            assert 'name' in data
            assert 'airdate' in data


@pytest.mark.asyncio
async def test_full_workflow(test_db):
    """Test complete add/get/delete workflow"""
    from database import init_db, add_follow, get_follows, delete_follow

    await init_db()

    # Empty at start
    follows = await get_follows()
    assert len(follows) == 0

    # Add multiple shows
    await add_follow(1, "Show A", 1, 1, "Ep1", "2024-01-01")
    await add_follow(2, "Show B", 2, 5, "Ep5", "2024-01-05")

    follows = await get_follows()
    assert len(follows) == 2

    # Verify order (by air_date)
    assert follows[0]['show_name'] == "Show A"
    assert follows[1]['show_name'] == "Show B"

    # Delete first show
    await delete_follow(follows[0]['id'])

    follows = await get_follows()
    assert len(follows) == 1
    assert follows[0]['show_name'] == "Show B"
