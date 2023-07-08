$(document).ready(function() {
    $('#form').submit(function(e) {
        e.preventDefault();
        
        var nome_raca = $('#nome_raca').val();

        $.ajax({
            url: '/insert_raca',
            type: 'POST',
            data: {
                nome_raca: nome_raca,
            },
            success: function(response) {
                var result = response.result;
                $('#result-container').text('Resultado: ' + result);
            }
        });
    });
});