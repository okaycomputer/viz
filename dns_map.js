var map = new Datamap({
  element: document.getElementById('container'),
  scope: 'world',
  geographyConfig: {
    popupOnHover: false,
    highlightOnHover: false
  },
  fills : {
    '1': '#1f77b4',
    '2': '#9467bd',
    '3': '#ff7f0e',
    '4': '#2ca02c',
    '5': '#e377c2',
    defaultFill: '#EDDC4E'
  },
  data: {}
});

map.bubbles(data, {
  popupTemplate: function (geo, data) { 
    return ['<div class="hoverinfo">' +  data.name + '<br/>' +  data.timestamp + '<br/>Client ID: ' + data.client_id + '<br/>Qtype: ' +  data.qtype + '</br>' + 'RCode' + data.rcode + 'Country: ' + data.country + '</div>'].join('');
  }
});