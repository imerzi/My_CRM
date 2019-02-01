$(document).ready(function() {
    var table = $('#meta').DataTable( {
        bAutoWidth: false,
        "paging": false,
        data: dataSet,
        columns: [
            { title: "Nom" },
            { title: "Prénom" },
            { title: "Consultant" },
            { title: "GRH"},
            { title: "Âge"},
            { title: "Genre"},
            { title: "Téléphone"},
            { title: "Date d'archive"},
            { title: "Date de recrutement"},
            { title: "Ville"},
            { title: "Code postal"},
            { title: "Email"},
            { title: "Dernier diplôme"},
            { title: "Poste actuel"},
            { title: "Employé actuel"},
            { title: "Spécialité"},
            { title: "Formation"},
            { title: "Réclamation salariale"},
            { title: "Logiciel"},
            { title: "extension"},
            { title: "Fichier"},
            { title: "Longitude"},
            { title: "Latitiude"},
            { title: "Skype"}
        ]
    } );

        table.columns( [3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18, 19, 20, 21, 22, 23] ).visible( false );
        table.columns( [2,9,13] ).visible( true );

        $('a.toggle-vis').on( 'click', function (e) {
        e.preventDefault();

        // Get the column API object
        var column = table.column( $(this).attr('data-column') );

        // Toggle the visibility
        column.visible( ! column.visible() );

        if ($(this).attr('class') == "btn btn-default toggle-vis") {
            $(this).removeClass("btn btn-default toggle-vis")
            $(this).addClass("btn btn-primary toggle-vis")
        }
        else {
            $(this).removeClass("btn btn-primary toggle-vis")
            $(this).addClass("btn btn-default toggle-vis")
        }

        table.columns.adjust().draw();

    });

     $('#meta tbody').on( 'click', 'tr', function () {
        var data_candidat = table.row(this).data(); // get all data from clicked row
        document.location.href = '/candidat/'+data_candidat[24];

    });
} );