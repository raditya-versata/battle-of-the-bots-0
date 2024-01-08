import json
import os
import requests
from pymongo import MongoClient
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import MongoDBAtlasVectorSearch
from key_helper import key_helper
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

def generate_response(query):
    keys = key_helper()
    client = MongoClient(keys.mongo_uri())
    db_name = "battleBot0"
    collection_name = "articles_md_split"
    collection = client[db_name][collection_name]

    embedding = OpenAIEmbeddings(openai_api_key=keys.openai_key(),disallowed_special=())


    vector_search = MongoDBAtlasVectorSearch.from_connection_string(
    keys.mongo_uri(),
    db_name + "." + collection_name,
    embedding,
    index_name="articles_md_split_idx"
    )

    # docs = vector_search.similarity_search(query, K=10)
    #
    # print(len(docs))
    # for doc in docs:
    #     print(doc.page_content)

    qa_retriever = vector_search.as_retriever(
        search_type="similarity",
        search_kwargs={
        "k": 5,
        "post_filter_pipeline": [{"$limit": 50}]
    }

    )

    prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {context}

    Question: {question}
    """
    PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
    )

    my_llm = OpenAI(openai_api_key=keys.openai_key(), temperature=0)


    qa = RetrievalQA.from_chain_type(llm=my_llm, chain_type="stuff",
                                    retriever=qa_retriever, return_source_documents=True, verbose=True,
                                    chain_type_kwargs={"prompt": PROMPT})


    docs = qa({"query": query})   

    return docs["result"]; 

def handler(event, context):
    try:
        # Read the ticketId from the URL query parameters
        ticketId = event.get('queryStringParameters', {}).get('ticketId')

        if not ticketId:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Missing ticketId parameter'})
            }

        # Set our ticket cache API endpoint.
        apiUrl = 'https://t2kc19w5te.execute-api.us-east-1.amazonaws.com/prod'

        # Making a request to the API
        headers = {
            'Authorization': f"Bearer {os.environ.get('TICKET_TOKEN')}"
        }
        response = requests.get(f"{apiUrl}?ticketId={ticketId}", headers=headers)

        # Parsing the JSON response
        data = response.json()

        id = data['ticket']['id']
        subject = data['ticket']['subject']
        name = data['users'][0]['name']
        email = data['users'][0]['email']

        # This is where you make the magic happen. 
        # Call an AI model, process the ticket data, etc.
        # Then, build your response!
        query = data['ticket']['description']
        response = generate_response(query)

        aiResponse = (
            f"Dear {name},\n\n"
            f"{response}\n\n"
            "Best regards,\n\n"
            "L2 Support Bot"
        )

        # Returning the JSON response
        return {
            'statusCode': 200,
            'body': json.dumps({'aiResponse': aiResponse})
        }

    except Exception as error:
        print('Error:', error)

        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal Server Error'})
        }