const id_personagem = parseInt(document.querySelector('#id_personagem').value, 10);


//MUDANÇA DE NOME DO PERSONAGEM:
const input_nome= document.querySelectorAll('#nome_personagem');

input_nome.forEach(input => {
  input.addEventListener('blur', function() {
    const id = input.id;
    $.ajax({
      url: `/base/${id_personagem}`,
      type: 'POST',
      data: {
          chave: id,
          valor: this.value,
      },
      success: function(response) {
        var result = response.result;
        $('#result-container').text('Resultado: ' + result);
      }    
    });
  });
});


//MUDANÇA DE ATRIBUTOS:
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
          //ATUALIZA VALOR DE PERICIAS:
          atualizar_pericias();
        }
      }
    });    
  });
});


//MUDANÇA DE SALVAGUARDAS:
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


//MUDANÇA DE STATUS BASE:
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


//MUDANÇA DE PERICIAS:
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


//MUDANÇA DE CARACTERISTICAS:
const inputs_caracteristicas= document.querySelectorAll('input[id^="caracteristicas_"]');

inputs_caracteristicas.forEach(input => {
  input.addEventListener('blur', function() {
    const id = input.id;
    const posicao=id.search('_')
    const caracteristica = id.substring(posicao+1);

    $.ajax({
      url: `/caracteristicas_personagem/${id_personagem}`,
      type: 'POST',
      data: {
          chave: caracteristica,
          valor: this.value,
      },
      success: function(response) {
        var result = response.result;
        $('#result-container').text('Resultado: ' + result);
      }    
    });
  });
});


function capitalizeFirstLetter(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

//FUNCAO PARA ATUALIZAR PERICIAS:
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