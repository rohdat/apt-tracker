var infowindow = null;
function initMap() {
	// Will get lat and lon based on written address
	var addr = 'google hq';
	var mapDiv = 'map';
	idmap = 'map';
	mapDiv = document.getElementById(idmap);
	mapDiv.style.width='250px';
	mapDiv.style.height='250px';
	mapDiv.style.backgroundColor='#CCC';
	var markers = [];
	var bound = new google.maps.LatLngBounds();
	$.getJSON('/main/JSON',function(json) {
		json.Apt.forEach(function (a){
			// console.log(a.id);
			addr = a.addr;
			// console.log(addr);
			geocodeMe(addr, function (latlon){
				bound.extend(latlon);
				// console.log("During for loop:");
				// console.log(bound.getCenter().toJSON());
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
				var eid = 'row-'+a.id;
				var row_active = document.getElementById(eid);
				console.log(row_active);
				marker.addListener('mouseover', function () {
					if (!row_active.className.match(/.*success.*/)) {
						row_active.className = "success";
					}
				})
				marker.addListener('mouseout', function () {
					console.log("Hover detected row-"+a.id);
					if (row_active.className.match(/.*success.*/)) {
						row_active.className = "";
					}
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
	// console.log(bound.getCenter().toJSON());
	
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

var asc = 1;
window.onload = function () {
	apt_table = document.getElementById('apt_table');
	console.log("Window finished loading")
}

function sortTable(col){
	var rows = apt_table.rows,
	rlen = rows.length
	arr = new Array();
	var i, j, cells, clen;
    for (i = 0; i < rlen; i++) {
        cells = rows[i].cells;
        clen = cells.length;
        arr[i] = new Array();
        for (j = 0; j < clen; j++) {
            arr[i][j] = cells[j].innerHTML;
        }
    }
    console.log("Sorting...")
	arr.sort(function (a, b) {
		return (a[col] == b[col]) ? 0 : ((a[col] > b[col]) ? asc : -1 * asc);
	});
	asc = -1*asc;
	for(i = 0; i < rlen; i++){
        arr[i] = "<td>"+arr[i].join("</td><td>")+"</td>";
    }
    apt_table.innerHTML = "<tr>"+arr.join("</tr><tr>")+"</tr>";

}
