"""
Tests for stream.py functions
"""
from os import path

from now_playing_graph.stream import read_gzip, kvf_stream_to_timeline

dir_name = path.dirname(__file__)


def test_kvf_stream_to_timeline_gzip():
    in_file = read_gzip(path.join(dir_name, 'fixtures', 'streamA.gz'))
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


def test_kvf_stream_to_timeline_missing_timestamps():
    with open(path.join(dir_name, 'fixtures', 'streamB')) as in_file:
        timeline = kvf_stream_to_timeline(in_file.readlines())

    timeline = list(timeline)
    print('\n'.join([str(entry) for entry in timeline]))

    assert len(timeline) == 4

    assert [entry.artist_name for entry in timeline] == \
           ['Fróði Bjarnason', 'Vincent', 'Enekk', 'KYLIE MINOGUE feat. JACK SAVORETTI']

    assert [entry.song_title for entry in timeline] == \
           ['Where My Home Is', 'Dyrabart', 'Mín sorg', "Music's Too Sad Without You (edit)"]

    assert [entry.duration for entry in timeline] == \
           [256, 287, 245, 206]

    # assert False
