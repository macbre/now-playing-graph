"""
Tests for stream.py functions
"""
from os import path

from now_playing_graph.stream import read_gzip, kvf_stream_to_timeline


def test_kvf_stream_to_timeline_gzip():
    in_file = read_gzip(path.join(path.dirname(__file__), 'fixtures', 'streamA.gz'))
    timeline = kvf_stream_to_timeline(in_file)

    timeline = list(timeline)
    print(timeline)

    assert len(timeline) == 5

    assert [entry['artist_name'] for entry in timeline] == \
           ['Jasmin', 'Teitur', 'Hamradun', 'Frændur', 'Wolfgang']

    assert [entry['song_title'] for entry in timeline] == \
           ['Make Sense', 'I Want to Be Kind', 'Ein stutt og stokkut løta', 'Uttanumtos', 'Ice Cold']

    # assert False
