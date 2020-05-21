var map = null;
var currMarker = null;

function initMap() {

    map = new google.maps.Map(document.getElementById('map'), {
      zoom: 3,
      center: {lat: -28.024, lng: 140.887}
    });

    
    
    // var marker = new google.maps.Marker({
    //                 position: {lat: 42.3601, lng: -71.0589},
    //                 map: map
    //             })
    
                // map.addListener('center_changed', function() {
        // window.setTimeout(function() {
        //   map.panTo(marker.getPosition());
        // }, 3000);
    //   });
    
    map.addListener('click', function(e) {
        // alert(e.latLng);
        
        currMarker.setMap(null);
        currMarker = new google.maps.Marker({
                position: e.latLng,
                map: map
      });
      $('input[name ="lat"]').val(currMarker.getPosition()['lat']())
      $('input[name ="lng"]').val(currMarker.getPosition()['lng']())
    })
    
    
    // marker.addListener('click', function() {
        // map.setZoom(8);
        // map.setCenter(marker.getPosition());
        // map.panTo(marker.getPosition());
    //   });
    // Add a marker clusterer to manage the markers.
    // var markerCluster = new MarkerClusterer(map, markers,
    //     {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
    
    // var infowindow = new google.maps.InfoWindow({
    //           content: '<h3>Say WHaaaa</h3?'
    //         });
    
    //         marker.addListener('click', function() {
    //             // alert(1);
    //           infowindow.open(marker.get('map'), marker);
    //         });
    
            
    // map.addListener('click', function(e) {
            
    //             currMarker = new google.maps.Marker({
    //             position: {lat: 42.3601, lng: -71.0589},
    //             map: map
    //         })
    //   });

    
    }

    let addCurrnetMeetMarker = (position) => {
        map.setCenter(position);
        currMarker = new google.maps.Marker({
            position: position,
            map: map
        });
    };