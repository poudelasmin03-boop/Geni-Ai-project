from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from dotenv import load_dotenv



from fastapi import FastAPI,BackgroundTasks
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType, NameEmail

from typing import List
from tools import deleted_product,insert_items,search_all

from langserve import add_routes
from database.db import engine,Base
from models.product import Products


from langchain.tools import tool


Base.metadata.create_all(bind=engine)

load_dotenv()

emailconf = ConnectionConfig(
    MAIL_USERNAME="poudelasmin03@gmail.com",
    MAIL_PASSWORD="zmni zqqj mcfp sohs",
    MAIL_FROM="poudelasmin03@email.com",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=False,
    MAIL_FROM_NAME="Payflow",
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


app =FastAPI()


@tool 
async def email_send(email:str,body:str,title:str,bgTask:BackgroundTasks=None)->str:
    """Send the email to a specific user.
     args
       email content receiver email
       title:Topic of the email.
       body : content/actual what the user want to sent
    """
    
    bgTask.add_task(simple_send(email,title,body))
    return "Successfully sent the email"
      


##Email who send
#title =>what is the topic 
### body==>means what are the content
async def simple_send(email: str,title:str,body:str):
    message = MessageSchema(
        subject=title,
        recipients=[email],
        body=body,
        subtype=MessageType.html
    )

    await FastMail(emailconf).send_message(message)







search  = TavilySearch(
  max_results = 5
)

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0

)

tools = [search,email_send,insert_items,deleted_product,search_all]
prompt = "Acts  a senior and professional assistant give a excellent answer for the user."

agent = create_agent(
model=llm,
tools=tools,
system_prompt=prompt
)


add_routes(
    app,
    agent,
    path="/agent"
)
# query = "Who is the current pm  of nepal?"

# result = agents.invoke({"messages":[
#   {
#     "role":"user",
#     "content":query
#   }
# ]})

# print(result["messages"][-1].content)


###install uv add colorama