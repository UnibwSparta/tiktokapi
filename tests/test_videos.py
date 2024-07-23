import os
from datetime import date

import pytest

from sparta.tiktokapi.access import create_bearer_token
from sparta.tiktokapi.models.model import CommentObject, VideoObject
from sparta.tiktokapi.videos.videos import query_video_comments, query_videos

client_key = os.getenv("CLIENT_KEY", "")
client_secret = os.getenv("CLIENT_SECRET", "")
bearer_token = create_bearer_token(client_key, client_secret)


@pytest.mark.asyncio
async def test_query_videos() -> None:
    query = {
        "and": [
            {"operation": "IN", "field_name": "region_code", "field_values": ["JP", "US"]},
            {"operation": "EQ", "field_name": "keyword", "field_values": ["animal"]},
        ]
    }
    start_date = date(2024, 2, 1)
    end_date = date(2024, 2, 5)

    async for video in query_videos(bearer_token, query, start_date, end_date, max_count=10):
        assert isinstance(video, VideoObject)
        break


@pytest.mark.asyncio
async def test_query_video_comments() -> None:
    video_id = 7388519845278567712
    async for comment in query_video_comments(bearer_token, video_id):
        assert isinstance(comment, CommentObject)
        break
