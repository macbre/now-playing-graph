"""
Timeline handling functions
"""
from datetime import datetime

# https://docs.python.org/3/library/dataclasses.html
from dataclasses import dataclass


@dataclass
class TimelineEntry:
    """
    Represents a single entry of radio stream timeline
    """
    artist_name: str
    song_title: str
    duration: int
    played_at: datetime
