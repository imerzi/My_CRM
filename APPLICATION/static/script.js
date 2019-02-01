document.addEventListener("DOMContentLoaded", function() {
    var e = document.getElementsByClassName("custom-file-input")

    for (var i = 0; i < e.length; i++) {
        document.getElementById(e[i].id).addEventListener('change',function(){
                //get the file name
                var fileName = $(this).val();
                fileName = fileName.replace(/^.*\\/, "");

                //replace the "Choose a file" label
                $(this).next('.custom-file-label').html(fileName);
            })
    }
});

$(".js-example-basic-hide-search").select2({
  minimumResultsForSearch: Infinity
});

$('.select2').select2()

$(document).ready(function(){
  $(":input").inputmask();
});
