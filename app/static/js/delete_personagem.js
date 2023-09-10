$(document).ready(function() {
    $('[id^="delete_"]').click(function(e) {
        e.preventDefault();
        
        // Obtenha o id_personagem do atributo data
        var id_personagem = $(this).data('id-personagem');

        $.ajax({
            url: '/personagem/' + id_personagem,
            type: 'DELETE',
            success: function(response) {
                window.location.reload(true);
            }
        });
    });
});
