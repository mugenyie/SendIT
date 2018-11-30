function initMap() {
    var directionsService = new google.maps.DirectionsService;
    var directionsDisplay = new google.maps.DirectionsRenderer({
        draggable: true,
        map: map,
        panel: document.getElementById('right-panel')
        });
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 7,
        center: {lat: 1.3733, lng: 32.2903}
    });
    directionsDisplay.setMap(map);
    directionsDisplay.addListener('directions_changed', function() {
        computeTotalDistance(directionsDisplay.getDirections());
        computeTotalDuration(directionsDisplay.getDirections())
        });

    var onChangeHandler = function() {
        calculateAndDisplayRoute(directionsService, directionsDisplay);
    };

    var pickup = document.getElementById('start');
    var destination = document.getElementById('end');
    new google.maps.places.Autocomplete(pickup);
    new google.maps.places.Autocomplete(destination);
    pickup.addEventListener('change', onChangeHandler);
    destination.addEventListener('change', onChangeHandler);
}

function calculateAndDisplayRoute(directionsService, directionsDisplay) {
    directionsService.route({
        origin: document.getElementById('start').value,
        destination: document.getElementById('end').value,
        travelMode: 'DRIVING'
    }, function(response, status) {
        if (status === 'OK') {
            directionsDisplay.setDirections(response);
        } 
    });
}

function computeTotalDistance(result) {
    var total = 0;
    var myroute = result.routes[0];
    for (var i = 0; i < myroute.legs.length; i++) {
        total += myroute.legs[i].distance.value;
    }
    total = total / 1000;
    document.getElementById('distance').innerHTML = total + ' km';
}

function computeTotalDuration(result) {
    var total = 0;
    var myroute = result.routes[0];
    for (var i = 0; i < myroute.legs.length; i++) {
        total += myroute.legs[i].duration.value;
    }
    total = total / 60;
    document.getElementById('duration').innerHTML = Math.ceil(total) + ' mins';
}

function initializeMapsAutocomplete() {
  let autocomplete = new google.maps.places.Autocomplete(
      /** @type {HTMLInputElement} */(document.getElementById('autocomplete')),
      { types: ['geocode'] });
  google.maps.event.addListener(autocomplete, 'place_changed', function() {
  });
}