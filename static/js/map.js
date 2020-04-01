function initMap() {
    var shipping_status = $('#shipping_status');

    var map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 50.830149, lng: 4.385636 },
        zoom: 15
    });
    var input = document.getElementById('pac-input');
    var latitude = document.getElementById('latitude');
    var longitude = document.getElementById('longitude');


    var autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.bindTo('bounds', map);
    autocomplete.setFields(
        ['address_components', 'geometry', 'icon', 'name']);


    var marker = new google.maps.Marker({
        map: map,
        draggable: true,
        position: { lat: 50.830149, lng: 4.385636 },
        anchorPoint: new google.maps.Point(0, -29)
    });

marker.addListener('drag', function (event) {
    latitude.value = this.getPosition().lat().toString();
    longitude.value = this.getPosition().lng().toString();
    var dis = getDistanceFromLatLonInKm(this.getPosition().lat(), this.getPosition().lng()).toFixed(2);
    if (dis > 2.0) shipping_status.html('You are ' + dis + ' km away from us, Shipping Charge 5 €')
    else shipping_status.html('You are ' + dis + ' km away from us, Shipping Charge 0 €');
});


autocomplete.addListener('place_changed', function () {
    var place = autocomplete.getPlace();

    if (!place.geometry) {
        $.alert({
            title: "Ooops !!!",
            content: "No details available for input: '" + place.name + "'",
            theme: "bootstrap",
        });
        return;
    }

    if (place.geometry.viewport) {
        map.fitBounds(place.geometry.viewport);
        map.setZoom(15);
    } else {
        map.setCenter(place.geometry.location);
        map.setZoom(15);
    }

    marker.setPosition(place.geometry.location);
    latitude.value = place.geometry.location.lat().toString();
    longitude.value = place.geometry.location.lng().toString();
    var dis = getDistanceFromLatLonInKm(place.geometry.location.lat(), place.geometry.location.lng()).toFixed(2);
    if (dis > 2.0) shipping_status.html('You are ' + dis + ' km away from us, Shipping Charge 5 €')
    else shipping_status.html('You are ' + dis + ' km away from us, Shipping Charge 0 €');

    if (place.address_components) {
        address = [
            (place.address_components[0] && place.address_components[0].short_name || ''),
            (place.address_components[1] && place.address_components[1].short_name || ''),
            (place.address_components[2] && place.address_components[2].short_name || '')
        ].join(' ');
    }

});



}



//google.maps.event.addDomListener(window, "load", initMap);


function getDistanceFromLatLonInKm(lat2, lon2) {
    var lat1 = 50.830149;
    var lon1 = 4.385636;
    var R = 6371; // Radius of the earth in km
    var dLat = deg2rad(lat2 - lat1);  // deg2rad below
    var dLon = deg2rad(lon2 - lon1);
    var a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    var d = R * c; // Distance in km
    return d;
}

function deg2rad(deg) {
    return deg * (Math.PI / 180)
}
