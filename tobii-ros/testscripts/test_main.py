import pytest 
from httpx import AsyncClient
from main import app 
from fastapi.testclient import TestClient

@pytest.mark.asyncio
async def test_websocket():
    client = TestClient(app)
    with client.websocket_connect("/datapoints") as websocket: 
        data = websocket.receive_json()
        assert data == {"msg": "Hello WebSocket"}
