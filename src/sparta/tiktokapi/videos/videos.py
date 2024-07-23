#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""tiktok_video_queries.py: Implementation of TikTok API functions for querying videos and comments.

This module contains functions to interact with the TikTok API for retrieving videos and comments based on specific search queries.
It includes asynchronous implementations to handle API requests efficiently and manage rate limiting.

Examples:
    Asynchronously query videos::

        from datetime import date
        from sparta.tiktokapi.access import create_bearer_token
        from tiktok_video_queries import query_videos

        client_key = "your_client_key"
        client_secret = "your_client_secret"
        bearer_token = create_bearer_token(client_key, client_secret)
        query = {"and": [{"field": "title", "value": "example"}]}
        start_date = date(2023, 1, 1)
        end_date = date(2023, 1, 31)

        async for video in query_videos(bearer_token, query, start_date, end_date):
            print(video)

    Asynchronously query video comments::

        from sparta.tiktokapi.access import create_bearer_token
        from tiktok_video_queries import query_video_comments

        client_key = "your_client_key"
        client_secret = "your_client_secret"
        bearer_token = create_bearer_token(client_key, client_secret)
        video_id = 1234567890

        async for comment in query_video_comments(bearer_token, video_id):
            print(comment)
"""
import asyncio
import logging
from datetime import date
from typing import AsyncGenerator, Dict, Optional

import aiohttp

from sparta.tiktokapi.access import get_header
from sparta.tiktokapi.models.constants import VIDEO_COMMENT_FIELS, VIDEO_FIELDS
from sparta.tiktokapi.models.model import CommentObject, Error, QueryVideoResponseData, ResearchVideoCommentsData, TiktokResponse, VideoObject

logger = logging.getLogger(__name__)


async def query_videos(
    bearer_token: str,
    query: Dict,
    start_date: date,
    end_date: date,
    is_random: Optional[bool] = None,
    max_count: Optional[int] = 100,
) -> AsyncGenerator[VideoObject, None]:
    """Asynchronously retrieves videos based on a specific query.

    This function queries the TikTok API to find videos matching the given search criteria (https://developers.tiktok.com/doc/research-api-specs-query-videos/).
    It handles rate limiting and pagination of results.

    Args:
        bearer_token (str): The bearer token for authentication.
        query (Dict): A JSON object that contains three types of children: and, or, and not, each of which is a list of conditions. A valid query must contain
                      at least one non-empty and, or, or not condition lists.
        start_date (date): The lower bound of video creation time in UTC.
        end_date (date): The upper bound of video creation time in UTC. The end_date must be no more than 30 days after the start_date.
        is_random (Optional[bool]): The flag that indicates whether to return results in random order.  If set to true, the API will return 1-100 videos in a
            random order that matches the query. If set to false or not set, then the API returns results in descending order of video IDs.
        max_count (Optional[int]): The maximum number of videos to retrieve. Default and max is 100. It is possible that the API returns fewer videos
          than the max count due to content moderation outcomes, videos being deleted, marked as private by users, or more.

    Yields:
        VideoObject: An object representing each video.

    Raises:
        Exception: If an HTTP error occurs or the query fails.
    """
    gateway_timeout_counter = 0
    async with aiohttp.ClientSession(headers=get_header(bearer_token)) as session:
        params = {"fields": VIDEO_FIELDS}

        body = {"query": query, "start_date": start_date.strftime("%Y%m%d"), "end_date": end_date.strftime("%Y%m%d"), "max_count": max_count}
        if is_random:
            body["is_random"] = is_random

        logger.debug(f"Query video body={body}")
        while True:
            async with session.post("https://open.tiktokapis.com/v2/research/video/query/", params=params, json=body) as response:
                if response.status == 429:
                    logger.error(f"Too Many Requests (HTTP {response.status}): {await response.text()}")
                    await asyncio.sleep(10)
                    continue

                if response.status == 504:
                    logger.error(f"Gateway Timeout (HTTP {response.status})")
                    gateway_timeout_counter += 1
                    if gateway_timeout_counter >= 10:
                        logger.error(f"Gateway Timeout (HTTP {response.status}): {await response.text()}")
                        logger.error("Abort the loop as Gateway has not responded for 1 hour.")
                        raise Exception(f"Gateway Timeout (HTTP {response.status}): {await response.text()}")
                    await asyncio.sleep(600)
                    continue

                if response.status == 500:
                    continue

                response_json = await response.json()

                if not response.ok:
                    logger.warn(f"Cannot query videos (HTTP {response.status}): {await response.text()}")
                    if response.status == 400:
                        error = Error.model_validate(response_json.get("error"))
                        if "is invalid or expired" in error.message:
                            logger.info("Sleep for 10 seconds as the TikTok API will not recognise the search ID if you use it immediately.")
                            await asyncio.sleep(10)
                            continue
                    else:
                        raise Exception(f"Cannot query videos (HTTP {response.status}): {response.text}")

                tiktokresponse = TiktokResponse.model_validate(response_json)
                data = tiktokresponse.data
                if not (isinstance(data, QueryVideoResponseData)):
                    break

                for video in data.videos:
                    yield video

                if data.has_more:
                    body["cursor"] = data.cursor
                    body["search_id"] = data.search_id
                else:
                    break


async def query_video_comments(bearer_token: str, video_id: int, max_count: Optional[int] = 100) -> AsyncGenerator[CommentObject, None]:
    """Asynchronously retrieves comments for a specific video.

    This function queries the TikTok API to find comments on the specified video (https://developers.tiktok.com/doc/research-api-specs-query-video-comments/).
    It handles rate limiting and pagination of results.

    Args:
        bearer_token (str): The bearer token for authentication.
        video_id (int): The ID of the video to retrieve comments for.
        max_count (Optional[int]): The maximum number of videos to retrieve. Default and max is 100. It is possible that the API returns fewer videos
          than the max count due to content moderation outcomes, videos being deleted, marked as private by users, or more.

    Yields:
        CommentObject: An object representing each comment.

    Raises:
        Exception: If an HTTP error occurs or the query fails.

    Note: only the top 1000 comments will be returned, so cursor + max_count <= 1000.
    """
    async with aiohttp.ClientSession(headers=get_header(bearer_token)) as session:
        params = {"fields": VIDEO_COMMENT_FIELS}
        body = {"video_id": video_id, "max_count": max_count}

        logger.debug(f"Query video comments body={body}")
        while True:
            async with session.post("https://open.tiktokapis.com/v2/research/video/comment/list/", params=params, json=body) as response:
                if response.status == 429:
                    logger.error(f"Too Many Requests (HTTP {response.status}): {await response.text()}")
                    await asyncio.sleep(10)
                    continue

                if not response.ok:
                    logger.error(f"Cannot query videos (HTTP {response.status}): {await response.text()}")
                    raise Exception

                tiktokresponse = TiktokResponse.model_validate(await response.json())
                data = tiktokresponse.data
                assert isinstance(data, ResearchVideoCommentsData)

                for comment in data.comments:
                    yield comment

                if data.has_more:
                    body["cursor"] = data.cursor
                    body["search_id"] = data.search_id  # type: ignore
                else:
                    break
