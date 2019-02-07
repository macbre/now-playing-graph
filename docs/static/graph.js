(function() {
    /**
     * @see http://graphalchemist.github.io/Alchemy/#/docs
     */
    var config = {
      backgroundColor: 'transparent',
      divSelector: '#graph',

      linkDistancefn: function(node) {
        // console.log(node);
        return Math.max(node.source.radius, node.target.radius) * 1.75;
      },

      dataSource: graph,

      edgeCaption: 'caption',
      edgeStyle: {
          "all": {
            "width": 4,
            "color": "#ccc",
            "opacity": 0.25,
            "directed": true,
            "curved": true,
            "selected": {
              "opacity": 1
            },
            "highlighted": {
              "opacity": 1
            },
            "hidden": {
              "opacity": 0
            }
          }
        },

      "nodeTypes": {"type": ["MusicRecording", "MusicGroup"]},
      nodeCaptionsOnByDefault: true,
      "nodeStyle": {
        "all": {
            radius: function(node) {
                var props = node._properties;
                // console.log(props);
                var multiplier = (props.type === 'MusicGroup' ? 3 : 0.07);
                return multiplier * props.size;
            },
            opacity: 0.8,
        },
        "MusicRecording": {
            color: "#3c91d044", // blue
            borderColor: "#eee"
        },
        "MusicGroup":{
            color: "#ef5c5e44", // red
            borderColor: "#eee"
        }
      }
    };

    var alchemy = new Alchemy(config);

    console.log(alchemy);

    if (typeof window.onGraphReady === 'function') {
        onGraphReady(alchemy, graph);
    }
})();
