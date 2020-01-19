TESTE = [{
            "id": 1,
            "nome": "teste1"
        },
         {
             "id": 2,
             "nome": "teste2"
         },
         {
            "id": 3,
            "nome": "teste3" 
         }]

#print(TESTE)




dados_validos = TESTE

tupla = tuple([dados_validos[chave] in dados_validos["id"]])

print(tupla)