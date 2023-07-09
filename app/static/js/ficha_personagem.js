const id_personagem = parseInt(document.querySelector('#id_personagem').value,10)

const inputs_atributos = document.querySelectorAll('input[id^="atributo_"]');

inputs_atributos.forEach(input => {
  input.addEventListener('blur', function() {
    const id = input.id;
    const posicao=id.search('_')
    const atributo = id.substring(posicao+1);

    $.ajax({
      url: `/atributos/${id_personagem}`,
      type: 'POST',
      data: {
          chave: atributo,
          valor: this.value,
      },
      success: function(response) {
        var result = response.result;
        $('#result-container').text('Resultado: ' + result);
        if ($(`#bonus_${atributo}`)) {
          $(`#bonus_${atributo}`).text(response.bonus);
        }
      }    
    });
  });
});