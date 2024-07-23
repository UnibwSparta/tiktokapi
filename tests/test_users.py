import os

import pytest

from sparta.tiktokapi.access import create_bearer_token
from sparta.tiktokapi.models.model import UserFollowerInfoObject, UserInfoObject
from sparta.tiktokapi.users.user import query_user_followers, query_user_following, query_user_info

client_key = os.getenv("CLIENT_KEY", "")
client_secret = os.getenv("CLIENT_SECRET", "")

bearer_token = create_bearer_token(client_key, client_secret)
username = "tiktok"


@pytest.mark.asyncio
async def test_query_user_info() -> None:
    user = await query_user_info(bearer_token, username)
    assert isinstance(user, UserInfoObject)


@pytest.mark.asyncio
async def test_query_user_followers() -> None:
    async for user in query_user_followers(bearer_token, username):
        assert isinstance(user, UserFollowerInfoObject)
        break


@pytest.mark.asyncio
async def test_query_user_following() -> None:
    async for user in query_user_following(bearer_token, username):
        assert isinstance(user, UserFollowerInfoObject)
        break
