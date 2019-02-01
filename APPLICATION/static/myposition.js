var autocomplete
var lat
var lng
var value = 10
var table

$(document).ready(function() {
    table = $('#meta').DataTable( {
        bAutoWidth: false,
        "paging": false,
        data: dataSet,
        columns: [
            { title: "Nom" },
            { title: "Prénom" },
            { title: "Ville" },
            { title: "Latitude" },
            { title: "Longitude" },
            { title: "ID"}
        ]
    });

    table.columns([3, 4, 5]).visible(false);

    $('#meta tbody').on('click', 'tr', function () {
        var data_candidat = table.row(this).data(); // get all data from clicked row
        document.location.href = '/candidat/' + data_candidat[5];
    });
});

autocomplete = new google.maps.places.Autocomplete(document.getElementById('autocomplete'), { types: ['geocode'] });
google.maps.event.addListener(autocomplete, 'place_changed', function() {
    var place = autocomplete.getPlace();
    lat = place.geometry.location.lat()
    lng = place.geometry.location.lng();
})

function deg2rad(deg) {
    return deg * Math.PI / 180
}

function distance(lat1, lon1, lat2, lon2) {
  var R = 6371; // Radius of the earth in km
  var dLat = deg2rad(lat2 - lat1); // degree to rad
  var dLon = deg2rad(lon2 - lon1);
  var a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
    Math.sin(dLon / 2) * Math.sin(dLon / 2);

  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  var d = R * c; // Distance in km
  return d;
}

function run(dataSet) {
    var tab = []
    tmp = Array.from(dataSet)
    value = document.getElementById("range").value;
    for (elem in tmp) {
        current = dataSet[elem]
        latA = parseFloat(current[3])
        lngA = parseFloat(current[4])
        lat = parseFloat(lat)
        lng = parseFloat(lng)
        dist = distance(latA, lngA, lat, lng)
        // check if dist(km) <= range value (km)
        // then push in new tab elem in range
        if (dist <= parseFloat(value)) {
            index = tmp.indexOf(elem)
            tab.push(tmp[elem])
        }
    }
    table.clear();
    table.rows.add(tab);
    table.draw();
}
