const selectElement = document.getElementById('id_tipo_equipamento');
const caInput = document.getElementById('ca');
const dadoInput = document.getElementById('dado');
const bonusInput = document.getElementById('bonus');

function selecao(){
    selectElement.selectedIndex = 0;
    const event = new Event('change');
    selectElement.dispatchEvent(event);
}

selectElement.addEventListener('change', function() {
    const opcaoSelecionada = selectElement.options[selectElement.selectedIndex].text;
    
    // Verifique o texto selecionado e mostre/oculte os campos apropriados
    if (opcaoSelecionada === 'armadura') {
        caInput.style.display = 'block';
        dadoInput.style.display = 'none';
        bonusInput.style.display = 'none';
    } else if (opcaoSelecionada === 'espada') {
        caInput.style.display = 'none';
        dadoInput.style.display = 'block';
        bonusInput.style.display = 'block';
    } else if (opcaoSelecionada === 'escudo'){
        // Selecione o comportamento padrão quando nenhuma opção específica é selecionada
        caInput.style.display = 'block';
        dadoInput.style.display = 'none';
        bonusInput.style.display = 'block';
    }
});

selecao()

$(document).ready(function() {
    $('#form').submit(function(e) {
        e.preventDefault();

        var form = $('#form')[0]; // Obtenha o formulário
        var formData = new FormData(form); // Crie um objeto FormData
        formData.append('id_tipo_equipamento', id_tipo_equipamento);
        formData.append('nome_equipamento', nome_equipamento);
        formData.append('descricao', descricao);
        formData.append('preco', preco);
        formData.append('peso', peso);
        formData.append('ca', ca);
        formData.append('dado', dado);
        formData.append('bonus', bonus);
        formData.append('imagem_equipamento', imagem_equipamento);

        $.ajax({
            url: '/criar_equipamento',
            type: 'POST',
            data: formData, // Use o objeto FormData aqui
            processData: false, // Evite que o jQuery processe os dados
            contentType: false, // Evite que o jQuery defina o cabeçalho "Content-Type"
            success: function(response) {
                var result = response.result;
                $('#result-container').text('Resultado: ' + result);
            }
        });
    });
});


