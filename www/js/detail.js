  var geojson;

  var defaultStyle = {'weight': '0', fillColor: '#381f5e', fillOpacity: '1'};

  L.mapbox.accessToken = 'pk.eyJ1IjoiZHVuZXIiLCJhIjoiaWkwMnJIZyJ9.2zMvIebbUOk9C5R2itT7Dg';
  var map = L.mapbox.map('small-map', 'duner.m3npglde', {
    minZoom: 15,
    maxBounds: [
      [42.07095890994855, -87.65922546386719],
      [42.039094188385945, -87.69158363342285]
    ],
    scrollWheelZoom: false
  }).setView([42.05504447993239,-87.6753830909729], 16);


  function parse_map_data(data){
    $.each(data, function(key, val){
        geojson = new L.GeoJSON(val, {
          style: function(feature) {
          return defaultStyle;
        }
      }).addTo(map);
      var bounds = geojson.getBounds();
      map.setView(bounds.getCenter(), 17);
    });
}

$(document).ready(function() {

  $(".rslides").responsiveSlides();
   $.ajax({
    url: dorm_url,
    async: true,
    dataType: 'jsonp',
    jsonp: false,
    jsonpCallback:'myCallback',
    success:function(data) {
        parse_map_data(data);
    }
  });

  $('#video-tab').click(function() {
    $('#embed-container').append('<iframe src="' + dorm_video + '" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>');
    $('#media-container img').css('display', 'none');
    $('#video-tab').css('background', '#381F5E');
    $('#photo-tab').css('background', '#c3bccf');
    $('#embed-container').css('display','block');
  });

  $('#photo-tab').click(function() {
    $('#embed-container iframe').remove();
    $('#embed-container').hide();
    $('#media-container img').css('display', 'block');
    $('#photo-tab').css('background', '#381F5E');
    $('#video-tab').css('background', '#c3bccf');
  });
});
