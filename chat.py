from dotenv import load_dotenv
import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI

def main():

    # carrega a chave da OpenAI, para rodar voce precisa colocar ela no .env
    load_dotenv()
    st.set_page_config(page_title="Comvest 2024")
    st.header("Comvest 2024")
    
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
    
    # recebe o a pergunta do usuario
    user_question = st.text_input("Qual sua dúvida sobre o Vestibular da Unicamp 2024:")
    if user_question:

        # faz uma similarity search
        docs = knowledge_base.similarity_search(user_question)
    
        llm = OpenAI()
        chain = load_qa_chain(llm, chain_type="stuff")
        response = chain.run(input_documents=docs, question=user_question)
            
        st.write(response)
        

if __name__ == '__main__':
    main()