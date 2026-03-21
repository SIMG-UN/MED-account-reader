
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src import models
from src import settings
from src.app.BancolombiaEchoSaver import gmail
from langchain_core.language_models.chat_models import BaseChatModel
from .prompts import INFORMATION_STRUCTURER_PROMPT_1, TEMPLATE_1
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel
from datetime import datetime



class BancolombiaEmail(BaseModel):
    amount : float | None
    date : datetime | None
    entity : str | None
    is_spent : bool | None




# TODO: ir pensando en un version mas general que sopote langchain y vLLM
def information_structurer(llm : BaseChatModel, body : str):
    parser = JsonOutputParser()
    email = TEMPLATE_1.format(body=body)
    prompt =  INFORMATION_STRUCTURER_PROMPT_1.format(email=email)
    ai_response = llm.invoke(prompt)
    print(ai_response.content)
    json_ai_response = parser.parse(ai_response.content)
    return json_ai_response


def get_bancolombia_data(llm : BaseChatModel):

    database_url = f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    engine = create_engine(database_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    creds = gmail.get_credentials()

    service = gmail.build(
        "gmail",
        "v1",
        credentials=creds
    )

    query = "alertasynotificaciones@an.notificacionesbancolombia.com"

    messages = gmail.get_all_messages(service, query)

    emails = []

    for m in messages:
        print("email conseguido")
        emails.append(gmail.fetch_message(service, m["id"]))
    
    for bancolombia_email_dict in emails:
        try:
            body = bancolombia_email_dict["body"]
            print(body)
            print("\n"*4)
            structured_info = information_structurer(llm=llm, body=body)

            email = BancolombiaEmail(**structured_info)

            bancolombia_echo_record = models.BancolombiaEcho(
                amount=email.amount,
                date=email.date,
                entity=email.entity,
                is_spent=email.is_spent
            )
            session.add(bancolombia_echo_record)
            session.flush()
        except Exception as e:
            print(f"error: {e}")
        
    session.commit()
    session.close()


if __name__=="__main__":
    from langchain_groq import ChatGroq

    #model = "openai/gpt-oss-120b"
    model = "openai/gpt-oss-20b"
    llm= ChatGroq(model=model, temperature=0.1, api_key=settings.GROQ_API_KEY)

    get_bancolombia_data(llm=llm)



"""
python3 -m src.app.BancolombiaEchoSaver.main

"""


