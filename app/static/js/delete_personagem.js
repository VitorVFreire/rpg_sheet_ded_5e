$(document).ready(function() {
    $('[id^="delete_"]').click(function(e) {
        e.preventDefault();
        
        // Obtenha o id_personagem do atributo data
        var id_personagem = $(this).data('id-personagem');
        console.log(id_personagem)
        $.ajax({
            url: '/personagem/' + id_personagem,
            type: 'DELETE',
            success: function(response) {
                var result = response.result;
                $('#result-container').text('Resultado: ' + result);
            }
        });
    });
});
