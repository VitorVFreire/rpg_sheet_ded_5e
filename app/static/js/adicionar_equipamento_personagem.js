const id_personagem = parseInt(document.querySelector('#id_personagem').value, 10);
const inputs_equipamentos = document.querySelectorAll('input[id^="equipamento_"]');

inputs_equipamentos.forEach(input => {
  input.addEventListener('change', function () {
    const id = input.id;
    const posicao = id.search('to_');
    const id_equipamento = id.substring(posicao + 3);
    console.log(id_equipamento)
    let tipo = 'POST';
    if (!this.checked) {
      tipo = 'DELETE'
    }
    $.ajax({
      url: `/equipamentos/${id_personagem}`,
      type: tipo,
      data: {
        id_equipamento: id_equipamento,
      },
      success: function (response) {
        var result = response.result;
        $('#result-container').text('Resultado: ' + result);
      }
    });
  });
});