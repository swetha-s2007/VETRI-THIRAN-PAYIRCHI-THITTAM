import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import make_url
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL=os.getenv('DATABASE_URL','sqlite:///./pocketsmart.db')
url=make_url(DATABASE_URL)
connect_args={'check_same_thread':False} if url.get_backend_name()=='sqlite' else {}
engine=create_engine(DATABASE_URL,connect_args=connect_args)
SessionLocal=sessionmaker(bind=engine,autocommit=False,autoflush=False)
Base=declarative_base()
def get_db():
    db=SessionLocal()
    try: yield db
    finally: db.close()
