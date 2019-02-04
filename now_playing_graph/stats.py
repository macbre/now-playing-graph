"""
Prepare some stats from timelines
"""
# https://docs.python.org/3.7/library/collections.html#collections.Counter
from collections import Counter


def get_timeline_stats(timeline):
    """
    :type timeline list[now_playing_graph.timeline.TimelineEntry]
    :rtype: dict
    """
    top_artists = Counter()
    top_songs = Counter()
    longest_songs = dict()

    for entry in timeline:
        top_artists.update((entry.artist_name,))
        top_songs.update((entry.song_title,))

        if entry.song_title not in longest_songs:
            longest_songs[entry.song_title] = entry.duration

    return dict(
        top_artists=top_artists.most_common(10),
        top_songs=top_songs.most_common(10),
        longest_songs=Counter(longest_songs).most_common(10),
    )
