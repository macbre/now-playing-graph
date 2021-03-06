# now-playing-graph
![](https://raw.githubusercontent.com/macbre/now-playing-graph/master/docs/graph.png)

Processes "now playing" data from [internet radio player](https://kvf.fo/popout/widget) for [Faroese Útvarp](https://kvf.fo/forsida/english).

## Requirements

**Python 3.7 is required** because [`datetime.datetime.fromisoformat` is used](https://docs.python.org/dev/library/datetime.html#datetime.datetime.fromisoformat).

## Why?

As a fan of all Faroese aspects, I'm curious to know:

* which artist is most frequently played?
* which artist songs are played for the the longest time?
* is some artist typically followed by another one?

## Collecting the data

The following bash script is run every minute to scrape "now playing" data from kvf.fo site:

```bash
curl -s --max-time 3 'https://netvarp.kringvarp.fo:80/sse' 2>&1  | grep data >> ~/kvf.log
```

## Data model

"Now playing" stream is turned into a graph with two types of nodes (modeled after [schema.org types](https://schema.org/)):

### Band / artist
> https://schema.org/MusicGroup

* `name`

### Song
> https://schema.org/MusicRecording

* `byArtist` -> a graph's edge linking to band / artist
* `duration`([ISO 8601](https://en.wikipedia.org/wiki/ISO_8601#Durations), e.g. `PT6M33S`)
* `name`

## Statistics

```
$ get_stats
2019-02-11 21:41:47 render_graph         INFO     Going to parse a stream from /home/macbre/src/git/now-playing-graph/data/kvf.log.gz
2019-02-11 21:41:47 root                 INFO     Lines parsed: 21959
2019-02-11 21:41:47 render_graph         INFO     Got a timeline with 2197 entries
top_artists: [('Eyðun Nolsøe', 16), ('Marius Ziska', 16), ('Streaplers', 14), ('Jens Marni Hansen', 14), ('Blátt Gras', 13), ('Ole Ivars', 13), ('Dalia Ouziel,  Gil Sharon,  Ron Ephrat,  Etc.', 12), ('Contrazt', 12), ('Dænsebændet', 12), ('Lasse Stefanz', 12)]

top_songs: [('Lukkan er ei gullið', 10), ('Á tíni slóð', 9), ('Eitt lítið tár í tøgnini', 9), ('Einsemi', 8), ('Heima er saman við tær', 7), ('Lieder Ohne Worte No. 3 in G Minor, Op. 53: Presto Agitato', 6), ('Samrøða fjalla millum', 6), ("Bahib'm'bau (kom við)", 6), ('Leingist so', 6), ('Piano Concerto in A Minor, Op. 7: I. Allegro Maestoso', 6)]

longest_songs: [('Symphony in C minor I. Allegro molto', 844), ('Mendelssohn: Piano Sextet In D, Op. 110 - 1. Allegro Vivace', 773), ('4th Symphony - 3.Il tempo largo', 720), ('Mendelssohn: Piano Sextet In D, Op. 110 - 4. Allegro Vivace', 694), ('Trombone Concerto, Op.81 - 2. satsur Andante', 662), ('Piano Trio In G Minor, Op. 17: I. Allegro Moderato', 633), ('Heljareyga', 613), ('Periferi', 605), ('4th Symphony - 1.Tempo molto moderato, quasi adagio', 598), ('4th Symphony - 4.Allegro', 564)]

longest_artists: [('Ilona Prunyi', 2433), ('Gothenburg Symphony Orchestra cond. Okko Kamu, Cond.: Okko Kamu', 2210), ('Berliner Philharmoniker - Herbert von Karajan', 2168), ('Marius Ziska', 2097), ('Ólavur á Váli', 2044), ('Hannis', 1996), ('Dalia Ouziel,  Gil Sharon,  Ron Ephrat,  Etc.', 1952), ('Stockholm Sinfonietta,  Neemi Jærvi stjórnar', 1869), ('Streaplers', 1745), ('Moyzeskvartettin', 1620)]
```

## Data examples

Here's the snippet of collected data:

```json
data: {"updated":"2019-01-22T20:27:23.930","now":{"artist":"Jasmin","title":"Make Sense","start":"2019-01-22T20:27:22.318"},"next":{"artist":"Teitur","title":"I Want to Be Kind","start":"2019-01-22T20:31:36.810"}}
data: {"updated":"2019-01-22T20:31:37.973","now":{"artist":"Teitur","title":"I Want to Be Kind","start":"2019-01-22T20:31:36.113"},"next":{"artist":"Hamradun","title":"Ein stutt og stokkut løta","start":"2019-01-22T20:35:45.775"}}
data: {"updated":"2019-01-22T20:31:37.973","now":{"artist":"Teitur","title":"I Want to Be Kind","start":"2019-01-22T20:31:36.113"},"next":{"artist":"Hamradun","title":"Ein stutt og stokkut løta","start":"2019-01-22T20:35:45.775"}}
data: {"updated":"2019-01-22T20:31:37.973","now":{"artist":"Teitur","title":"I Want to Be Kind","start":"2019-01-22T20:31:36.113"},"next":{"artist":"Hamradun","title":"Ein stutt og stokkut løta","start":"2019-01-22T20:35:45.775"}}
data: {"updated":"2019-01-22T20:31:37.973","now":{"artist":"Teitur","title":"I Want to Be Kind","start":"2019-01-22T20:31:36.113"},"next":{"artist":"Hamradun","title":"Ein stutt og stokkut løta","start":"2019-01-22T20:35:45.775"}}
data: {"updated":"2019-01-22T20:35:42.473","now":{"artist":"Hamradun","title":"Ein stutt og stokkut løta","start":"2019-01-22T20:35:40.614"},"next":{"artist":"Frændur","title":"Uttanumtos","start":"2019-01-22T20:38:26.234"}}
data: {"updated":"2019-01-22T20:35:42.473","now":{"artist":"Hamradun","title":"Ein stutt og stokkut løta","start":"2019-01-22T20:35:40.614"},"next":{"artist":"Frændur","title":"Uttanumtos","start":"2019-01-22T20:38:26.234"}}
data: {"updated":"2019-01-22T20:35:42.473","now":{"artist":"Hamradun","title":"Ein stutt og stokkut løta","start":"2019-01-22T20:35:40.614"},"next":{"artist":"Frændur","title":"Uttanumtos","start":"2019-01-22T20:38:26.234"}}
data: {"updated":"2019-01-22T20:38:19.440","now":{"artist":"Frændur","title":"Uttanumtos","start":"2019-01-22T20:38:17.833"},"next":{"artist":"Wolfgang","title":"Ice Cold","start":"2019-01-22T20:41:45.936"}}
data: {"updated":"2019-01-22T20:38:19.440","now":{"artist":"Frændur","title":"Uttanumtos","start":"2019-01-22T20:38:17.833"},"next":{"artist":"Wolfgang","title":"Ice Cold","start":"2019-01-22T20:41:45.936"}}
data: {"updated":"2019-01-22T20:38:19.440","now":{"artist":"Frændur","title":"Uttanumtos","start":"2019-01-22T20:38:17.833"},"next":{"artist":"Wolfgang","title":"Ice Cold","start":"2019-01-22T20:41:45.936"}}
data: {"updated":"2019-01-22T20:41:47.483","now":{"artist":"Wolfgang","title":"Ice Cold","start":"2019-01-22T20:41:45.668"},"next":{"artist":"Fróði Bjarnason","title":"Where My Home Is","start":"2019-01-22T20:44:46.528"}}
```

`kvf_stream_to_timeline` helper will turn the above stream into a list of `TimelineEntry` dataclasses:

```python
TimelineEntry(artist_name='Jasmin', song_title='Make Sense', duration=254, played_at=datetime.datetime(2019, 1, 22, 20, 27, 22, 318000))
TimelineEntry(artist_name='Teitur', song_title='I Want to Be Kind', duration=249, played_at=datetime.datetime(2019, 1, 22, 20, 31, 36, 113000))
TimelineEntry(artist_name='Hamradun', song_title='Ein stutt og stokkut løta', duration=165, played_at=datetime.datetime(2019, 1, 22, 20, 35, 40, 614000))
TimelineEntry(artist_name='Frændur', song_title='Uttanumtos', duration=208, played_at=datetime.datetime(2019, 1, 22, 20, 38, 17, 833000))
TimelineEntry(artist_name='Wolfgang', song_title='Ice Cold', duration=180, played_at=datetime.datetime(2019, 1, 22, 20, 41, 45, 668000))
```

`timeline_to_models` helper will give you a set of models with songs linking back to artists:

```
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
```

`models_to_graph_json` helper will then return [GraphJSON](https://github.com/jsongraph/json-graph-specification) representation of the timeline:

```json
{
 "nodes": [
  {
   "id": "5834d4db6",
   "caption": "Eiv\u00f8r P\u00e1lsd\u00f3ttir",
   "type": "MusicGroup"
  },
  {
   "id": "51e2d554b",
   "caption": "Enekk",
   "type": "MusicGroup"
  },
  {
   "id": "5705c4343",
   "caption": "Orka",
   "type": "MusicGroup"
  },
  {
   "id": "1d12586d0",
   "caption": "Elisabeth og Elinborg",
   "type": "MusicRecording"
  },
  {
   "id": "dccf0f42d",
   "caption": "Mannabarn",
   "type": "MusicRecording"
  },
  {
   "id": "51b04a795",
   "caption": "V\u00e1rsins lj\u00f3\u00f0",
   "type": "MusicRecording"
  },
  {
   "id": "308f8a2b4",
   "caption": "Slatur",
   "type": "MusicRecording"
  },
  {
   "id": "bef2f5fc9",
   "caption": "\u00d3dn",
   "type": "MusicRecording"
  },
  {
   "id": "b73add98e",
   "caption": "Hon leitar",
   "type": "MusicRecording"
  }
 ],
 "edges": [
  {
   "source": "1d12586d0",
   "target": "5834d4db6",
   "caption": "byArtist"
  },
  {
   "source": "dccf0f42d",
   "target": "5834d4db6",
   "caption": "byArtist"
  },
  {
   "source": "51b04a795",
   "target": "5834d4db6",
   "caption": "byArtist"
  },
  {
   "source": "308f8a2b4",
   "target": "51e2d554b",
   "caption": "byArtist"
  },
  {
   "source": "bef2f5fc9",
   "target": "51e2d554b",
   "caption": "byArtist"
  },
  {
   "source": "b73add98e",
   "target": "5705c4343",
   "caption": "byArtist"
  }
 ]
}
```
