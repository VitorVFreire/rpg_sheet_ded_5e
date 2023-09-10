const id_personagem = parseInt(document.querySelector('#id_personagem').value, 10);

status_base()
atributos()
pericias()
salvaguardas()
caracteristicas()
habilidades()

async function status_base() {
  const conexao_status_base = await fetch(`http://localhost:8085/status_base/${id_personagem}`)
  const status_base = await conexao_status_base.json()

  html_status_base(status_base.nivel,
    status_base.alinhamento,
    status_base.faccao,
    status_base.antecendente,
    status_base.xp,
    status_base.deslocamento,
    status_base.iniciativa,
    status_base.vida,
    status_base.vida_atual,
    status_base.vida_temporaria,
    status_base.inspiracao,
    status_base.ca)
}

function html_status_base(nivel, alinhamento, faccao, antecendente, xp, deslocamento, iniciativa, vida, vida_atual, vida_temporaria, inspiracao, ca) {
  const status_vida = document.getElementById('status_base_vida')
  status_vida.value = vida

  const status_nivel = document.getElementById('status_base_nivel')
  status_nivel.value = nivel

  const status_alinhamento = document.getElementById('status_base_alinhamento')
  status_alinhamento.value = alinhamento

  const status_faccao = document.getElementById('status_base_faccao')
  status_faccao.value = faccao

  const status_antecendente = document.getElementById('status_base_antecendente')
  status_antecendente.value = antecendente

  const status_xp = document.getElementById('status_base_xp')
  status_xp.value = xp

  const status_deslocamento = document.getElementById('status_base_deslocamento')
  status_deslocamento.value = deslocamento

  const status_iniciativa = document.getElementById('status_base_iniciativa')
  status_iniciativa.value = iniciativa

  const status_vida_atual = document.getElementById('status_base_vida_atual')
  status_vida_atual.value = vida_atual

  const status_vida_temporaria = document.getElementById('status_base_vida_temporaria')
  status_vida_temporaria.value = vida_temporaria

  const status_inspiracao = document.getElementById('status_base_inspiracao')
  status_inspiracao.value = inspiracao

  const status_ca = document.getElementById('status_base_ca')
  status_ca.value = ca
}

async function atributos() {
  const conexao_atributos = await fetch(`http://localhost:8085/atributos/${id_personagem}`)
  const atributos = await conexao_atributos.json()

  html_atributos(atributos.forca,
    atributos.destreza,
    atributos.inteligencia,
    atributos.sabedoria,
    atributos.carisma,
    atributos.constituicao,
    atributos.bonus_proficiencia)

  html_bonus_atributos(atributos.bonus_forca,
    atributos.bonus_inteligencia,
    atributos.bonus_carisma,
    atributos.bonus_sabedoria,
    atributos.bonus_destreza,
    atributos.bonus_constituicao)
}

function html_atributos(forca, destreza, inteligencia, sabedoria, carisma, constituicao, bonus_proficiencia) {
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

  const atributo_bonus_proficiencia = document.getElementById('atributo_bonus_proficiencia')
  atributo_bonus_proficiencia.value = bonus_proficiencia
}

function html_bonus_atributos(bonus_forca, bonus_inteligencia, bonus_carisma, bonus_sabedoria, bonus_destreza, bonus_constituicao) {
  const atributo_bonus_forca = document.getElementById('bonus_forca')
  atributo_bonus_forca.innerHTML = bonus_forca

  const atributo_bonus_destreza = document.getElementById('bonus_destreza')
  atributo_bonus_destreza.innerHTML = bonus_destreza

  const atributo_bonus_inteligencia = document.getElementById('bonus_inteligencia')
  atributo_bonus_inteligencia.innerHTML = bonus_inteligencia

  const atributo_bonus_sabedoria = document.getElementById('bonus_sabedoria')
  atributo_bonus_sabedoria.innerHTML = bonus_sabedoria

  const atributo_bonus_carisma = document.getElementById('bonus_carisma')
  atributo_bonus_carisma.innerHTML = bonus_carisma

  const atributo_bonus_constituicao = document.getElementById('bonus_constituicao')
  atributo_bonus_constituicao.innerHTML = bonus_constituicao
}

async function pericias() {
  const conexao_pericias = await fetch(`http://localhost:8085/pericias/${id_personagem}`)
  const data = await conexao_pericias.json();

  const pericias = data.pericias;

  const periciasDoPersonagem = data.pericias_do_personagem;

  html_pericias(pericias, periciasDoPersonagem)

  const checkboxes_pericias = document.querySelectorAll('input[id^="check_pericia_"]');
  checkboxes_pericias.forEach(checkbox => {
    checkbox.addEventListener('change', function (event) {
      if (event.target.matches('input[id^="check_pericia_"]')) {
        const id = event.target.id;
        const posicao = id.search('a_');
        const pericia = id.substring(posicao + 2);
        let tipo = 'POST';
        if (!event.target.checked) {
          tipo = 'DELETE';
        }
        $.ajax({
          url: `/pericias/${id_personagem}`,
          type: tipo,
          data: {
            chave: pericia,
          },
          success: function (response) {
            var result = response.result;
            $('#result-container').text('Resultado: ' + result);
            $(`#pericia_${pericia}`).text(response.pericia);
          },
        });
      }
    });
  });
}

function html_pericias(periciasData, periciasDoPersonagem) {
  const periciasSection = document.querySelector('[data-pericias-lista]');
  for (const pericia in periciasData) {
    if (periciasData.hasOwnProperty(pericia)) {
      const valor = periciasData[pericia];
      const periciaElement = document.createElement('div');
      periciaElement.classList.add('col')
      periciaElement.innerHTML = `
            <label for="check_pericia_${pericia}">${capitalizeFirstLetter(pericia)}</label> <br>
            <input type="checkbox" class="form-check-input" id="check_pericia_${pericia}" required/>
            <div id='pericia_${pericia}'>${valor}</div>
        </div>
      `;
      periciasSection.appendChild(periciaElement);

      if (periciasDoPersonagem.includes(pericia)) {
        let check_box_pericia = document.querySelector(`#check_pericia_${pericia}`);
        check_box_pericia.checked = true;
      }
    }
  }
}

async function salvaguardas() {
  const conexao_salvaguardas = await fetch(`http://localhost:8085/salvaguardas/${id_personagem}`)
  const salvaguardas = await conexao_salvaguardas.json()
  html_salvaguardas(salvaguardas.forca,
    salvaguardas.destreza,
    salvaguardas.inteligencia,
    salvaguardas.sabedoria,
    salvaguardas.carisma,
    salvaguardas.constituicao)
  const listaSalvaguardasUnicas = [...new Set(salvaguardas.salvaguardas)];

  for (const salvaguarda of listaSalvaguardasUnicas) {
    let check_box_salvaguarda = document.querySelector(`#check_salvaguarda_${salvaguarda}`);
    if (check_box_salvaguarda) {
      check_box_salvaguarda.checked = true;
    }
  }
}

function html_salvaguardas(forca, destreza, inteligencia, sabedoria, carisma, constituicao) {
  const atributo_forca = document.getElementById('resistencia_forca')
  atributo_forca.innerHTML = forca

  const atributo_destreza = document.getElementById('resistencia_destreza')
  atributo_destreza.innerHTML = destreza

  const atributo_inteligencia = document.getElementById('resistencia_inteligencia')
  atributo_inteligencia.innerHTML = inteligencia

  const atributo_sabedoria = document.getElementById('resistencia_sabedoria')
  atributo_sabedoria.innerHTML = sabedoria

  const atributo_carisma = document.getElementById('resistencia_carisma')
  atributo_carisma.innerHTML = carisma

  const atributo_constituicao = document.getElementById('resistencia_constituicao')
  atributo_constituicao.innerHTML = constituicao
}

async function caracteristicas() {
  const conexao_caracteristicas = await fetch(`http://localhost:8085/caracteristicas/${id_personagem}`)
  const caracteristicas = await conexao_caracteristicas.json()

  html_caracteristicas(caracteristicas.idade,
    caracteristicas.altura,
    caracteristicas.peso,
    caracteristicas.cor_dos_olhos,
    caracteristicas.cor_da_pele,
    caracteristicas.cor_do_cabelo,
    caracteristicas.imagem_personagem)
}

function html_caracteristicas(idade, altura, peso, cor_dos_olhos, cor_da_pele, cor_do_cabelo, imagem_personagem) {
  const status_idade = document.getElementById('caracteristicas_idade')
  status_idade.value = idade

  const status_altura = document.getElementById('caracteristicas_altura')
  status_altura.value = altura

  const status_peso = document.getElementById('caracteristicas_peso')
  status_peso.value = peso

  const status_cor_dos_olhos = document.getElementById('caracteristicas_cor_olhos')
  status_cor_dos_olhos.value = cor_dos_olhos

  const status_cor_da_pele = document.getElementById('caracteristicas_cor_pele')
  status_cor_da_pele.value = cor_da_pele

  const status_cor_do_cabelo = document.getElementById('caracteristicas_cor_cabelo')
  status_cor_do_cabelo.value = cor_do_cabelo

  const status_imagem_personagem = document.getElementById('caracteristicas_imagem_personagem')
  status_imagem_personagem.value = imagem_personagem
}

async function habilidades() {
  const conexao_habilidades = await fetch(`http://localhost:8085/habilidades/${id_personagem}`)

  if (conexao_habilidades.status === 200){
    const data = await conexao_habilidades.json()
    html_habilidades(data)
  }  
}

function html_habilidades(habilidades) {
  const habilidadesSection = document.querySelector('[data-habilidades]');
  for (const valor in habilidades) {
    if (habilidades.hasOwnProperty(valor)) {
      const habilidade = habilidades[valor]
      const habilidadeElement = document.createElement('div');
      habilidadeElement.classList.add('row')
      habilidadeElement.classList.add('justify-content')
      habilidadeElement.innerHTML = `
        <label>Habilidade: ${habilidade.nome_habilidade}</label>
        <label>Tipo de dano: ${habilidade.tipo_dano} | ${habilidade.qtd_dados}d${habilidade.lados_dados}</label>
        <a href="${habilidade.link_detalhes}" target="_blank" class="link-warning link-offset-2 link-offset-3-hover link-underline link-underline-opacity-0">Detalhes</a>
        </div>
      `;
      habilidadesSection.appendChild(habilidadeElement);
    }
  }
}

const input_nome = document.querySelectorAll('#nome_personagem');

input_nome.forEach(input => {
  input.addEventListener('blur', function () {
    const id = input.id;
    $.ajax({
      url: `/update/base/${id_personagem}`,
      type: 'POST',
      data: {
        chave: id,
        valor: this.value,
      },
      success: function (response) {
        var result = response.result;
        $('#result-container').text('Resultado: ' + result);
      }
    });
  });
});

//MUDANÇA DE ATRIBUTOS:
const inputs_atributos = document.querySelectorAll('input[id^="atributo_"]');

inputs_atributos.forEach(input => {
  input.addEventListener('blur', function () {
    const id = input.id;
    const posicao = id.search('to_');
    const atributo = id.substring(posicao + 3);

    $.ajax({
      url: `/atributos/${id_personagem}`,
      type: 'PUT',
      data: {
        chave: atributo,
        valor: this.value,
      },
      success: function (response) {
        var result = response.result;
        $('#result-container').text('Resultado: ' + result);
        if ($(`#bonus_${atributo}`)) {
          $(`#bonus_${atributo}`).text(response.bonus);
          $(`#resistencia_${atributo}`).innerHTML = response.resistencia;
          atualizar_pericias();
          atualizar_salvaguardas();
        }
      }
    });
  });
});


//MUDANÇA DE SALVAGUARDAS:
const inputs_salvaguardas = document.querySelectorAll('input[id^="check_salvaguarda_"]');

inputs_salvaguardas.forEach(input => {
  input.addEventListener('change', function () {
    const id = input.id;
    const posicao = id.search('da_');
    const salvaguarda = id.substring(posicao + 3);
    let tipo = 'POST';
    if (!this.checked) {
      tipo = 'DELETE'
    }
    $.ajax({
      url: `/salvaguardas/${id_personagem}`,
      type: tipo,
      data: {
        chave: salvaguarda,
      },
      success: function (response) {
        var result = response.result;
        $('#result-container').text('Resultado: ' + result);
        document.getElementById(`resistencia_${salvaguarda}`).innerHTML = response.resistencia;
      }
    });
  });
});


//MUDANÇA DE STATUS BASE:
const inputs_status_base = document.querySelectorAll('input[id^="status_base_"]');

inputs_status_base.forEach(input => {
  input.addEventListener('blur', function () {
    const id = input.id;
    const posicao = id.search('e_')
    const status_base = id.substring(posicao + 2);

    $.ajax({
      url: `/status_base/${id_personagem}`,
      type: 'PUT',
      data: {
        chave: status_base,
        valor: this.value,
      },
      success: function (response) {
        var result = response.result;
        $('#result-container').text('Resultado: ' + result);
      }
    });
  });
});

//MUDANÇA DE CARACTERISTICAS:
const inputs_caracteristicas = document.querySelectorAll('input[id^="caracteristicas_"]');

inputs_caracteristicas.forEach(input => {
  input.addEventListener('blur', function () {
    const id = input.id;
    const posicao = id.search('_')
    const caracteristica = id.substring(posicao + 1);

    $.ajax({
      url: `/caracteristicas/${id_personagem}`,
      type: 'PUT',
      data: {
        chave: caracteristica,
        valor: this.value,
      },
      success: function (response) {
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
    type: 'GET',
    success: function (response) {
      for (const [key, value] of Object.entries(response.pericias)) {
        $(`#pericia_${key}`).text(value);
      }
    }
  });
}

function atualizar_salvaguardas() {
  $.ajax({
    url: `/salvaguardas/${id_personagem}`,
    type: 'GET',
    success: function (response) {
      html_salvaguardas(response.forca,
        response.destreza,
        response.inteligencia,
        response.sabedoria,
        response.carisma,
        response.constituicao)
    }
  });
}