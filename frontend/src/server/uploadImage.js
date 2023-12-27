export async function uploadImage(file, characterID, setLoading) {
    try {
      if (file) {
        setLoading(true);
        const formData = new FormData();
        formData.append('character_image', file);

        const response = await fetch(`/characteristics/${characterID}`, {
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
    } finally {
      setLoading(false);
    }
};