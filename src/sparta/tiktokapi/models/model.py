#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""tiktok_models.py: Models for TikTok API responses.

This module defines data models using Pydantic for various TikTok API responses, including video details, comments, user information, followers, and more.

Examples:
    Define a video object::

        from sparta.tiktokapi.models.model import VideoObject

        video = VideoObject(
            id=12345,
            create_time=1617187200,
            username="example_user",
            region_code="US",
            video_description="This is an example video",
            comment_count=100,
            share_count=50,
            view_count=1000,
            hashtag_names=["example", "video"]
        )
        print(video)

Source: https://developers.tiktok.com/doc/research-api-codebook/
"""
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class Error(BaseModel):
    code: str
    message: str
    log_id: str


class VideoObject(BaseModel):
    id: int = Field(..., description='Unique identifier for the TikTok video. Also called "item_id" or "video_id"')
    create_time: int = Field(..., description="UTC Unix epoch (in seconds) of when the TikTok video was posted. (Inherited field from TNS research API)")
    username: str = Field(..., description="The video's author's username")
    region_code: str = Field(..., description="A two digit code for the country where the video creator registered their account")
    video_description: str = Field(..., description="The description of the video, also known as the title")
    music_id: Optional[int] = Field(None, description="The music_id used in the video")
    like_count: Optional[int] = Field(None, description="The number of likes the video has received")
    comment_count: int = Field(..., description="The number of comments the video has received")
    share_count: int = Field(..., description="The number of shares the video has received")
    view_count: int = Field(..., description="The number of video views the video has received")
    effect_ids: Optional[List[str]] = Field(None, description="The list of effect ids applied on the video")
    hashtag_names: List[str] = Field(..., description="The list of hashtag names that the video participates in")
    playlist_id: Optional[int] = Field(None, description="The ID of playlist that the video belongs to")
    voice_to_text: Optional[str] = Field(
        None, description="Voice to text and subtitles (for videos that have voice to text features on, show the texts already generated)"
    )

    model_config = ConfigDict(from_attributes=True)


class QueryVideoResponseData(BaseModel):
    videos: List[VideoObject] = Field(..., description="A list of video objects that match the query.")
    cursor: int = Field(..., description="Returns video results from the given index.")
    has_more: bool = Field(..., description="Whether there are more videos or not.")
    search_id: str = Field(
        ...,
        description="""A search_id is a unique identifier assigned to a cached search result.
        This identifier enables the resumption of a prior search and retrieval of additional results based on the same search criteria.""",
    )


class CommentObject(BaseModel):
    id: int = Field(..., description="The unique ID for the comment")
    text: str = Field(..., description="The text within the comment")
    video_id: int = Field(..., description="The ID of the video or item that the comment is under")
    parent_comment_id: int = Field(..., description="The ID of the comment's parent comment, if any")
    like_count: Optional[int] = Field(None, description="The number of likes a comment has")
    reply_count: int = Field(..., description="The number of replies a comment has")
    create_time: int = Field(..., description="The unix timestamp that the comment was created on")


class ResearchVideoCommentsData(BaseModel):
    comments: List[CommentObject] = Field(..., description="A list of comment objects.")
    cursor: int = Field(..., description="The cursor of the next page.")
    has_more: bool = Field(..., description="Whether there are more videos or not.")


class UserInfoObject(BaseModel):
    display_name: str = Field(..., description="The user's display name / nickname")
    bio_description: str = Field(..., description="The user's bio description")
    avatar_url: str = Field(..., description="The url to a user's profile picture")
    is_verified: bool = Field(..., description="The user's verified status. True if verified, false if not")
    following_count: int = Field(..., description="The number of people the user is following")
    follower_count: int = Field(..., description="The number of followers the user has")
    video_count: int = Field(..., description="The number of videos the user has posted")
    likes_count: int = Field(..., description="The total number of likes the user has accumulated")


class UserFollowerInfoObject(BaseModel):
    display_name: str = Field(..., description="The profile name of the follower of this user / that the user is following.")
    username: str = Field(..., description="The username of the follower of this user / that the user is following.")


class UserLikedVideosData(BaseModel):
    user_liked_videos: List[VideoObject] = Field(..., description="A list of video objects that match the query.")
    cursor: int = Field(..., description="Retrieve liked videos starting from the specified Unix timestamp in UTC seconds")
    has_more: bool = Field(..., description="Whether there are more videos or not.")
    search_id: str = Field(
        ...,
        description="""A search_id is a unique identifier assigned to a cached search result.
        This identifier enables the resumption of a prior search and retrieval of additional results based on the same search criteria.""",
    )


class UserPinnedVideosData(BaseModel):
    pinned_videos_list: List[VideoObject] = Field(..., description="A list of video objects that match the query.")


class UserRepostedVideosData(BaseModel):
    user_reposted_videos: List[VideoObject] = Field(..., description="A list of video objects that match the query.")
    cursor: int = Field(..., description="Retrieve liked videos starting from the specified Unix timestamp in UTC seconds")
    has_more: bool = Field(..., description="Whether there are more videos or not.")
    search_id: str = Field(
        ...,
        description="""A search_id is a unique identifier assigned to a cached search result.
        This identifier enables the resumption of a prior search and retrieval of additional results based on the same search criteria.""",
    )


class UserFollowerData(BaseModel):
    user_followers: List[UserFollowerInfoObject] = Field(..., description="A list of user info objects that match the query.")
    cursor: int = Field(
        ...,
        description="""Accounts the user started following on or before this time will be returned. It is a Unix timestamp in UTC seconds.
        Default value is set as the time this request was made.""",
    )
    has_more: bool = Field(..., description="Whether there are more accounts this user is following or not.")


class UserFollowingData(BaseModel):
    user_following: List[UserFollowerInfoObject] = Field(..., description="A list of user info objects that match the query.")
    cursor: int = Field(
        ...,
        description="""Accounts the user started following / Followers that followed this user on or before this time will be returned.
        It is a Unix timestamp in UTC seconds. Default value is set as the time this request was made.""",
    )
    has_more: bool = Field(..., description="Whether there are more accounts this user is following / has more followers or not or not.")


class TiktokResponse(BaseModel):
    data: Union[
        QueryVideoResponseData, ResearchVideoCommentsData, UserInfoObject, UserLikedVideosData, UserPinnedVideosData, UserFollowerData, UserFollowingData, Dict
    ]
    error: Error
