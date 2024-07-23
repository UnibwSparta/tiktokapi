#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""tiktok_api_authentication.py: Functions for TikTok API authentication and header management.

This module contains functions to create a bearer token for authenticating with the TikTok API and to generate headers for API requests.

Examples:
    Create a bearer token::

        from sparta.tiktokapi.access import create_bearer_token

        client_key = "your_client_key"
        client_secret = "your_client_secret"
        bearer_token = create_bearer_token(client_key, client_secret)
        print(bearer_token)

    Get headers for API requests::

        from sparta.tiktokapi.access import get_header

        bearer_token = "your_bearer_token"
        headers = get_header(bearer_token)
        print(headers)
"""
from typing import Dict

import requests


def create_bearer_token(client_key: str, client_secret: str) -> str:
    """Creates a bearer token for TikTok API authentication.

    This function sends a request to the TikTok API to generate a bearer token using the provided client key and client secret.

    Args:
        client_key (str): The client key provided by TikTok for API access.
        client_secret (str): The client secret provided by TikTok for API access.

    Returns:
        str: The bearer token to be used for authentication in subsequent API requests.

    Raises:
        Exception: If the request to the API fails or returns an error.
    """
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cache-Control": "no-cache",
    }

    data = {
        "client_key": client_key,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }

    response = requests.post("https://open.tiktokapis.com/v2/oauth/token/", headers=headers, data=data)
    bearer_token = response.json()["access_token"]
    return bearer_token


def get_header(bearer_token: str) -> Dict:
    """Generates headers for TikTok API requests.

    This function creates the necessary headers for making requests to the TikTok API using the provided bearer token.

    Args:
        bearer_token (str): The bearer token for authentication.

    Returns:
        Dict: A dictionary containing the headers for the API request.
    """
    headers = {"Authorization": f"Bearer {bearer_token}", "content-type": "application/json"}
    return headers
