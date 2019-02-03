# now-playing-graph
Processes "now playing" data from [internet radio player](https://kvf.fo/popout/widget) for [Faroese Útvarp](https://kvf.fo/forsida/english).

## Why?

As a fan of all Faroese aspects, I'm curius to know:

* which artist is most frequently played?
* which artist songs are played for the the longest time?
* is some artist typically followed by another one?

## Collecting the data

The following bash script is run every minute to scripe "now playing" data from kvf.fo site:

```bash
curl -s --max-time 3 'https://netvarp.kringvarp.fo:80/sse' 2>&1  | grep data >> ~/kvf.log
```

Here's the snippet of collected data:

```json
data: {"updated":"2019-02-01T19:40:20.322","now":{"artist":"Hamradun","title":"Sinklars vísa","start":"2019-02-01T19:40:18.839"},"next":{"artist":"Anton Liljedahl","title":"Vónarsjón","start":"2019-02-01T19:48:35.668"}}
data: {"updated":"2019-02-01T19:40:20.322","now":{"artist":"Hamradun","title":"Sinklars vísa","start":"2019-02-01T19:40:18.839"},"next":{"artist":"Anton Liljedahl","title":"Vónarsjón","start":"2019-02-01T19:48:35.668"}}
data: {"updated":"2019-02-01T19:48:36.119","now":{"artist":"Anton Liljedahl","title":"Vónarsjón","start":"2019-02-01T19:48:34.228"},"next":{"artist":"Evi Tausen","title":"Neon Moon","start":"2019-02-01T19:52:56.924"}}
data: {"updated":"2019-02-01T19:48:36.119","now":{"artist":"Anton Liljedahl","title":"Vónarsjón","start":"2019-02-01T19:48:34.228"},"next":{"artist":"Evi Tausen","title":"Neon Moon","start":"2019-02-01T19:52:56.924"}}
data: {"updated":"2019-02-01T19:48:36.119","now":{"artist":"Anton Liljedahl","title":"Vónarsjón","start":"2019-02-01T19:48:34.228"},"next":{"artist":"Evi Tausen","title":"Neon Moon","start":"2019-02-01T19:52:56.924"}}
data: {"updated":"2019-02-01T19:48:36.119","now":{"artist":"Anton Liljedahl","title":"Vónarsjón","start":"2019-02-01T19:48:34.228"},"next":{"artist":"Evi Tausen","title":"Neon Moon","start":"2019-02-01T19:52:56.924"}}
data: {"updated":"2019-02-01T19:52:49.352","now":{"artist":"Evi Tausen","title":"Neon Moon","start":"2019-02-01T19:52:47.664"},"next":{"artist":"Arnold Ludvig Sextet","title":"Miles Beyond","start":"2019-02-01T19:56:42.840"}}
```
