let send_ajax = (url, data, type, success = null, error = null) => {


    // if (type == 'POST' || type == 'post') {

    // }

    $.ajax({
        url: url,
        type: type,
        data: data,
        datatype: "json",
        success: success,
        error: error
    });
    // return false;
};


function initMap() {

    map = new google.maps.Map(document.getElementById('map'), {
      zoom: 3,
      center: {lat: -28.024, lng: 140.887}
    });
    
    
    
    // Create an array of alphabetical characters used to label the markers.
    var labels = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    
    
    // Add some markers to the map.
    // Note: The code uses the JavaScript Array.prototype.map() method to
    // create an array of markers based on a given "locations" array.
    // The map() method here has nothing to do with the Google Maps API.
    
    // var markers = locations.map(function(location, i) {
    //   return new google.maps.Marker({
    //     position: location,
    //     label: labels[i % labels.length]
    //   });
    // });
    
    
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
        let coords = e.latLng.toString().replace(/[{()}]/g, '').split(',');
        console.log(coords[1]);
        $('#id_lat').val(+coords[0]);
        $('#id_lng').val(+coords[1])

        currMarker.setMap(null);
        currMarker = new google.maps.Marker({
                position: e.latLng,
                map: map
      });
        // console.log(e.latLng);
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
        
    $('#btn').on('click', function(e) {
        
        console.log(currMarker.position);
        
        send_ajax(document.location.pathname, {'coords': String(currMarker.position)}, 'post')
        return false;
    })
    
    }

let addCurrnetMeetMarker = (position) => {
    map.setCenter(position);
    currMarker = new google.maps.Marker({
        position: position,
        map: map
    });
};