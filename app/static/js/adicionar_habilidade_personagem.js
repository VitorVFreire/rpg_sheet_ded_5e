const id_personagem = parseInt(document.querySelector('#id_personagem').value, 10);
const inputs_habilidades = document.querySelectorAll('input[id^="habilidade_"]');

inputs_habilidades.forEach(input => {
  input.addEventListener('change', function () {
    const id = input.id;
    const posicao = id.search('de_');
    const id_habilidade = id.substring(posicao + 3);
    let tipo = 'POST';
    if (!this.checked) {
      tipo = 'DELETE'
    }
    $.ajax({
      url: `/habilidades/${id_personagem}`,
      type: tipo,
      data: {
        id_habilidade: id_habilidade,
      },
      success: function (response) {
        var result = response.result;
        $('#result-container').text('Resultado: ' + result);
      }
    });
  });
});