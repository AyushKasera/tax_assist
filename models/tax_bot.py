import streamlit as st
import os
from langchain_ollama import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import PromptTemplate


from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key="pcsk_4xFCjp_Cr14Jn4ZbvQzSTsQA9YvGvp3UqRjuxW288d8F99TwdBiARxcCJQucwtdxLhALx2")

## retrieval from database 
## Cosine Similarity Retreive Results from VectorDB
def retrieve_query(query,k=2):
    matching_results=index.similarity_search(query,k=k)
    return matching_results



def set_custom_prompt(custom_prompt_template):
    prompt=PromptTemplate(template=custom_prompt_template,input_variables=["context","question"])
    return prompt




from langchain_ollama import OllamaLLM
llm = OllamaLLM(model="llama3.1")

def main():
    st.title("Ask Chatbot!")

    if 'messages' not in st.session_state:
        st.session_state.messages=[]

    for message in st.session_state.messages:
      st.chat_message(message['role']).markdown(message['content'])
    
    
    prompt=st.chat_input("pass your prompt here")

    if prompt:
        st.chat_message('user').markdown(prompt)
        st.session_state.messages.append({'role':'user','content':prompt})

        custom_prompt_template = """
              Use the piece of information provided in the context to answer the user's question. If you dont know the answer, just say you dont know, dont try to make up an answer.add()Dont provide anything out of the given context

              Context : {context}
              Question : {question}

              Start the answer directly. No small talk please

              """
        


        try:
            vectorstore = get_vectorstore()
            if vectorstore is None:
                st.error("Failed to load the vector storage")
            qa_chain=prompt |llm| StrOutputParser()
            response= qa_chain.invoke({'query':prompt})
            
            result = response["result"]
            




            #response="Hi , I am MediBot"
            st.chat_message('assistant').markdown(result)
            st.session_state.messages.append({'role':'assistant','content':result})
        
        except Exception as e:
            st.error(f"Error: {str(e)}")


     
if __name__ == "__main__":
    main()
