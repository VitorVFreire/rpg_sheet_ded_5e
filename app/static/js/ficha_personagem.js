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
          $(`#resistencia_${atributo}`).text(response.resistencia);
        }
      }    
    });
  });
});

const inputs_salvaguardas= document.querySelectorAll('input[id^="salvaguarda_"]');

inputs_salvaguardas.forEach(input => {
  input.addEventListener('change', function() {
    console.log('AQUIIIIIII')
    const id = input.id;
    const posicao = id.search('_');
    const salvaguarda = id.substring(posicao + 1);
    let tipo = 'adicionar';
    console.log(salvaguarda);
    if (!this.checked) {
      tipo = 'remover';
    }
    $.ajax({
      url: `/salvaguarda/${id_personagem}`,
      type: 'POST',
      data: {
        chave: salvaguarda,
        tipo: tipo,
      },
      success: function(response) {
        var result = response.result;
        $('#result-container').text('Resultado: ' + result);
        $(`#resistencia_${salvaguarda}`).text(response.resistencia);
      }
    });
  });
});
