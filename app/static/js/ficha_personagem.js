const id_personagem = parseInt(document.querySelector('#id_personagem').value, 10);

const inputs_atributos = document.querySelectorAll('input[id^="atributo_"]');

inputs_atributos.forEach(input => {
  input.addEventListener('blur', function() {
    const id = input.id;
    const posicao = id.search('_');
    const atributo = id.substring(posicao + 1);

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
          atualizar_pericias();
        }
      }
    });    
  });
});

const inputs_salvaguardas= document.querySelectorAll('input[id^="salvaguarda_"]');

inputs_salvaguardas.forEach(input => {
  input.addEventListener('change', function() {
    const id = input.id;
    const posicao = id.search('_');
    const salvaguarda = id.substring(posicao + 1);
    let tipo = 'adicionar';
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

const inputs_status_base = document.querySelectorAll('input[id^="status_base_"]');

inputs_status_base.forEach(input => {
  input.addEventListener('blur', function() {
    const id = input.id;
    const posicao=id.search('e_')
    const status_base = id.substring(posicao+2);

    $.ajax({
      url: `/status_base/${id_personagem}`,
      type: 'POST',
      data: {
          chave: status_base,
          valor: this.value,
      },
      success: function(response) {
        var result = response.result;
        $('#result-container').text('Resultado: ' + result);
      }    
    });
  });
});

const inputs_pericias= document.querySelectorAll('input[id^="check_pericia_"]');

inputs_pericias.forEach(input => {
  input.addEventListener('change', function() {
    const id = input.id;
    const posicao=id.search('a_')
    const pericia = id.substring(posicao+2);
    let tipo = 'adicionar';
    if (!this.checked) {
      tipo = 'remover';
    }
    $.ajax({
      url: `/nova_pericia/${id_personagem}`,
      type: 'POST',
      data: {
        chave: pericia,
        tipo: tipo,
      },
      success: function(response) {
        var result = response.result;
        $('#result-container').text('Resultado: ' + result);
        $(`#pericia_${pericia}`).text(response.pericia);
      }
    });
  });
});


function capitalizeFirstLetter(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

function atualizar_pericias() {
  $.ajax({
    url: `/pericias/${id_personagem}`,
    type: 'POST',
    success: function(response) {
      for (const [key, value] of Object.entries(response)) {
        $(`#pericia_${key}`).text(value);
      }
    }
  });
}