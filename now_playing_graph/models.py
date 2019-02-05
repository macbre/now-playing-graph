"""
Models representing artists and songs. They're based on schema.org types.
"""
# https://docs.python.org/3.7/library/hashlib.html
from hashlib import md5


class BaseModel:
    """
    Base class for schema.org-based models
    """
    def __init__(self, name: str, properties: dict = None, relations: dict = None):
        """
        :type name str
        :type properties dict
        :type relations dict
        """
        self.name = name
        self.properties = properties or dict()
        self.relations = relations or dict()
        self.type = self.get_type()

        # model unique ID, used when rendering a graph
        self._hash = md5('{}-{}'.format(self.name, self.type).encode('utf-8')).hexdigest()[:9]

    def get_type(self):
        """
        :rtype: str
        """
        raise NotImplementedError(
            '{}.get_type() should be implemented'.format(self.__class__.__name__))

    @staticmethod
    def get_size():
        """
        :rtype: int
        """
        return 1

    def get_properties(self):
        """
        :rtype: dict
        """
        return self.properties

    def get_hash(self):
        """
        :rtype: str
        """
        return self._hash

    def __getitem__(self, item):
        return self.properties.get(item)

    def __setitem__(self, key: str, value):
        self.properties[key] = value

    def __repr__(self):
        ret = '<{} https://schema.org/{} ({})'.\
            format(self.__class__.__name__, self.get_type(), self.name)

        # dump node properties
        # (p:Person {name: 'Jennifer'})
        if self.properties:
            ret += ' '

        ret += ', '.join([
            '{} = "{}"'.format(key, value)
            for key, value in self.properties.items()
        ])

        ret += '>'

        # dump relations
        # -[rel:IS_FRIENDS_WITH]->
        for relation, target in self.relations.items():
            ret += '\n\t--[:{}]->({})'.format(relation, target.name)

        return ret


class ArtistModel(BaseModel):
    """
    Represents a band or an artist
    """
    # https://schema.org/MusicGroup
    def get_type(self):
        return 'MusicGroup'

    def get_size(self):
        """
        :rtype: int
        """
        return self['songs']


class SongModel(BaseModel):
    """
    Represents a song
    """
    # https://schema.org/MusicRecording
    def get_type(self):
        return 'MusicRecording'

    def get_size(self):
        """
        :rtype: int
        """
        return self['duration']


def timeline_to_models(timeline, min_songs: int = None):
    """
    Builds a set of models representing artists and songs using a provided playlist timeline.

    You can also filter out bands with less than "min_songs" songs
    to make the graph a bit smaller and more meaningful.

    :type timeline list[now_playing_graph.timeline.TimelineEntry]
    :type min_songs int
    :rtype: list[BaseModel]
    """
    timeline = list(timeline)

    # create a unique set of artists
    artists = {entry.artist_name for entry in timeline}  # set comprehension
    artists = sorted(artists)

    # build a hash of artists models
    artists = {
        artist: ArtistModel(name=artist, properties={'songs': 0}) for artist in artists
    }

    # prepare a list of unique (artist, song) pairs
    songs = set()

    for entry in timeline:
        songs.add((entry.artist_name, entry.song_title, entry.duration))

        # increase songs counter for each artist
        artists[entry.artist_name]['songs'] += 1

    # filter out artists with less than min_songs
    if min_songs:
        artists = {
            artist: entry for artist, entry in artists.items() if entry['songs'] >= min_songs
        }

    # sort the sets to make them more deterministic
    songs = list(sorted(songs))

    # print(artists, songs)

    # using the list build a set of songs models that link to an artist
    songs = [
        SongModel(
            name=song,
            properties={'duration': duration},
            relations={'byArtist': artists[artist]}
        )
        for artist, song, duration in songs if artist in artists
    ]

    # return both artists and songs (and  make the order deterministic)
    return sorted(artists.values(), key=lambda i: i.name) + songs
