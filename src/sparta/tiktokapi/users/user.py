#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""tiktok_user_queries.py: Implementation of TikTok API functions for querying user information, followers, and following.

This module contains functions to interact with the TikTok API for retrieving user information, followers, and following lists.
It includes asynchronous implementations to handle API requests efficiently and manage rate limiting.

Examples:
    Retrieve user information::

        from sparta.tiktokapi.access import create_bearer_token
        from sparta.tiktokapi.users.user import query_user_info

        client_key = "your_client_key"
        client_secret = "your_client_secret"
        bearer_token = create_bearer_token(client_key, client_secret)
        username = "example_user"

        user_info = await query_user_info(bearer_token, username)
        print(user_info)

    Retrieve user followers::

        from sparta.tiktokapi.access import create_bearer_token
        from sparta.tiktokapi.users.user import query_user_followers

        client_key = "your_client_key"
        client_secret = "your_client_secret"
        bearer_token = create_bearer_token(client_key, client_secret)
        username = "example_user"

        async for follower in query_user_followers(bearer_token, username):
            print(follower)

    Retrieve user following::

        from sparta.tiktokapi.access import create_bearer_token
        from sparta.tiktokapi.users.user import query_user_following

        client_key = "your_client_key"
        client_secret = "your_client_secret"
        bearer_token = create_bearer_token(client_key, client_secret)
        username = "example_user"

        async for following in query_user_following(bearer_token, username):
            print(following)
"""
import asyncio
import logging
from typing import AsyncGenerator, Dict, Optional

import aiohttp

from sparta.tiktokapi.access import get_header
from sparta.tiktokapi.models.constants import USER_INFO_FIELDS
from sparta.tiktokapi.models.model import TiktokResponse, UserFollowerData, UserFollowerInfoObject, UserFollowingData, UserInfoObject

logger = logging.getLogger(__name__)


async def query_user_info(bearer_token: str, username: str) -> UserInfoObject:
    """Asynchronously retrieves information about a TikTok user.

    This function queries the TikTok API to get detailed information about a user based on their username (https://open.tiktokapis.com/v2/research/user/info/).

    Args:
        bearer_token (str): The bearer token for authentication.
        username (str): The username of the TikTok user.

    Returns:
        UserInfoObject: An object containing the user's information.

    Raises:
        Exception: If an HTTP error occurs or the query fails.
    """
    async with aiohttp.ClientSession(headers=get_header(bearer_token)) as session:
        params = {"fields": USER_INFO_FIELDS}
        body = {"username": username}
        logger.debug(f"Query video body={body}")
        async with session.post("https://open.tiktokapis.com/v2/research/user/info/", params=params, json=body) as response:
            if not response.ok:
                logger.error(f"Cannot query user info (HTTP {response.status}): {await response.text()}")
                raise Exception

            tiktokresponse = TiktokResponse.model_validate(await response.json())
            data = tiktokresponse.data
            assert isinstance(data, UserInfoObject)
            return data


async def query_user_followers(bearer_token: str, username: str, max_count: Optional[int] = 100) -> AsyncGenerator[UserFollowerInfoObject, None]:
    """Asynchronously retrieves the followers of a TikTok user.

    This function queries the TikTok API to get a list of followers for the specified user. It handles rate limiting and pagination of results
    (https://developers.tiktok.com/doc/research-api-specs-query-user-followers/).

    Args:
        bearer_token (str): The bearer token for authentication.
        username (str): The username of the TikTok user.
        max_count (Optional[int], optional): The maximum number of videos to retrieve. Default and max is 100. It is possible that the API returns fewer videos
          than the max count due to content moderation outcomes, videos being deleted, marked as private by users, or more.

    Yields:
        UserFollowerInfoObject: An object representing each follower.

    Raises:
        Exception: If an HTTP error occurs or the query fails.
    """
    async with aiohttp.ClientSession(headers=get_header(bearer_token)) as session:
        params: Dict = {}
        body = {"username": username, "max_count": max_count}
        logger.debug(f"Query user folowers body={body}")

        while True:
            async with session.post("https://open.tiktokapis.com/v2/research/user/followers/", params=params, json=body) as response:
                if response.status == 429:
                    logger.error(f"Too Many Requests (HTTP {response.status}): {await response.text()}")
                    await asyncio.sleep(10)
                    continue

                if not response.ok:
                    logger.error(f"Cannot query user folowers (HTTP {response.status}): {await response.text()}")
                    raise Exception

                tiktokresponse = TiktokResponse.model_validate(await response.json())
                data = tiktokresponse.data
                assert isinstance(data, UserFollowerData)

                for user in data.user_followers:
                    yield user

                if data.has_more:
                    body["cursor"] = data.cursor
                else:
                    break


async def query_user_following(bearer_token: str, username: str, max_count: Optional[int] = 100) -> AsyncGenerator[UserFollowerInfoObject, None]:
    """Asynchronously retrieves the users followed by a TikTok user.

    This function queries the TikTok API to get a list of users followed by the specified user. It handles rate limiting and pagination of results.
    (https://developers.tiktok.com/doc/research-api-specs-query-user-following/)

    Args:
        bearer_token (str): The bearer token for authentication.
        username (str): The username of the TikTok user.
        max_count (Optional[int], optional): The maximum number of videos to retrieve. Default and max is 100. It is possible that the API returns fewer videos
          than the max count due to content moderation outcomes, videos being deleted, marked as private by users, or more.

    Yields:
        UserFollowerInfoObject: An object representing each followed user.

    Raises:
        Exception: If an HTTP error occurs or the query fails.
    """
    async with aiohttp.ClientSession(headers=get_header(bearer_token)) as session:
        params: Dict = {}
        body = {"username": username, "max_count": max_count}
        logger.debug(f"Query user folowers body={body}")

        while True:
            async with session.post("https://open.tiktokapis.com/v2/research/user/following/", params=params, json=body) as response:
                if response.status == 429:
                    logger.error(f"Too Many Requests (HTTP {response.status}): {await response.text()}")
                    await asyncio.sleep(10)
                    continue

                if not response.ok:
                    logger.error(f"Cannot query user folowers (HTTP {response.status}): {await response.text()}")
                    raise Exception

                tiktokresponse = TiktokResponse.model_validate(await response.json())
                data = tiktokresponse.data
                assert isinstance(data, UserFollowingData)

                for user in data.user_following:
                    yield user

                if data.has_more:
                    body["cursor"] = data.cursor
                else:
                    break
