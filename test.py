# Roda automaticamente o queries.txt e imprime a acuracia
# Acuracia eh o score medio das queries
# O score de uma query eh a porcentagem de palavras da resposta correta que estao na resposta do bot

from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from time import sleep

# devolve quantos % das palavras em answer estao em response
def compare(answer, response):
    answer = answer.split()
    response = response.split()
    matching = 0
    for i in answer:
        for j in response:
            if (''.join(ch for ch in i if ch.isalnum()) == ''.join(ch for ch in j if ch.isalnum())):
                matching += 1
                break 
    return matching / len(answer)

def main():
    load_dotenv()
    
    # arquivo do vestibular
    file = "./vestibular2024.txt"
    
    # extrai o texto
    text = ""
    with open(file, 'r') as infile:
        for line in infile:
            text += line

    # quebra em chunks
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    
    # cria os embeddings
    embeddings = OpenAIEmbeddings()
    knowledge_base = FAISS.from_texts(chunks, embeddings)
    
    # input.txt eh o arquivo com as perguntas e respostas
    accuracy = 0
    input = "./queries.txt"
    with open(input, 'r') as infile:
        lines = infile.readlines()
        for question, answer in zip(lines[0::2], lines[1::2]):

            # coloquei esse sleep pq minha chave da openAI soh permite 3 requests por minuto
            # e sem o sleep ele ficava printando uma mensagem de erro
            # com a chave de voces deve ser melhor tirar o sleep para rodar
            sleep(20)
            print(question)

            # faz uma similarity search
            docs = knowledge_base.similarity_search(question)
        
            llm = OpenAI()
            chain = load_qa_chain(llm, chain_type="stuff")
            response = chain.run(input_documents=docs, question=question)
            
            print(answer)
            print(response[1::] + '\n')
            accuracy += compare(answer, response)
    
    # Imprime a acuracia do bot
    print(2 * accuracy / len(lines))
        

if __name__ == '__main__':
    main()