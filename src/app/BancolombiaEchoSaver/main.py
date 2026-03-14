
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src import models
from src import settings
from src.app.BancolombiaEchoSaver import gmail


def get_bancolombia_data():

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

    query = "from:thomas@solenium.co"

    messages = gmail.get_all_messages(service, query)

    emails = []

    for m in messages:
        emails.append(gmail.fetch_message(service, m["id"]))
    
    for x in emails:
        print(type(x))
        print(x)

        bancolombia_echo_record = models.BancolombiaEcho(
            date=x["date"],
            body=x["body"]
        )
        session.add(bancolombia_echo_record)
        session.flush()
    
    session.commit()
    session.close()


if __name__=="__main__":
    get_bancolombia_data()




