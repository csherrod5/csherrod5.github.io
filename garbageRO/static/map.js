var onRoute = [];
var lat = [];
var lng = [];

function initHomeMap() {
	var directionsService = new google.maps.DirectionsService;
  var directionsDisplay = new google.maps.DirectionsRenderer;
	var map = new google.maps.Map(document.getElementById('homeMap'), {
		center: {lat: 30.612725, lng: -96.339578},
		zoom: 15
	});
	directionsDisplay.setMap(map);

	loadWaypoints();
  calculateAndDisplayRoute(directionsService, directionsDisplay);
}

function initMarkerMap(oldLat, oldLng) {
	var markerMap = new google.maps.Map(document.getElementById('markerMap'), {
		center: {lat: 30.612725, lng: -96.339578},
		zoom: 18
	});

	var myMarker = new google.maps.Marker({
		position: new google.maps.LatLng(oldLat, oldLng),
		draggable: true
	});

	google.maps.event.addListener(myMarker, 'dragend', function(evt){
		document.getElementById('markerLat').innerHTML = evt.latLng.lat().toFixed(6);
		document.getElementById('markerLng').innerHTML = evt.latLng.lng().toFixed(6);
	});

	google.maps.event.addListener(myMarker, 'dragstart', function(evt){

	});

	markerMap.setCenter(myMarker.position);
	myMarker.setMap(markerMap);
}

function updateDumpsterLocation() {
	var markerLat = document.getElementById('markerLat').innerHTML;
	var markerLng = document.getElementById('markerLng').innerHTML;

	var string = location + "/" + markerLat + "/" + markerLng;
	location.href = string;
}

function loadWaypoints() {
	$("form").each(function() {
		onRoute.push(this.added.value);
		lat.push(this.lat.value);
		lng.push(this.lng.value);
	});
}

function calculateAndDisplayRoute(directionsService, directionsDisplay) {
	var waypts = [];
	for (var i = 0; i < onRoute.length; i++) {
		if (onRoute[i] == 'True') {
			waypts.push({
				location: new google.maps.LatLng(lat[i], lng[i]),
				stopover: true
			});
		}
	}

	if (waypts.length > 0) {
		directionsService.route({
			origin: 'College Station Municipal Court',
			destination: 'College Station Municipal Court',
			waypoints: waypts,
			optimizeWaypoints: true,
			travelMode: 'DRIVING'
		}, function(response, status) {
			if (status === 'OK') {
				directionsDisplay.setDirections(response);
				//var route = response.routes[0];
				//var summaryPanel = document.getElementById('directions-panel');
				//summaryPanel.innerHTML = '';
				// For each route, display summary information.
				//for (var i = 0; i < route.legs.length; i++) {
					//var routeSegment = i + 1;
					//summaryPanel.innerHTML += '<b>Route Segment: ' + routeSegment +
							//'</b><br>';
					//summaryPanel.innerHTML += route.legs[i].start_address + ' to ';
					//summaryPanel.innerHTML += route.legs[i].end_address + '<br>';
					//summaryPanel.innerHTML += route.legs[i].distance.text + '<br><br>';
				//}
			} else {
				window.alert('Directions request failed due to ' + status);
			}
		});
	}
}
