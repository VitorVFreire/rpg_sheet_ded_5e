$(document).ready(function() {
    $('#form').submit(function(e) {
        e.preventDefault();
        
        var nome_salvaguarda = $('#nome_salvaguarda').val();

        $.ajax({
            url: '/criar_salvaguarda',
            type: 'POST',
            data: {
                nome_salvaguarda: nome_salvaguarda,
            },
            success: function(response) {
                var result = response.result;
                $('#result-container').text('Resultado: ' + result);
            }
        });
    });
});