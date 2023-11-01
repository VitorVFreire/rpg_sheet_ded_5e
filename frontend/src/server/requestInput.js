const requestInput = async (key, value, url, characterID, method) => {
  try {
    const data = new FormData();
    data.append('chave', key);
    data.append('valor', value);

    const response = await fetch(`/${url}/${characterID}`, {
      method: method,
      body: data,
    });

    if (response.ok) {
      return await response.json();
    } else {
      return undefined;
    }
  } catch (error) {
    console.error('Erro na requisição:', error);
    return undefined;
  }
};

export default requestInput;
