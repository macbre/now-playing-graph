"""
Tests for stats.py functions
"""
from os import path

from now_playing_graph.stats import get_timeline_stats
from now_playing_graph.stream import read_gzip, kvf_stream_to_timeline

dir_name = path.dirname(__file__)


def test_stats_for_stream_from_data():
    in_file = read_gzip(path.join(dir_name, '..', 'data', 'kvf.log.gz'))
    timeline = kvf_stream_to_timeline(in_file)

    stats = get_timeline_stats(timeline)

    print(stats)

    # top artists
    assert ('Eyðun Nolsøe', 16) in stats['top_artists']
    assert ('Marius Ziska', 16) in stats['top_artists']

    # top songs
    assert stats['top_songs'][0] == ('Lukkan er ei gullið', 10)
    assert stats['top_songs'][1] == ('Á tíni slóð', 9)

    # longest songs
    assert stats['longest_songs'][0] == ('Symphony in C minor I. Allegro molto', 844)
    assert stats['longest_songs'][1] == ('Mendelssohn: Piano Sextet In D, Op. 110 - 1. Allegro Vivace', 773)

    # artist which are most frequently played on the air
    assert stats['longest_artists'][0] == ('Ilona Prunyi', 2433)  # The Seasons, Op. 37b: May. "May Nights"
    assert stats['longest_artists'][1] == ('Gothenburg Symphony Orchestra cond. Okko Kamu, Cond.: Okko Kamu', 2210)

    # assert False
