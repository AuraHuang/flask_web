$('input[type="file"]').change(function(e){
    var fileName = e.target.files[0].name;
    $(e.target).siblings('.custom-file-label').text(fileName);
});