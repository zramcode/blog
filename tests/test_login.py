import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.asyncio
async def test_login():    
   async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
     token_response = await ac.post("/login", data={"username": "mostafa", "password": "mostafa"})
    
     assert token_response.status_code == 200
     token = token_response.json().get("access_token")
     assert token is not None
    
     headers = {"Authorization": f"Bearer {token}"}
     post_data = {
            "title": "E2E Test Post",
            "content": "This is a test post created during E2E testing.",
            "slug" : "E2E"
        }
     create_post_response = await ac.post("/posts/", json=post_data, headers=headers)
     assert create_post_response.status_code == 200
     assert create_post_response.json()["title"] == "E2E Test Post"
