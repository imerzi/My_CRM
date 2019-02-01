$(document).ready(function() {

    var table = $('#meta').DataTable({
        bAutoWidth: false,
        "paging": false,
        data: dataSet,
        columns: [
            { title: "Nom companie" },
            { title: "Nom contact" },
            { title: "Prénom contact" },
            { title: "Ville contact"},
            { title: "Code postal contact"}
        ]
    });

    $('#city').on( 'keyup', function () {
    table
        .columns( 3 )
        .search( this.value )
        .draw();
    });

    $('#zipcode').on( 'keyup', function () {
    table
        .columns( 4 )
        .search( this.value )
        .draw();
    });

    $('#meta tbody').on( 'click', 'tr', function () {
        var data_client = table.row(this).data(); // get all data from clicked row
        document.location.href = '/client/'+data_client[5];
    });

});