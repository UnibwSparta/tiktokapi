#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""constants.py: Constants for TikTok API Endpoints.

This module defines Fields as constants for various TikTok API endpoints, including video details, comments, user information, followers, and more.
"""
VIDEO_FIELDS = "id,video_description,create_time,region_code,share_count,view_count,like_count,comment_count,music_id,hashtag_names,username,effect_ids,playlist_id,voice_to_text,is_stem_verified,favorites_count,video_duration"  # noqa
VIDEO_COMMENT_FIELS = "id,video_id,text,like_count,reply_count,parent_comment_id,create_time"
USER_INFO_FIELDS = "display_name,bio_description,avatar_url,is_verified,follower_count,following_count,likes_count,video_count"
USER_VIDEO_FIELDS = "id,create_time,username,region_code,video_description,music_id,like_count,comment_count,share_count,view_count,hashtag_names,is_stem_verified,video_duration"  # noqa
