
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnableSequence
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document 
import chromadb
from langchain_openai import OpenAIEmbeddings

# TODO
# Then take the users secondary query, and compare it to the information in the data store, 
# Return information to the user
# Ask if user has any more questions , repeat until user says no


COUNT = 0

load_dotenv()
model = ChatOpenAI(model='gpt-4o')

embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
vector_store = Chroma(collection_name = 'test_collection',
            embedding_function=embeddings,
            )

def find_website(website):
    '''
    Uses Chatgpt to find a list of websites based on a user query
    '''
    prompt_template = ChatPromptTemplate.from_messages([
    ("system","You are an ai assistant that finds the top most visited websites based on what the user asks for"),
    ("human","Find me the urls of {website}")])

    format_prompt = RunnableLambda(lambda x: prompt_template.format_prompt(**x))
    invoke_model = RunnableLambda(lambda x: model.invoke(x.to_messages()))
    parse_output = RunnableLambda(lambda x: x.content)

    chain = RunnableSequence(format_prompt,invoke_model,parse_output)

    response = chain.invoke({"website":website})
    websites = []
    for w in response.split():
        if '[' in w:
            websites.append(w[1:].split(']')[0])
    return websites

def scrape(site):
    
    loader = WebBaseLoader([site])
    documents = loader.load()
    text_splitter = CharacterTextSplitter(separator="\n",chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    Words = []
    for doc in docs:    
        words = doc.page_content.split()
        Words.append(' '.join(words))
    return Words    

def add_store(text,Id):
    doc= [Document(
    text,
    id=Id)]

    vector_store.add_documents(doc)
    return 

def add_store_site(site):
    
    # This will iterate through a link and add information in chunks to the vector store 
    scraped = scrape(site)
    global COUNT 
    for x in scraped:
        add_store(x,COUNT)
        COUNT+=1
    return     

add_store_site('https://www.apple.com')

    # retriever = vector_store.as_retriever(
    #     search_type="similarity_score_threshold",
    #     search_kwargs={'k':2, "score_threshold":.3}

    # )
    # query = "This is a document about hawaii"
    # relevant_docs = retriever.invoke(query)
    # if relevant_docs!=[]:
    #     for x in relevant_docs:
    #         print(x.page_content)


# while True:
#     query = input("What website would you like to learn about today?: ")
    
#     if query.lower() == 'exit':
#         break

#     websites = find_website(query)
#     for s in websites:
      

# query = "User Query Goes here, related to website"
# relevant_docs = retriever.invoke(query)
# if relevant_docs!=[]:
#     for x in relevant_docs:
#         print(x.page_content) 

# chat_history = []
# system_message = SystemMessage(content="You are a very sarcastic AI assistant")
# chat_history.append(system_message)

