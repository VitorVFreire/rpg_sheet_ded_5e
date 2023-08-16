const id_personagem = 1
async function atributos_teste(){
    const conexao_atributos = await fetch(`http://192.168.1.100:8085/atributos/${id_personagem}`)
    const atributos = await conexao_atributos.json()
  
    console.log(atributos)
}
async function pericias_teste(){
    const conexao_atributos = await fetch(`http://192.168.1.100:8085/pericias/${id_personagem}`)
    const atributos = await conexao_atributos.json()
  
    console.log(atributos)
}