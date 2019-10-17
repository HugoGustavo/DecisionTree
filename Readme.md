# Aprendizado em árvore de decisão: um exemplo de aplicação
Para fazer o uso da aplicação é necessário primeiro gerar as instâncias para ser classficadas. Para isso basta utilizar o seguinte comando:

`python create-teste-data.py k` 

Onde k é o número de testes que será gerado. Após executar esse comando será gerado o arquivo **Xadrez-teste.txt** contendo todos casos de teste gerado.

Para classificar os testes gerados, basta utilizar o comando:

`python decision-tree.py`

Após executar esse comando será gerado dois arquivos,  **tree.txt** contendo a árvore de decisão em si; e  **classification.txt** contendo cada um dos testes e a classificação atribuída para cada teste pela árvore de decisão.

Obs.: Ao classificar os casos de teste, o programa apresentará o número de casos de teste, bem como  a acurária obtida nos testes.