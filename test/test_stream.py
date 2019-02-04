"""
Tests for stream.py functions
"""
from os import path

from now_playing_graph.stream import read_gzip, kvf_stream_to_timeline


def test_kvf_stream_to_timeline_gzip():
    in_file = read_gzip(path.join(path.dirname(__file__), 'fixtures', 'streamA.gz'))
    timeline = kvf_stream_to_timeline(in_file)

    timeline = list(timeline)
    print('\n'.join([str(entry) for entry in timeline]))

    assert len(timeline) == 5

    assert [entry.artist_name for entry in timeline] == \
           ['Jasmin', 'Teitur', 'Hamradun', 'Frændur', 'Wolfgang']

    assert [entry.song_title for entry in timeline] == \
           ['Make Sense', 'I Want to Be Kind', 'Ein stutt og stokkut løta', 'Uttanumtos', 'Ice Cold']

    assert [entry.duration for entry in timeline] == \
           [254, 249, 165, 208, 180]

    assert timeline[0].played_at.hour == 20, 'Has been played at 8 pm'

    # assert False
