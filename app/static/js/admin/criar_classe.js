$(document).ready(function() {
    $('#form').submit(function(e) {
        e.preventDefault();
        
        var nome_classe = $('#nome_classe').val();

        $.ajax({
            url: '/criar_classe',
            type: 'POST',
            data: {
                nome_classe: nome_classe,
            },
            success: function(response) {
                var result = response.result;
                $('#result-container').text('Resultado: ' + result);
            }
        });
    });
});