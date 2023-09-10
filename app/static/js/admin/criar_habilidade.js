$(document).ready(function() {
    $('#form').submit(function(e) {
        e.preventDefault();
        
        var nome_habilidade = $('#nome_habilidade').val();
        var nome_atributo = $('#nome_atributo').val();
        var lados_dados = $('#lados_dados').val();
        var link_detalhes = $('#link_detalhes').val();
        var tipo_dano = $('#tipo_dano').val();
        var qtd_dados = $('#qtd_dados').val();
        var nivel_habilidade = $('#nivel_habilidade').val();
        var adicional_por_nivel = $('#adicional_por_nivel').val();

        $.ajax({
            url: '/criar_habilidade',
            type: 'POST',
            data: {
                nome_habilidade: nome_habilidade,
                nome_atributo: nome_atributo,
                lados_dados: lados_dados,
                link_detalhes: link_detalhes,
                tipo_dano: tipo_dano,
                qtd_dados: qtd_dados,
                nivel_habilidade: nivel_habilidade,
                adicional_por_nivel: adicional_por_nivel
            },
            success: function(response) {
                var result = response.result;
                $('#result-container').text('Resultado: ' + result);
            }
        });
    });
});