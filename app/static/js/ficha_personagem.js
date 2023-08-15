const id_personagem = parseInt(document.querySelector('#id_personagem').value, 10);

async function status_base(){
  const conexao_status_base = await fetch(`http://192.168.1.104:8085/status_base/${id_personagem}`)
  const status_base = conexao_status_base.json()

  const status_base_vida = document.getElementById('status_base_vida')
  status_base_vida.value = status_base.vida
}

async function atributos(){
  const conexao_atributos = await fetch(`http://192.168.1.104:8085/atributos/${id_personagem}`)
  const atributos = await conexao_atributos.json()

  html_atributos(atributos.forca, 
    atributos.destreza, 
    atributos.inteligencia,
    atributos.sabedoria,
    atributos.carisma, 
    atributos.constituicao)
  
  html_bonus_atributos(atributos.bonus_forca, 
    atributos.bonus_inteligencia,
    atributos.bonus_carisma,
    atributos.bonus_sabedoria,
    atributos.bonus_destreza,
    atributos.bonus_constituicao)
}

function html_atributos(forca, destreza, inteligencia, sabedoria, carisma, constituicao){
  const atributo_forca = document.getElementById('atributo_forca')
  atributo_forca.value = forca

  const atributo_destreza = document.getElementById('atributo_destreza')
  atributo_destreza.value = destreza

  const atributo_inteligencia = document.getElementById('atributo_inteligencia')
  atributo_inteligencia.value = inteligencia

  const atributo_sabedoria = document.getElementById('atributo_sabedoria')
  atributo_sabedoria.value = sabedoria

  const atributo_carisma = document.getElementById('atributo_carisma')
  atributo_carisma.value = carisma

  const atributo_constituicao = document.getElementById('atributo_constituicao')
  atributo_constituicao.value = constituicao
}

function html_bonus_atributos(bonus_forca, bonus_inteligencia, bonus_carisma, bonus_sabedoria, bonus_destreza, bonus_constituicao){
  const atributo_bonus_forca = document.getElementById('bonus_forca')
  atributo_bonus_forca.innerHTML = bonus_forca.toString()

  const atributo_bonus_destreza = document.getElementById('bonus_destreza')
  atributo_bonus_destreza.innerHTML = bonus_destreza.toString()

  const atributo_bonus_inteligencia = document.getElementById('bonus_inteligencia')
  atributo_bonus_inteligencia.innerHTML = bonus_inteligencia.toString()

  const atributo_bonus_sabedoria = document.getElementById('bonus_sabedoria')
  atributo_bonus_sabedoria.innerHTML = bonus_sabedoria.toString()

  const atributo_bonus_carisma = document.getElementById('bonus_carisma')
  atributo_bonus_carisma.innerHTML = bonus_carisma.toString()

  const atributo_bonus_constituicao = document.getElementById('bonus_constituicao')
  atributo_bonus_constituicao.innerHTML = bonus_constituicao.toString()
}

atributos()

//MUDANÇA DE NOME DO PERSONAGEM:
const input_nome= document.querySelectorAll('#nome_personagem');

input_nome.forEach(input => {
  input.addEventListener('blur', function() {
    const id = input.id;
    $.ajax({
      url: `/update/base/${id_personagem}`,
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
      url: `/update/atributos/${id_personagem}`,
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
      url: `/update/salvaguarda/${id_personagem}`,
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
      url: `/update/status_base/${id_personagem}`,
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
      url: `/update/nova_pericia/${id_personagem}`,
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
      url: `/update/caracteristicas_personagem/${id_personagem}`,
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