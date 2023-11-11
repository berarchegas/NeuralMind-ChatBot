# NeuralMind ChatBot

ChatBot para o Processo Seletivo de Estágio de Verão da NeuralMind 2023/2024.
Relatório pode ser acessado aqui: 

## Instalação

Para instalar o chatbot, clone o repositório e rode:

```
pip install -r requirements.txt
```

Você também precisa adicionar a sua chave da OpenAI ao arquivo `.env`.

## Uso

para rodar o chatbot, rode:

```
streamlit run chat.py
```

E para rodar os testes automatizados, rode:

```
python test.py
```

## Arquivo de entrada

Numa primeira tentativa eu usava a biblioteca pypdf2 para transformar o PDF da resolução em um arquivo .txt e depois alimentava o ChatBot com esse arquivo. No entanto, o PDF contém algumas imagens e tabelas sobre as quais nosso Bot não conseguia responder.

A solução que eu encontrei foi criar scripts em Python para converter as tabelas em texto em um formato que o bot entenderia. Outros anexos, como a fórmula da NPF2, tive que passar a limpo na mão, mas o processo foi rápido.

## Bot

Primeiro extraímos o texto do arquivo .txt e quebramos o texto em chunks de tamanho 1000, possivelmente com um overlap para não terminar frases/ideias no meio. Aí usamos o FAISS (Facebook AI Similarity Search) para transformar esses chunks de texto em vectors, e guardamos isso para usar nas queries. 

Em seguida, usando o front-end do Streamlit, nós recebemos a query do usuário, fazemos uma similarity search nos nossos vectors e usamos o langchain para integrar a API da OpenAI, a query do usuário e o resultado da similarity search, e então escrevemos a resposta do ChatBot usando novamente o StreamLit.

### Possíveis melhorias

Implementação de memória do Bot. No momento ele só responde a query atual e esquece tudo que já foi perguntado anteriormente.

Otimização usando os testes automatizados. Como eu estava utilizando apenas os $5$ dólares do Free Trial, a API da OpenAI só me permitia fazer 3 perguntas por minuto, o que tornou o processo de teste lento. 

No entanto, com um acesso menos limitado, poderia usar os testes automatizados para otimizar parâmetros como tamanho dos chunks e do overlap dos chunks, usar Max Marginal Relevance Search ao invés de Similarity Search, usar chains diferentes do LangChain que especificam ao Bot melhor qual o papel dele, etc.


## Testes

Para definir um conjunto representativo de perguntas que podem ser feitas ao bot, passei por várias seções da resolução e escrevi manualmente 42 perguntas. Tentei fazer perguntas variadas e sobre diferentes tópicos, algumas perguntas realizadas foram: O curso de Dança pertence a que área? Qual a NMO de Geografia? De quem é o livro "Tarde"? Qual o máximo de vagas para Ampla Concorrência para Enfermagem? Quanto tempo o candidato tem para realizar a primeira fase?

Agora o problema maior foi definir uma forma de verificar se a resposta do bot está correta, visto que não sabemos em qual formato o bot vai entregar a resposta. Exemplo: Qual a NMO de Geografia? Ele pode responder "400", "A NMO é 400" ou "A Nota Mínima de Opção do curso de Geografia é 400", e todas estariam corretas.

A solução que eu encontrei foi definir respostas curtas e checar qual porcentagem de palavras da minha resposta curta está contida na resposta que o bot me proporciona. Ou seja, para a pergunta "Qual a NMO de Geografia?", a resposta correta seria "400" e qualquer resposta que contém 400 seria considerada correta. Claro que esse método não é muito eficiente e não funciona muito bem para perguntas com respostas mais longas, mas ele é o suficiente para eu poder verificar como a acurácia do meu bot muda se eu mudar o arquivo de entrada do pdf original para o .txt organizado, por exemplo.

Além disso, a acurácia do nosso bot fica muito atrelada ao conjunto de perguntas que eu escrevi, que não é muito significativo. Mas como minha meta era só ter uma ideia do quão funcional esse protótipo está, acho que esses testes bastam.

No final, a acurácia do bot ficou 0.7235487637678022.
