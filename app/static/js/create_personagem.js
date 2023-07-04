
$(document).ready(function() {
    $('#form').submit(function(e) {
        e.preventDefault();
        
        var id_raca = $('#id_raca').val();
        var nome_personagem = $('#nome_personagem').val();

        $.ajax({
            url: 'http://127.0.0.1:5000/insert_personagem',
            type: 'POST',
            data: {
                id_raca: id_raca,
                nome_personagem: nome_personagem,
            },
            success: function(response) {
                var result = response.result;
                $('#result-container').text('Resultado: ' + result);
            }
        });
    });
});