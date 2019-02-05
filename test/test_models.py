"""
Tests for models.py module
"""
from now_playing_graph.models import ArtistModel, SongModel, timeline_to_models
from now_playing_graph.stream import kvf_stream_to_timeline


def test_models():
    artist = ArtistModel(name='Foo Fighters')

    assert repr(artist) == '<ArtistModel https://schema.org/MusicGroup (Foo Fighters)>'
    assert repr(SongModel(name='In The Bar')) == '<SongModel https://schema.org/MusicRecording (In The Bar)>'

    assert repr(SongModel(name='In The Bar', properties={'duration': 124})) == \
        '<SongModel https://schema.org/MusicRecording (In The Bar) duration = "124">'

    assert repr(SongModel(name='In The Bar', properties={'duration': 165}, relations={'byArtist': artist})) == \
        '<SongModel https://schema.org/MusicRecording (In The Bar) duration = "165">\n' \
        '\t--[:byArtist]->(Foo Fighters)'


def test_timeline_to_models():
    stream = """
data: {"updated":"2019-01-20T18:50:24.980","now":{"artist":"Eivør Pálsdóttir","title":"Elisabeth og Elinborg","start":"2019-01-20T18:50:23.541"},"next":{"artist":"Benjamin Rajani","title":"Sálmur 40","start":"2019-01-20T18:54:36.950"}}
data: {"updated":"2019-01-21T04:02:57.133","now":{"artist":"Enekk","title":"Ódn","start":"2019-01-21T04:02:55.506"},"next":{"artist":"Ragnar í vík","title":"You Broke Your Own Heart","start":"2019-01-21T04:07:24"}}
data: {"updated":"2019-01-23T02:42:21.638","now":{"artist":"Eivør Pálsdóttir","title":"Vársins ljóð","start":"2019-01-23T02:42:19.771"},"next":{"artist":"Jens John Jakobsen","title":"Undur sólar hita","start":"2019-01-23T02:46:54.400"}}
data: {"updated":"2019-01-26T06:23:55.616","now":{"artist":"Enekk","title":"Slatur","start":"2019-01-26T06:23:54.161"},"next":{"artist":"Taxi","title":"Meistarin","start":"2019-01-26T06:27:09.274"}}
data: {"updated":"2019-02-04T12:10:24.312","now":{"artist":"Eivør Pálsdóttir","title":"Mannabarn","start":"2019-02-04T12:10:22.916"},"next":{"artist":"The Dreams","title":"Verden vil bedrages","start":"2019-02-04T12:15:15.660"}}
data: {"updated":"2019-01-22T12:08:11.478","now":{"artist":"Orka","title":"Hon leitar","start":"2019-01-22T12:08:10.052"},"next":{"artist":"Holgar","title":"Veitslan","start":"2019-01-22T12:10:22.780"}}
""".strip().split("\n")

    timeline = list(kvf_stream_to_timeline(stream))
    models = timeline_to_models(timeline)

    assert "\n".join(map(repr, models)) == """
<ArtistModel https://schema.org/MusicGroup (Eivør Pálsdóttir)>
<ArtistModel https://schema.org/MusicGroup (Enekk)>
<ArtistModel https://schema.org/MusicGroup (Orka)>
<SongModel https://schema.org/MusicRecording (Elisabeth og Elinborg) duration = "253">
	--[:byArtist]->(Eivør Pálsdóttir)
<SongModel https://schema.org/MusicRecording (Mannabarn) duration = "292">
	--[:byArtist]->(Eivør Pálsdóttir)
<SongModel https://schema.org/MusicRecording (Vársins ljóð) duration = "274">
	--[:byArtist]->(Eivør Pálsdóttir)
<SongModel https://schema.org/MusicRecording (Slatur) duration = "195">
	--[:byArtist]->(Enekk)
<SongModel https://schema.org/MusicRecording (Ódn) duration = "268">
	--[:byArtist]->(Enekk)
<SongModel https://schema.org/MusicRecording (Hon leitar) duration = "132">
	--[:byArtist]->(Orka)
    """.strip()

    # assert False
