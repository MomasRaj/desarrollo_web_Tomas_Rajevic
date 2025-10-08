from sqlalchemy import create_engine, Column, Integer, BigInteger, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import json

DB_NAME = "confessions_db"
DB_USERNAME = "dbadmin"
DB_PASSWORD = "dbadmin"
DB_HOST = "localhost"
DB_PORT = 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# --- Models ---

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    profile_image = Column(String(255), nullable=True)
    password = Column(String(255), nullable=False)

    confesiones = relationship("Confesion", back_populates="usuario", cascade="all, delete")

class Confesion(Base):
    __tablename__ = 'confesiones'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    conf_title = Column(String(255), nullable=False)
    conf_text = Column(String(255), nullable=False)
    conf_img = Column(String(255), nullable=False)
    user_id = Column(BigInteger, ForeignKey('usuarios.id'), nullable=False)

    usuario = relationship("Usuario", back_populates="confesiones")

# --- Database Functions ---

def get_user_by_id(id):
    session = SessionLocal()
    user = session.query(Usuario).filter_by(id=id).first()
    session.close()
    return user

def get_user_by_email(email):
    session = SessionLocal()
    user = session.query(Usuario).filter_by(email=email).first()
    session.close()
    return user

def get_user_by_username(username):
    session = SessionLocal()
    user = session.query(Usuario).filter_by(username=username).first()
    session.close()
    return user

def create_user(username, password, email):
    session = SessionLocal()
    new_user = Usuario(username=username, password=password, email=email)
    session.add(new_user)
    session.commit()
    session.close()

def get_confessions(page_size):
    session = SessionLocal()
    confesiones = session.query(Confesion).limit(page_size).all()
    session.close()
    return confesiones

def create_confession(conf_title, conf_text, conf_img, user_id):
    session = SessionLocal()
    new_confession = Confesion(conf_title=conf_title,conf_text=conf_text, conf_img=conf_img, user_id=user_id)
    session.add(new_confession)
    session.commit()
    session.close()

def change_profile_picture(username, new_img):
    session = SessionLocal()
    user = session.query(Usuario).filter_by(username=username).first()
    if user:
        user.profile_image = new_img
        session.commit()
    session.close()

def get_profile_picture(username):
    session = SessionLocal()
    user = session.query(Usuario).filter_by(username=username).first()
    if user:
        profile_image = user.profile_image
    else:
        profile_image = None
    session.close()
    return profile_image

def register_user(username, password, email):
    if get_user_by_email(email) is not None:
        return False, "El correo ya esta en uso."
    
    if get_user_by_username(username) is not None:
        return False, "El nombre de usuario esta en uso."
    
    create_user(username, password, email)
    return True, None

def login_user(username, password):
    a_user = get_user_by_username(username)
    if a_user is None:
        return False, "Usuario o contraseña incorrectos."
    
    if a_user.password != password:
        return False, "Usuario o contraseña incorrectos."
    
    return True, None
