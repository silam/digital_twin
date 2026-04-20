import os
from openai import OpenAI
import gradio as gr
import uuid
import chromadb
from pprint import pprint
import json
import requests
import random


#--------------------------------------------
# Setup
#--------------------------------------------

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if OPENAI_API_KEY is None:
    raise Exception("API Key is missing!")
else:
    print("Key is: " + OPENAI_API_KEY[:8])

client = OpenAI(api_key=OPENAI_API_KEY)

#--------------------------------------------
# Document
#--------------------------------------------
document_overview = """


My name is Si Lam

I am based in Minnesota, United States

Cooking: Enjoy cooking food every day

I love watching soccer and play soccer. I love to watch UEFA Champion Leaguage and FIFA World Cup. 
Since Messi plays for Inter Miami, I watch and follow Messi's team every game.


In 1999, I Just graduated from Ausbug College

I got my master degree in Software Engineering at University of St. Thomas in 2015
I got my BS at Augsburg College in 1999

I have Microsoft Azure Certified: AI-102, AZ-420, DP-900,DP-700,DP-600,D-100,AZ-400,AZ-104,AZ-204

also I have Amazon Web Service AWS Certified: Administrator and Developer;, 

I am Senior Software Engineer at Red Wing Shoes, working on Front End Javascript, Blazor, and
back end API

You can follow me at my personal website: http://www.serverlessdeveloper.com


My Contact info: silam@hotmail.com 


Here is the list of AWS Certification 

AWS Certified Solution Architect - Associate 
AWS Certified Developer 

Here is the list of Microsoft Azure Certification:

Microsoft Certified Azure AI Engineer Associate (AI-102)
Microsoft Certified Azure Administrator Associate (AZ-104)
Microsoft Certified Developer (AZ-204)
Microsoft Certified DevOps Certified Engineer Expert (AZ-400) 
Microsoft Certified Data Scientist Associate (DP-100)
Microsoft Certified Azure Cosmos DB Developer Specialty (AZ-420)
Microsoft Certified Azure Data Fundamentals (DP-900)

My portfolio is at http://serverlessdeveloper.com/
ReactJS, Angular, NodeJS, .NET core, Microsoft Azure Certified, AWS certified solution architect, Developer Certified, API Gateway, AWS Lambda functions, Azure DynamoDb, AWS CosmoDB

Contact me at si.lam@serverlessdeveloper.com

Skills with Microsoft Certified: Fabric Analytics Engineer Associate
1-Maintain a data analytics solution
2-Prepare data
3-Implement and manage semantic models


Skills measured for Microsoft Certified: Fabric Analytics Engineer Associate:
Plan and manage an Azure AI solution
Implement decision support solutions
Implement computer vision solutions
Implement natural language processing solutions
Implement knowledge mining and document intelligence solutions
Implement generative AI solutions




Skills at Microsoft Certified: Azure Cosmos DB Developer Specialty

Skills measured for Microsoft Certified: Azure Cosmos DB Developer Specialty

Design and implement data models
Design and implement data distribution
Integrate an Azure Cosmos DB solution
Optimize an Azure Cosmos DB solution
Maintain an Azure Cosmos DB solution


Azure Data Fundamentals Certification


Skills at AWS Developer Certificate

Skills measured for AWS Developer Certificate
Skills measured for AWS Developer Certificate
Master Advanced AWS Services: Deepen your knowledge of AWS by exploring advanced services such as AWS Lambda, Amazon S3, Amazon EC2, and AWS Elastic Beanstalk. Understanding the nuances of these services can help you design and deploy scalable, high-performance applications.
Gain Proficiency in Infrastructure as Code (IaC): Tools like AWS CloudFormation and Terraform are becoming industry standards. Learning to automate cloud infrastructure provisioning through IaC can significantly improve efficiency and accuracy in deployments.
Stay Current with AWS Certifications: Regularly update your certifications, such as the AWS Certified Developer – Associate or AWS Certified DevOps Engineer – Professional, to validate your skills and stay aligned with the latest AWS features and best practices.
Develop Expertise in Serverless Architectures: Embrace the serverless paradigm by learning how to build and manage applications with AWS serverless technologies, which can lead to cost savings and operational simplicity.
Participate in AWS Hackathons and Challenges: Engage in competitive coding and problem-solving events to push your limits, innovate with AWS technologies, and learn from your peers.
Contribute to Open Source Projects: Get involved in open source projects that use AWS technologies to gain practical experience, collaborate with other developers, and contribute to the community.
Enhance Data Skills with AWS Analytics Services: Develop your ability to work with data by using AWS analytics services like Amazon Redshift, AWS Glue, and Amazon Athena to process, analyze, and visualize data at scale.
Focus on Security Best Practices: Prioritize learning about AWS security services such as AWS Identity and Access Management (IAM), Amazon Cognito, and AWS Key Management Service (KMS) to ensure the applications you develop are secure and compliant.
Adopt a DevOps Culture: Integrate DevOps practices into your workflow by using AWS tools like AWS CodeBuild, AWS CodeDeploy, and AWS CodePipeline to automate software delivery processes and foster a culture of continuous integration and continuous delivery (CI/CD).
Engage with the AWS Community: Join AWS user groups, forums, and social media communities to exchange knowledge, stay informed about new developments, and build a professional network within the AWS ecosystem.

Show all featured items


Azure Certified: AI-102, AZ-420, DP-900,DP-700,DP-600,D-100,AZ-400,AZ-104,AZ-204
AWS Certified: Admin& Developer;, ReactJS, FastAPI, Serverless AppSenior Software Engineer at Red Wing Shoes.serverlessdeveloper.com


Experience

1-Red Wing Shoe Co
Senior Software Engineer

Red Wing Shoe Co. · Full-time

Jan 2021 - Present · 5 yrs 4 mos

Red Wing, Minnesota, United States

LinkedIn helped me get this job helped me get this job

Thumbnail for Red  Wing Shoes
Red  Wing Shoes


.NET Software Engineer

2-Deluxe

Mar 2020 - Jan 2021 · 11 mos

Minnesota, United States

Software Development Engineer

3-Hollander, a Solera Company

Jan 2019 - Feb 2020 · 1 yr 2 mos

Plymouth, MN, United States

.Software Eng

4-Danaher
Senior Software Eng

Danaher

May 2007 - Jan 2019 · 11 yrs 9 mos


5-Spanlink Communication Company

Senior Software Eng

May 1997 - May 2007 · 10 yrs 1 mo

Plymouth, MN

"""
f = open('./data/document_education.txt', 'r', encoding='utf-8')
document_education = f.read()

f = open('./data/document_overview.txt', 'r', encoding='utf-8')
document_overview = f.read()

f = open('./data/document_professional.txt', 'r', encoding='utf-8')
document_professional = f.read()

#--------------------------------------------
# Chunk Function
#--------------------------------------------
#Split text into chunks
def split_text_into_chunks(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    BOUNDARIES = ["\n\n","\n",". ", "? ", "! "," "]
    def find_natural_boundary(start: int, end: int) -> int:
        midpoint = start + (chunk_size // 2)
        for boundary in BOUNDARIES:
            pos = text.rfind(boundary, midpoint, end)
            if pos != -1:
                return pos + len(boundary)
        return end
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            end = find_natural_boundary(start, end)
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = max(start + 1, end - overlap)
    return chunks
#--------------------------------------------
# RAG
#--------------------------------------------
documents = [
    {"text": document_education, "source":"Education"},
    {"text": document_overview, "source":"personal life"},
    {"text": document_professional, "source":"Professional Experiences"}

]
chunks = []
ids = []
metadatas = []
for doc in documents:
    chunks_ = split_text_into_chunks(doc["text"], chunk_size=300, overlap = 30)
    ids_ = [str(uuid.uuid4()) for _ in range(len(chunks_))]
    metadatas_ = [{"source":doc["source"], "chunk_index": i } for i in range(len(chunks_))]

    print(str(ids_))
    chunks.extend(chunks_)
    ids.extend(ids_)
    metadatas.extend(metadatas_)

# Generate embedding
response = client.embeddings.create(
    model = "text-embedding-3-small",
    input = chunks
)


embeddings = [item.embedding for item in response.data]
print(f"Generated {len(embeddings)} embeddings")
print(f"Each embedding has {len(embeddings[0])} dimension")



chroma_client = chromadb.PersistentClient(path="./chroma_db_digital_twin")

collection = chroma_client.get_or_create_collection(name="digital_twin")

if collection.get()["ids"]:
    collection.delete(collection.get()["ids"])


#pprint(collection.get())
collection.add(
    ids=ids,
    embeddings=embeddings,
    documents=chunks,
    metadatas=metadatas
)

#--------------------------------------------
# System message
#--------------------------------------------

system_message = """ 

Important: do not make something up. If you don't know the answer, just say I donot know
The only factual information available to you is what is in this system message.
You can't get any more facts about Si Lam from the internet or make something up.
Here is the ONLY factual information about Si Lam

If the question is asked that is not answerable, say I don't know.

IMPORTANT: whenever you don't know something about Si Lam, always use send_notification tool to alert to Si Lam,
do this automatically without asking the user.
"""

#--------------------------------------------
# Main response function
#--------------------------------------------

def handle_tool_call(tool_calls):
    tools_results = []
    # return what to add to our context (about tool call results, a dictionary)
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        #print(f"Calling function {function_name}")
        args = json.loads(tool_call.function.arguments)

        #Route to function name
        if function_name == "send_notification":

            content = send_notification(args['message'])
            #print(f"Send notification: {args['message']}")
            #content = f"Notitication sent: {args['message']}"
        elif function_name == "dice_roll":

            #print(f"Send notification: {args['message']}")
            content = f"Rolled: {dice_roll()}"
        else:
            content = f"Unknown function {function_name}"

        tool_call_result  = {
            "role":"tool",
            "content":content,
            "tool_call_id":tool_call.id
            
        }

        tools_results.append(tool_call_result)

    return tools_results

def response_ai(message, history):
    
    response = client.embeddings.create(
        model = "text-embedding-3-small",
        input = [message]
    )

    query_embedding = response.data[0].embedding

    results = collection.query(
        query_embeddings = query_embedding,
        n_results=3,
        include = ["documents","metadatas"]
    )

    print("\n====================================\n")
    print("**Retrived Chunks**")
    for chunk, metadata in zip(results["documents"][0], results["metadatas"][0]):
        print("----------------------------------------------------------------")
        print(f"<<Document {metadata['source']} -- Chunk {metadata['chunk_index']}\n\n{chunk}\n\n")
    
    system_message_enhanced = system_message + "\n\nContent:\n" + "\n---\n".join(results["documents"][0])
    messages = [{"role":"system", "content": system_message_enhanced}] \
               + history \
               + [{"role":"user", "content": message}] 

    
    response = client.chat.completions.create(
        model = "gpt-4.1-mini",
        messages= messages,
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message
    loop = 0
    tool_count = len(message.tool_calls) if message is not None and message.tool_calls is not None else 0

    pprint(f"Tools count: {tool_count}")
    while message.tool_calls:
        loop += 1
        if (loop > tool_count): break
        
        #handle tool call
        tool_result = handle_tool_call(message.tool_calls) #whole list of tools

        #add message to context
        messages.append(message)

        #add info about tool call response to context, i.e. mesages
        messages.extend(tool_result)

        #invokde LLM one more time to get its updated response
        response = client.chat.completions.create(
            model='gpt-4.1-mini',
            messages=messages,
            tools=tools #will be in the future
        )
        message = response.choices[0].message

    return(message.content)

#----------------------------------------------
# Tools
#-----------------------------------------------

tools = []

pushover_user  = os.getenv("PUSHOVER_USER")
pushover_token = os.getenv("PUSHOVER_TOKEN")
pushover_url   = "https://api.pushover.net/1/messages.json"



def send_notification(message: str):
    if pushover_token is None or pushover_user is None:
        return ("Pushover credentials are not configured. Cannot send notification!")
    
    pay_load = {"user":pushover_user,
                "token": pushover_token,
                "message": message}
    requests.post(pushover_url, data = pay_load)
    return (f"Notification sent: {message}")

send_notification_function = {

    "name" : "send_notification",
    "description": "Sends a push notification to the real Si Lam. Use this when:\
                    1) Someone wants to get in touch, hire, or collaborate - ask for their name and contact details first, then send notification to Si Lam with the name and contact details.\
                    2) You don't know the answer to a question about Si Lam - send AUTOMATICALLY without asking, include the question so he can add this info later.",
    "parameters": {
        "type": "object",
        "properties":{
            "message": {
                "type": "string",
                "description":"The notification message to send to user device"
            }
        },
        "required": ["message"]
    }
}
tools.append({"type": "function","function": send_notification_function})



# simulate rolling a dice
def dice_roll():
    result = random.randint(1,6)
    return result 

roll_dice_function = {
    "name" : "dice_roll",
    "description": "Return a number by rolling a dice",
    "parameters": {
        "type": "object",
        "properties":{
            
        },
        "required": []
    }
}

tools.append( {"type": "function","function": roll_dice_function})

#--------------------------------------------
# Launch
#--------------------------------------------
gr.ChatInterface(fn=response_ai, autofocus=True, autoscroll=True, submit_btn=True, examples=["Hello","Certification","Education","Professional Experience"], title="Echo Bot").launch(inbrowser=True) #, share=True)