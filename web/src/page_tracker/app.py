""" Flask app that tracks page views using Redis. """

import os
from functools import cache

from flask import Flask
from redis import Redis, RedisError

app = Flask(__name__)


@app.get("/")
def index():
    """Index page

    Returns:
        int: page views
    """
    try:
        page_views = redis().incr("page_views")
    except RedisError:
        app.logger.exception("Redis error")
        return "Sorry, something went wrong. \N{pensive face}", 500

    return f"This page has been viewed {page_views} times."


@cache
def redis():
    """create a Redis connection

    Returns:
        redis instance
    """
    return Redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
