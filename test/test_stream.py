"""
Tests for stream.py functions
"""
from os import path

from now_playing_graph.stream import \
    read_gzip, read_text,\
    kvf_stream_to_timeline

dir_name = path.dirname(__file__)


def print_timeline(timeline):
    """
    :type timeline list[now_playing_graph.timeline.TimelineEntry]
    """
    print('\n'.join([str(entry) for entry in timeline]))


def test_kvf_stream_to_timeline_gzip():
    in_file = read_gzip(path.join(dir_name, 'fixtures', 'streamA.gz'))
    timeline = list(kvf_stream_to_timeline(in_file))

    print_timeline(timeline)

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
    in_file = read_text(path.join(dir_name, 'fixtures', 'streamB'))
    timeline = list(kvf_stream_to_timeline(in_file))

    print_timeline(timeline)

    assert len(timeline) == 4

    assert [entry.artist_name for entry in timeline] == \
           ['Fróði Bjarnason', 'Vincent', 'Enekk', 'KYLIE MINOGUE feat. JACK SAVORETTI']

    assert [entry.song_title for entry in timeline] == \
           ['Where My Home Is', 'Dyrabart', 'Mín sorg', "Music's Too Sad Without You (edit)"]

    assert [entry.duration for entry in timeline] == \
           [256, 287, 245, 206]

    # assert False


def test_kvf_stream_from_string():
    stream = """
data: {"updated":"2019-02-04T13:25:04.585","now":{"artist":"Rita Ora & Rudimental","title":"Summer Love","start":"2019-02-04T13:25:03.090"},"next":{"artist":"Alvaro Soler","title":"La Cintura","start":"2019-02-04T13:29:21.084"}}
data: {"updated":"2019-02-04T13:25:04.585","now":{"artist":{},"title":{},"start":"2019-02-04T13:25:03.090"},"next":{"artist":"Alvaro Soler","title":"La Cintura","start":"2019-02-04T13:29:21.084"}}
data: {"updated":"2019-02-04T13:49:36.550","now":{"artist":{},"title":{},"start":"2019-02-04T13:25:03.090"},"next":{"artist":"Bent Fabricius-Bjerre","title":"Nøglen til paradis","start":"2019-02-04T13:29:21.084"}}
data: {"updated":"2019-02-04T14:00:01.086","now":{"artist":{},"title":{},"start":{}},"next":{"artist":{},"title":{},"start":{}}}
data: {"updated":"2019-02-04T14:37:16.794","now":{"artist":"Vestmenn","title":"Ró","start":"2019-02-04T14:37:15.186"},"next":{"artist":"Kári P","title":"Bara tú riggar","start":"2019-02-04T14:43:20.266"}}
""".strip().split("\n")

    timeline = list(kvf_stream_to_timeline(stream))

    print_timeline(timeline)

    assert len(timeline) == 2

    # assert False


def test_kvf_stream_from_string2():
    stream = """
data: {"updated":"2019-01-27T19:55:55.896","now":{"artist":"Moyzeskvartettin","title":"String Quartet No.17 in Bb, K.458 ('The Hunt') 2.Menuetto- Moderato","start":"2019-01-27T19:55:54.386"},"next":{"artist":{},"title":{},"start":{}}}
data: {"updated":"2019-01-27T19:59:51.112","now":{"artist":{},"title":"Ann ti Orff","start":"2019-01-27T19:59:49.625"},"next":{"artist":{},"title":{},"start":{}}}
data: {"updated":"2019-01-27T19:59:51.112","now":{"artist":{},"title":"Ann ti Orff","start":"2019-01-27T19:59:49.625"},"next":{"artist":{},"title":{},"start":{}}}
data: {"updated":"2019-01-27T20:00:48.644","now":{"artist":{},"title":"Carmina Burana FSO","start":"2019-01-27T20:00:47.250"},"next":{"artist":{},"title":{},"start":{}}}
data: {"updated":"2019-01-27T21:03:37.157","now":{"artist":{},"title":{},"start":{}},"next":{"artist":{},"title":{},"start":{}}}
data: {"updated":"2019-01-27T22:00:27.400","now":{"artist":{},"title":{},"start":{}},"next":{"artist":"Elisa's","title":"Be mig! Se mig! Ge mig!","start":"2019-01-27T22:03:11.724"}}
data: {"updated":"2019-01-27T22:00:27.400","now":{"artist":{},"title":{},"start":{}},"next":{"artist":"Elisa's","title":"Be mig! Se mig! Ge mig!","start":"2019-01-27T22:03:11.724"}}
data: {"updated":"2019-01-27T22:00:27.400","now":{"artist":{},"title":{},"start":{}},"next":{"artist":"Elisa's","title":"Be mig! Se mig! Ge mig!","start":"2019-01-27T22:03:11.724"}}
data: {"updated":"2019-01-27T22:03:08.947","now":{"artist":"Elisa's","title":"Be mig! Se mig! Ge mig!","start":"2019-01-27T22:03:06.959"},"next":{"artist":"Doodle Bugs","title":"Suderø","start":"2019-01-27T22:06:10.573"}}
""".strip().split("\n")

    timeline = list(kvf_stream_to_timeline(stream))

    print_timeline(timeline)

    assert len(timeline) == 2

    assert [entry.artist_name for entry in timeline] == \
           ['Moyzeskvartettin', "Elisa's"]

    assert [entry.song_title for entry in timeline] == \
           ["String Quartet No.17 in Bb, K.458 ('The Hunt') 2.Menuetto- Moderato", 'Be mig! Se mig! Ge mig!']

    assert [entry.duration for entry in timeline] == \
           [236, 183]

    # assert False


def test_read_stream_from_data():
    in_file = read_gzip(path.join(dir_name, '..', 'data', 'kvf.log.gz'))
    timeline = list(kvf_stream_to_timeline(in_file))

    # print_timeline(timeline)

    assert len(timeline) == 2197
