from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnableSequence
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document 
import chromadb
from langchain_openai import OpenAIEmbeddings 

load_dotenv()
model = ChatOpenAI(model='gpt-4o')

prompt_template = ChatPromptTemplate.from_messages([
    ("system","You are a comedian who tells jokes about {topic}"),
    ("human","Tell me {joke_count} jokes")
])

uppercase_output = RunnableLambda(lambda x:x.upper())
count_words = RunnableLambda(lambda x: print(len(x.split()),x))

chain = prompt_template | model | StrOutputParser() | uppercase_output | count_words

result = chain.invoke({
    "topic":"sharks",
    "joke_count":2
})

print(result)
# vector store allows you to use built in vector models, feed in lines of text into a database, then 
# query the database, add to the database, and then run similarity vector searches using queries, comparing the 
# query to all items in the database.

# Obviously then this information can be fed back into prompt templates, and using ChatOpenAi models,
# you can then look for relevant information from documents which are most similar to the query
# So this lets you search giant pieces of textual data for similar information, and then use 
# OpenAI chat models to then ask questions or interact with the returned data.


embeddings = OpenAIEmbeddings(model='text-embedding-3-small')
vector_store = Chroma(collection_name = 'test_collection',
            embedding_function=embeddings,
            persist_directory="./chroma_langchain_db")

doc_1 = Document(
   'This is a document about pineapple',
   id=1 
)

doc_2 = Document(
    'This is a document about oranges',
    id=2
)

documents = [doc_1,doc_2]
vector_store.add_documents(documents)

retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={'k':2, "score_threshold":.5}

)
query = "This is a document about hawaii"
relevant_docs = retriever.invoke(query)
if relevant_docs!=[]:
    for x in relevant_docs:
        print(x.page_content)

# retriever = db.as_retriever(
#     search_type="similarity_score_threshold",
#     search_kwargs = {"k":1, "score_threshold":.6}
# )
# relevant_docs = retriever.invoke(query)


# chroma_client = chromadb.Client()
# collection = chroma_client.create_collection(name="my_collection")
# collection.add(documents=[
#     'This is a document about pineapple',
#     'This is a document about oranges'],
#     ids = ['id1','id2'])

# collection.documents.
# results = collection.query(
#     query_texts = ['This is a query document about hawaii'],
#     n_results = 2)
# print(results)    