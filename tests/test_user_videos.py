import os
from datetime import datetime

import pytest

from sparta.tiktokapi.access import create_bearer_token
from sparta.tiktokapi.models.model import VideoObject
from sparta.tiktokapi.users.videos import query_user_pinned_videos

# from sparta.tiktokapi.users.videos import query_user_liked_videos, query_user_pinned_videos, query_user_reposted_videos

client_key = os.getenv("CLIENT_KEY", "")
client_secret = os.getenv("CLIENT_SECRET", "")
bearer_token = create_bearer_token(client_key, client_secret)
start_time = datetime(2024, 1, 1)


@pytest.mark.asyncio
async def test_query_user_pinned_videos() -> None:
    username = "dfb"
    async for video in query_user_pinned_videos(bearer_token, username, start_time):
        assert isinstance(video, VideoObject)
        break


# Looking for a user with liked and reposted videos
# @pytest.mark.asyncio
# async def test_query_user_liked_videos() -> None:
#     username = "dfb"
#     async for video in query_user_liked_videos(bearer_token, username, start_time):
#         assert isinstance(video, VideoObject)
#         break


# @pytest.mark.asyncio
# async def test_query_user_reposted_videos() -> None:
#     username = "dfb"
#     async for video in query_user_reposted_videos(bearer_token, username, start_time):
#         assert isinstance(video, VideoObject)
#         break
