
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


# Create a prompt template for the user, to ask about websites
# Take the top few sites that the model returns, and throw them into the web scraper
# From there, chunk the textual data, and send it to the vector store/db
# Then take the users secondary query, and compare it to the information in the data store, 
# Return information to the user

# Ask if user has any more questions , repeat until user says no

load_dotenv()
model = ChatOpenAI(model='gpt-4o')
chat history = []

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

format_prompt = RunnableLambda(lambda x: prompt_template.format_prompt(**x))
invoke_model = RunnableLambda(lambda x: model.invoke(x.to_messages()))
parse_output = RunnableLambda(lambda x: x.content)

chain = RunnableSequence(format_prompt,invoke_model,parse_output)

response = chain.invoke({"topic":"sharks", "joke_count":2})

def scrape(website):
    
    loader = WebBaseLoader(url)
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    for doc in docs:    
        words = doc.page_content.split()
        print(' '.join(words))

while True:
    query = input("What website would you like to learn about today?: ")
    
    if query.lower() == 'exit':
        break

    website = model.invoke(HumanMessage(content=query))
    response= website.content

    chat_history.append(AIMessage(content=response))

    print(response)


prompt_template = ChatPromptTemplate.from_messages([
    ("system","Which website would you like to get information from?"),
    ("human","Tell me {joke_count} jokes")
])

format_prompt = RunnableLambda(lambda x: prompt_template.format_prompt(**x))
invoke_model = RunnableLambda(lambda x: model.invoke(x.to_messages()))
parse_output = RunnableLambda(lambda x: x.content)

chain = RunnableSequence(format_prompt,invoke_model,parse_output)

response = chain.invoke({"topic":"sharks", "joke_count":2})

print(response)



url = ['https://www.apple.com']
loader = WebBaseLoader(url)
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
for doc in docs[:3]:
    
    words = doc.page_content.split()
    print(' '.join(words))

embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
vector_store = Chroma(collection_name = 'test_collection',
            embedding_function=embeddings,
            persist_directory="./chroma_langchain_db")

query = "User Query Goes here, related to website"
relevant_docs = retriever.invoke(query)
if relevant_docs!=[]:
    for x in relevant_docs:
        print(x.page_content) 

chat_history = []
system_message = SystemMessage(content="You are a very sarcastic AI assistant")
chat_history.append(system_message)

while True:
    query = input("You: ")
    
    if query.lower() == 'exit':
        break 
    chat_history.append(HumanMessage(content=query))

    result = model.invoke(chat_history)
    response= result.content 
    chat_history.append(AIMessage(content=response))

    print(response)

