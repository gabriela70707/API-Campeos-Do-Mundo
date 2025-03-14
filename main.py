from fastapi import FastAPI 
from model import Campeoes 
# uvicorn main:app --reload -- rodar o servidor 
print("Servidor carregado com sucesso!")


app = FastAPI() 

os_campeoes = {
    1: {
        "nome": "Pelé",
        "posicao": "Atacante",
        "pais": "Brasil",
        "ano": 1958,
        "foto": "https://static.poder360.com.br/2022/12/pele-morte-copa-848x477.jpg"
    },
    2: {
        "nome": "Kaka",
        "posicao": "Meia Ofensivo",
        "pais": "Brasil",
        "ano": 2002,
        "foto": "https://p2.trrsf.com/image/fget/cf/774/0/images.terra.com/2013/03/21/kakacorremowa.jpg"
    },
    3: {
        "nome": "Ronaldo Fenômeno",
        "posicao": "Atacante",
        "pais": "Brasil",
        "ano": 2002,
        "foto": "https://epichurus.com/wp-content/uploads/2014/03/ronaldo_taca.jpg"
    },
    4: {
        "nome": "Zidane",
        "posicao": "Meio-campista",
        "pais": "França",
        "ano": 1998,
        "foto": "https://acervofolha.blogfolha.uol.com.br/files/2018/07/Zidane.jpg"
    },
    5: {
        "nome": "Cafu",
        "posicao": "Lateral-direito",
        "pais": "Brasil",
        "ano": 2002,
        "foto": "https://f.i.uol.com.br/fotografia/2019/07/14/15631453895d2bb4ada49b0_1563145389_3x2_md.jpg"
    },
    6: {
        "nome": "Iniesta",
        "posicao": "Meio-campista",
        "pais": "Espanha",
        "ano": 2010,
        "foto": "https://static.gazetaesportiva.com/uploads/imagem/2023/08/27/000_33TM93L.jpg"
    },
    7: {
        "nome": "Messi",
        "posicao": "Atacante",
        "pais": "Argentina",
        "ano": 2022,
        "foto": "https://static.sambafoot.com/wp/sites/2/Messi-copa-768x614.jpeg"
    },
}


@app.get("/campeoes") #Significa que ao acessar esse endpoint a função abaixo será executada
async def get_campeoes(): #async significa que a função pode executar tarefas de forma assíncrona, ou seja, ela pode lidar com várias solicitações ao mesmo tempo, deixando a API mais rápida.
    return os_campeoes #retorna o dicionario criado acima


@app.get("/campeoes/{campeoes_id}")
async def get_campeao(campeoes_id:int): #pega o campeoes_id passado na url para realizar a logica da função
    if campeoes_id in os_campeoes: #verifica se o id existe no dicionario 
        campeao = os_campeoes[campeoes_id] 
        return campeao
    
    else:
        return {"error": "Esse ID de jogador não existe"}  # Resposta estruturada em JSON


@app.post("/campeoes")
async def add_campeao(campeao: Campeoes):  # Quer dizer que o modelo inserido deve seguir o padrao da Classe Campeoes

    """ 
    max encontra o maior valor existente, .keys()pega todas as chaves do dicionario ou seja o max estara pegando a maior chave do dicionario e 
    acrescentando 1 isso evita erros de duplicação de dados , que pode acontecer usando o len. O default e apenas caso nao exista nenhuma chave ainda, nesse
    caso iniciara com zero
    CODIGO:
    novo_id = max(os_campeoes.keys(), default=0) + 1  # Calcula o próximo ID
    """

    #Irei usar o len nesse caso pois nao há problema caso um jogador ocupe o id de outro que foi excluido
    novo_id = len(os_campeoes) + 1
    campeao.id = novo_id  # Define o ID diretamente no objeto `Campeao`, para evitar que ele apareça como null

    os_campeoes[novo_id] = campeao.dict()  # Converte o objeto para dicionário e adiciona no dicionario os_campeoes
    
    return {"message": "Campeão adicionado com sucesso!", **campeao.dict()}  #**campeao.dict() retorna todos os atributos do objeto


@app.put("/campeoes/{campeoes_id}")
async def editar_campeao(campeoes_id: int, campeao:Campeoes):
    if campeoes_id in os_campeoes:
        campeao.id = campeoes_id
        os_campeoes[campeoes_id] = campeao.dict()
        return {"message":"Campeão atualizado com sucesso", **campeao.dict()}
    
    else: 
        return {"error": "o id procurado não existe"}




@app.patch("/campeoes/{campeoes_id}")
async def update_campeao_parcial(campeoes_id: int, campeao_parcial: Campeoes):
    if campeoes_id in os_campeoes:
        campeao_atual = os_campeoes[campeoes_id]
        

        campos_para_atualizar = campeao_parcial.dict(exclude_unset=True) # o exclude_unset é para ignorar os valores que não foram passados na solicitação, ele vem do modelo pydantic
        campeao_atual.update(campos_para_atualizar) #update metodo para atualizar os campos
        
        os_campeoes[campeoes_id] = campeao_atual
        return {"message": "Campeão atualizado parcialmente com sucesso!", **campeao_atual} #campeao com os campos atualizados
    else:
        return {"error":"Campeão não encontrado"}



@app.delete("/campeoes/{campeoes_id}")
async def deletar_campeao(campeoes_id: int):
    if campeoes_id in os_campeoes:  # Verifica se o ID existe no dicionário
        del os_campeoes[campeoes_id]  # Deleta o registro correspondente
        return {"message": f"Campeão com ID {campeoes_id} deletado com sucesso!"}
    else:
        return {"error": f"Campeão com ID {campeoes_id} não encontrado."}




if __name__ == "__main__": #evita comportamentos indesejados quando o codigo é importado em outro arquivo
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, log_level="info", reload = True)


"""
Aprendizados :
pydantic - Serve para trabalhar com modelo de dados aqui no Python 

Quando se estiver tratando de api e for retornar uma mensagem ao usuario o mais correto é retornar em formato json ou seja chave e valor
ex: {"message": "Campeão adicionado com sucesso!", **campeao.dict()} 

uvicorn - é uma forma de rodar servidor aqui no python

campeao: Campeoes dessa forma é possivel garantir que uma entrada seja instanciada como um objeto de uma classe

campeao.dict() assim da para transformar um objeto de uma classe em um dicionario com chave e valores

os_campeoes.keys() dessa forma é possivel pegar as chaves de um dicionario sendo nomedodicionario.keys()



if __name__ == "__main__": isso serve para evitar que o servidor rode quando voce exportar o arquivo para algum lugar. Pois com esse codigo so é possivel
rodar o servidor diretamente no codigo principal 

Quando o servidor parar de atualizar por algum motivo troca de porta pode ser a melhor solução e a mais rapida tambem 
ex: uvicorn main:app --reload --port 8080

"""