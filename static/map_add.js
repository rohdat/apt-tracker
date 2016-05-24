function initMap() {
	// Will get lat and lon based on written address
	var addr = 'google hq';
	var mapDiv = 'map';
	$.getJSON('/main/JSON',function(json) {
		json.Apt.forEach(function (a){
			// console.log(a.id);
			addr = a.addr;
			console.log(addr);
			idmap = 'map-'+a.id;
			mapDiv = document.getElementById(idmap);
			mapDiv.style.width='250px';
			mapDiv.style.height='250px';
			mapDiv.style.backgroundColor='#CCC';
			geocodeMe(addr, mapDiv, function (latlon, mapDiv){
				var map = new google.maps.Map(mapDiv, {
					// center: {lat:44.54, lng:-78.56},
					center:latlon,
					zoom:14
				});
				var marker = new google.maps.Marker ({
					map:map,
					position:latlon
				});
			})
		})
	})
	
}

function geocodeMe (addr, mapDiv, callback) {
	geocoder = new google.maps.Geocoder();
	geocoder.geocode( { 'address': addr }, function (results, status) {
	if (status == google.maps.GeocoderStatus.OK) {
		latlon = new google.maps.LatLng(results[0].geometry.location.lat(), results[0].geometry.location.lng());
		if (typeof callback == 'function') {
			callback(latlon, mapDiv);
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