#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""tiktok_api_implementation.py: Implementation of TikTok API functions for retrieving user videos.

This module contains functions to interact with the TikTok API for retrieving liked, pinned, and reposted videos by a user.
It includes asynchronous implementations to handle API requests efficiently and manage rate limiting.

Examples:
    Retrieve liked videos of a user::

        from datetime import datetime
        from sparta.tiktokapi.access import create_bearer_token
        from sparta.tiktokapi.users.videos import query_user_liked_videos

        client_key = "your_client_key"
        client_secret = "your_client_secret"
        bearer_token = create_bearer_token(client_key, client_secret)
        username = "example_user"
        start_time = datetime(2023, 1, 1)

        async for video in query_user_liked_videos(bearer_token, username, start_time):
            print(video)

    Retrieve pinned videos of a user::

        from datetime import datetime
        from sparta.tiktokapi.access import create_bearer_token
        from sparta.tiktokapi.users.videos import query_user_pinned_videos

        client_key = "your_client_key"
        client_secret = "your_client_secret"
        bearer_token = create_bearer_token(client_key, client_secret)
        username = "example_user"
        start_time = datetime(2023, 1, 1)

        async for video in query_user_pinned_videos(bearer_token, username, start_time):
            print(video)

    Retrieve reposted videos of a user::

        from datetime import datetime
        from sparta.tiktokapi.access import create_bearer_token
        from sparta.tiktokapi.users.videos import query_user_reposted_videos

        client_key = "your_client_key"
        client_secret = "your_client_secret"
        bearer_token = create_bearer_token(client_key, client_secret)
        username = "example_user"
        start_time = datetime(2023, 1, 1)

        async for video in query_user_reposted_videos(bearer_token, username, start_time):
            print(video)
"""
import asyncio
import logging
import time
from datetime import datetime
from typing import AsyncGenerator, Optional

import aiohttp

from sparta.tiktokapi.access import get_header
from sparta.tiktokapi.models.constants import USER_VIDEO_FIELDS
from sparta.tiktokapi.models.model import TiktokResponse, UserLikedVideosData, UserPinnedVideosData, UserRepostedVideosData, VideoObject

logger = logging.getLogger(__name__)


async def query_user_liked_videos(bearer_token: str, username: str, start_time: datetime, max_count: Optional[int] = 100) -> AsyncGenerator[VideoObject, None]:
    """Asynchronously retrieves videos liked by a user.

    This function queries the TikTok API to find videos liked by the specified user (https://open.tiktokapis.com/v2/research/user/liked_videos/). It handles
    rate limiting and pagination of results.

    Args:
        bearer_token (str): The bearer token for authorization.
        username (str): The username of the TikTok user.
        start_time (datetime): The starting time from which videos are retrieved.
        max_count (Optional[int], optional): The maximum number of videos to retrieve. Default and max is 100. It is possible that the API returns fewer videos
          than the max count due to content moderation outcomes, videos being deleted, marked as private by users, or more.

    Yields:
        VideoObject: An object representing each liked video.

    Raises:
        Exception: If an HTTP error occurs or the query fails.
    """
    async with aiohttp.ClientSession(headers=get_header(bearer_token)) as session:
        params = {"fields": USER_VIDEO_FIELDS}
        body = {"username": username, "max_count": max_count, "cursor": time.mktime(start_time.timetuple())}
        logger.debug(f"Query user liked videos body={body}")

        while True:
            async with session.post("https://open.tiktokapis.com/v2/research/user/liked_videos/", params=params, json=body) as response:
                if response.status == 429:
                    logger.error(f"Too Many Requests (HTTP {response.status}): {await response.text()}")
                    await asyncio.sleep(10)
                    continue

                if not response.ok:
                    logger.error(f"Cannot query videos (HTTP {response.status}): {await response.text()}")
                    raise Exception

                tiktokresponse = TiktokResponse.model_validate(await response.json())
                data = tiktokresponse.data
                assert isinstance(data, UserLikedVideosData)

                for video in data.user_liked_videos:
                    yield video

                if data.has_more:
                    body["cursor"] = data.cursor
                    body["search_id"] = data.search_id
                else:
                    break


async def query_user_pinned_videos(bearer_token: str, username: str, start_time: datetime, max_count: Optional[int] = 100) -> AsyncGenerator[VideoObject, None]:
    """Asynchronously retrieves videos pinned by a user.

    This function queries the TikTok API to find videos pinned by the specified user (https://open.tiktokapis.com/v2/research/user/pinned_videos/). It handles
    rate limiting and pagination of results.

    Args:
        bearer_token (str): The bearer token for authorization.
        username (str): The username of the TikTok user.
        start_time (datetime): The starting time from which videos are retrieved.
        max_count (Optional[int], optional): The maximum number of videos to retrieve. Default and max is 100. It is possible that the API returns fewer videos
          than the max count due to content moderation outcomes, videos being deleted, marked as private by users, or more.

    Yields:
        VideoObject: An object representing each pinned video.

    Raises:
        Exception: If an HTTP error occurs or the query fails.
    """
    async with aiohttp.ClientSession(headers=get_header(bearer_token)) as session:
        params = {"fields": USER_VIDEO_FIELDS}
        body = {"username": username, "max_count": max_count, "cursor": time.mktime(start_time.timetuple())}
        logger.debug(f"Query user liked videos body={body}")

        async with session.post("https://open.tiktokapis.com/v2/research/user/pinned_videos/", params=params, json=body) as response:
            if not response.ok:
                logger.error(f"Cannot query videos (HTTP {response.status}): {await response.text()}")
                raise Exception

            tiktokresponse = TiktokResponse.model_validate(await response.json())

            data = tiktokresponse.data
            assert isinstance(data, UserPinnedVideosData)

            for video in data.pinned_videos_list:
                yield video


async def query_user_reposted_videos(
    bearer_token: str, username: str, start_time: datetime, max_count: Optional[int] = 100
) -> AsyncGenerator[VideoObject, None]:
    """Asynchronously retrieves videos reposted by a user.

    This function queries the TikTok API to find videos reposted by the specified user (https://open.tiktokapis.com/v2/research/user/reposted_videos/). It
    handles rate limiting and pagination of results.

    Args:
        bearer_token (str): The bearer token for authorization.
        username (str): The username of the TikTok user.
        start_time (datetime): The starting time from which videos are retrieved.
        max_count (Optional[int], optional): The maximum number of videos to retrieve. Default and max is 100. It is possible that the API returns fewer videos
          than the max count due to content moderation outcomes, videos being deleted, marked as private by users, or more.

    Yields:
        VideoObject: An object representing each reposted video.

    Raises:
        Exception: If an HTTP error occurs or the query fails.
    """
    async with aiohttp.ClientSession(headers=get_header(bearer_token)) as session:
        params = {"fields": USER_VIDEO_FIELDS}
        body = {"username": username, "max_count": max_count, "cursor": time.mktime(start_time.timetuple())}
        logger.debug(f"Query user liked videos body={body}")

        while True:
            async with session.post("https://open.tiktokapis.com/v2/research/user/reposted_videos/", params=params, json=body) as response:
                if response.status == 429:
                    logger.error(f"Too Many Requests (HTTP {response.status}): {await response.text()}")
                    await asyncio.sleep(10)
                    continue

                if not response.ok:
                    logger.error(f"Cannot query videos (HTTP {response.status}): {await response.text()}")
                    raise Exception

                tiktokresponse = TiktokResponse.model_validate(await response.json())
                data = tiktokresponse.data
                assert isinstance(data, UserRepostedVideosData)

                for video in data.user_reposted_videos:
                    yield video

                if data.has_more:
                    body["cursor"] = data.cursor
                    body["search_id"] = data.search_id
                else:
                    break
