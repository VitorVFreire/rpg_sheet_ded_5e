$(document).ready(function() {
    $('#form').submit(function(e) {
        e.preventDefault();
        
        var nome_pericia = $('#nome_pericia').val();
        var status_uso = $('#status_uso').val();

        $.ajax({
            url: '/criar_pericia',
            type: 'POST',
            data: {
                nome_pericia: nome_pericia,
                status_uso: status_uso,
            },
            success: function(response) {
                var result = response.result;
                $('#result-container').text('Resultado: ' + result);
            }
        });
    });
});