"""
Tests for models.py module
"""
from now_playing_graph.models import ArtistModel, SongModel, timeline_to_models
from now_playing_graph.stream import kvf_stream_to_timeline

from . import STREAM


def test_model():
    artist = ArtistModel(name='Foo Fighters', properties={'songs': 0})

    artist['songs'] += 1
    artist['foo'] = 'bar'

    assert artist['songs'] == 1
    assert artist['foo'] == 'bar'
    assert artist.get_properties() == dict(songs=1, foo='bar')
    # assert False


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
    models = timeline_to_models(kvf_stream_to_timeline(STREAM))

    assert len(models) == 9

    assert "\n".join(map(repr, models)) == """
<ArtistModel https://schema.org/MusicGroup (Eivør Pálsdóttir) songs = "3">
<ArtistModel https://schema.org/MusicGroup (Enekk) songs = "2">
<ArtistModel https://schema.org/MusicGroup (Orka) songs = "1">
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
