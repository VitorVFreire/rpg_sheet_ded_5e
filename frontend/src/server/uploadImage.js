export async function uploadImage(file, characterID) {
    try {
      if (file) {
        const formData = new FormData();
        formData.append('img_personagem', file);

        const response = await fetch(`/caracteristicas/${characterID}`, {
          method: 'PUT',
          body: formData,
        });

        if (response.ok) {
          return await response.json();
          
        } else {
          console.error('Erro ao enviar a imagem.');
          return undefined;
        }
      }
    } catch (error) {
      console.error('Erro na requisição:', error);
      return undefined;
    }
};