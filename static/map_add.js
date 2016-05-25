var infowindow = null;
function initMap() {
	// Will get lat and lon based on written address
	var addr = 'google hq';
	var mapDiv = 'map';
	idmap = 'map';
	mapDiv = document.getElementById(idmap);
	mapDiv.style.width='1000px';
	mapDiv.style.height='250px';
	mapDiv.style.backgroundColor='#CCC';
	var markers = [];
	var bound = new google.maps.LatLngBounds();
	$.getJSON('/main/JSON',function(json) {
		json.Apt.forEach(function (a){
			// console.log(a.id);
			addr = a.addr;
			console.log(addr);
			geocodeMe(addr, function (latlon){
				bound.extend(latlon);
				console.log("During for loop:");
				console.log(bound.getCenter().toJSON());
				var contentString = getContent(a);
				var marker = new google.maps.Marker ({
					map:map,
					position:latlon
				});

				marker.addListener('click',function() {
					if (infowindow){
						infowindow.close();
					}
					infowindow = new google.maps.InfoWindow({
						content: contentString
					});

					infowindow.open(map,marker);
				})
				updateMap();
			})
		})
	})
	var mapCenter = bound.getCenter();
	var map = new google.maps.Map(mapDiv, {
		center: mapCenter,
		zoom:14
	});
	console.log(bound.getCenter().toJSON());
	
	var updateMap = function (){
		mapCenter = bound.getCenter();
		map.setCenter(mapCenter);
		map.fitBounds(bound);
	};
	var getContent = function (a) {
		return "<div>Rent: $"+a.rent+"</div><hr><div>Status: "+a.link;
	}
	
}

function geocodeMe (addr, callback) {
	geocoder = new google.maps.Geocoder();
	geocoder.geocode( { 'address': addr }, function (results, status) {
	if (status == google.maps.GeocoderStatus.OK) {
		latlon = new google.maps.LatLng(results[0].geometry.location.lat(), results[0].geometry.location.lng());
		if (typeof callback == 'function') {
			callback(latlon);
		}
		// console.log(results[0].geometry.location.lat())
	} else {
		throw ("no results found for: "+addr);
	}
	});
}

function deleteConfirm(id) {
	if (confirm("Delete for sure?") == true) {
		window.location.replace("/apts/"+id+"/delete");
	} else {
		// window.location.replace("main");
	}
}