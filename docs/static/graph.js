(function() {
    var NODE_MAX_RADIUS = 20;

    /**
     * @see http://graphalchemist.github.io/Alchemy/#/docs
     */
    var config = {
      backgroundColor: 'transparent',
      divSelector: '#graph',
      initialScale: 0.5,

      linkDistancefn: function(node) {
        // console.log(node);
        return Math.min(node.source.radius, node.target.radius, NODE_MAX_RADIUS) * 3.5;
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
        curvedEdges: false,

      "nodeTypes": {"type": ["MusicRecording", "MusicGroup"]},
      nodeCaptionsOnByDefault: false,
      "nodeStyle": {
        "all": {
            radius: function(node) {
                var props = node._properties,
                    isBig = (props.type === 'MusicGroup'),
                    multiplier = (isBig ? 3 : 0.05),
                    radius = Math.min(multiplier * props.size, NODE_MAX_RADIUS) * (isBig ? 2 : 1);

                console.log([props.type, props.size, radius]);
                return radius;
            },
            opacity: 0.8,
        },
        "MusicRecording": {
            color: "#3c91d044", // blue
            borderColor: "#eee",
            "hidden": {
                "color": "none",
                "borderColor": "none"
            }
        },
        "MusicGroup":{
            color: "#ef5c5e44", // red
            borderColor: "#eee"
        }
        },
        "nodeMouseOver": function(node) {
            return 'foo';
        }
    };

    var alchemy = new Alchemy(config);

    console.log(alchemy);

    if (typeof window.onGraphReady === 'function') {
        onGraphReady(alchemy, graph);
    }
})();
