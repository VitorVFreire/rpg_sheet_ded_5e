const requestInput = async (key, value, url, characterID, method, setLoading) => {
  try {
    setLoading(true);

    const data = new FormData();
    data.append('key', key);
    data.append('value', value);

    const response = await fetch(`/${url}/${characterID}`, {
      method: method,
      body: data,
    });

    if (response.ok) {
      const responseData = await response.json();
      if (responseData.data) {
        Object.entries(responseData.data).forEach(([key, value]) => {
          const element = document.querySelector('#' + key);
          if (element) {
            element.innerText = value;
          }
        });
      }
    }
    setLoading(false);
  } catch (error) {
    console.error('Erro na requisição:', error);
    return undefined;
  }
};

export default requestInput;


