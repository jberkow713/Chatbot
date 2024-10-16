
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

# COUNT represents ID of vector store, resetting every iteration program is run
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
    ("system","Find full website addresses related to {website}"
    )])

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

def query_store(query):

    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={'k':2, "score_threshold":.3}) 
    content = []
    if retriever.invoke(query)!=[]:
        for x in relevant_docs:
            content.append(x.page_content)
    return content 

usable_data = []
while True:
    query = input("What would you like to learn about today?: ")
    
    if query.lower() == 'exit':
        break

    cur_count = COUNT 
    websites = find_website(query)
    print(websites)
    for s in websites:
        if 'www' in s or 'https' in s:
            try:           
                add_store_site(s)
            except BaseException as error:
                continue
            
    if COUNT - cur_count == 0:
        prompt_template = ChatPromptTemplate.from_messages([
            ("system","Please give information about  {topic} "),])
        chain = prompt_template | model | StrOutputParser()
        result = chain.invoke({
                "topic":query })
        print(result)        
               
    else:
        query_2 = input(f"What would you like to learn about {query}:")
        retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={'k':5, "score_threshold":.1})
        
        relevant_docs = retriever.invoke(query_2)
        
        if relevant_docs!=[]:
            for x in relevant_docs:
                usable_data.append(x.page_content)

            result = model.invoke(usable_data)
            print(result.content) 
        else:
            prompt_template = ChatPromptTemplate.from_messages([
            ("system","Please give information about  {topic} regarding {topic2}"),])
            chain = prompt_template | model | StrOutputParser()

            result = chain.invoke({
                    "topic":query,
                    "topic2":query_2
                })
            print(result)    