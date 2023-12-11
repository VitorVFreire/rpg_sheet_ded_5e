const requestInput = async (key, value, url, characterID, method) => {
  try {
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
          console.log(`document.querySelector('#${key}')`)
          const element = document.querySelector('#' + key);
          if (element) {
            element.innerText = value;
          }
        });
      }
    } else {
      return undefined;
    }
  } catch (error) {
    console.error('Erro na requisição:', error);
    return undefined;
  }
};

export default requestInput;