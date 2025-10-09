from sqlalchemy import create_engine, Column, Integer, BigInteger, String, ForeignKey, Enum, Text, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy.sql import func
from datetime import datetime
import json

DB_NAME = "tarea2"
DB_USERNAME = "cc5002"
DB_PASSWORD = "programacionweb"
DB_HOST = "localhost"
DB_PORT = 3306

DATABASE_URL = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# --- Models ---

class Region(Base):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)

    comunas = relationship('Comuna', back_populates='region')


class Comuna(Base):
    __tablename__ = 'comuna'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(200), nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)

    region = relationship('Region', back_populates='comunas')
    avisos = relationship('AvisoAdopcion', back_populates='comuna')


class AvisoAdopcion(Base):
    __tablename__ = 'aviso_adopcion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_ingreso = Column(DateTime, nullable=False, server_default=func.now())
    comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable=False)
    sector = Column(String(100))
    nombre = Column(String(200), nullable=False)
    email = Column(String(100), nullable=False)
    celular = Column(String(15))
    tipo = Column(Enum('gato', 'perro'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    edad = Column(Integer, nullable=False)
    unidad_medida = Column(Enum('a', 'm'), nullable=False)  #
    fecha_entrega = Column(DateTime, nullable=False)
    descripcion = Column(Text(500))

    comuna = relationship('Comuna', back_populates='avisos')
    fotos = relationship('Foto', back_populates='aviso', cascade="all, delete-orphan")
    contactos = relationship('ContactarPor', back_populates='aviso', cascade="all, delete-orphan")


class Foto(Base):
    __tablename__ = 'foto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ruta_archivo = Column(String(300), nullable=False)
    nombre_archivo = Column(String(300), nullable=False)
    actividad_id = Column(Integer, ForeignKey('aviso_adopcion.id'), nullable=False)

    aviso = relationship('AvisoAdopcion', back_populates='fotos')


class ContactarPor(Base):
    __tablename__ = 'contactar_por'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(Enum('whatsapp', 'telegram', 'X', 'instagram', 'tiktok', 'otra'), nullable=False)
    identificador = Column(String(150), nullable=False)
    actividad_id = Column(Integer, ForeignKey('aviso_adopcion.id'), nullable=False)

    aviso = relationship('AvisoAdopcion', back_populates='contactos')

# --- Database Functions ---

def get_all_regiones():
    session = SessionLocal()
    regiones = session.query(Region).all()
    session.close()
    return regiones

def get_comunas_by_region(region_id):
    session = SessionLocal()
    comunas = session.query(Comuna).filter_by(region_id=region_id).all()
    session.close()
    return comunas


def get_ultimo_avisos(limit=5):
    session = SessionLocal()
    avisos = session.query(AvisoAdopcion).order_by(AvisoAdopcion.fecha_ingreso.desc()).limit(limit).all()
    session.close()
    return avisos

def get_aviso_by_id(aviso_id):
    session = SessionLocal()
    aviso = session.query(AvisoAdopcion).filter_by(id=aviso_id).first()
    session.close()
    return aviso

def crear_aviso(comuna_id, sector, nombre, email, celular, tipo, cantidad, edad, unidad_medida, fecha_entrega, descripcion):
    session = SessionLocal()
    nuevo_aviso = AvisoAdopcion(
        fecha_ingreso=datetime.now(),
        comuna_id=comuna_id,
        sector=sector,
        nombre=nombre,
        email=email,
        celular=celular,
        tipo=tipo,
        cantidad=cantidad,
        edad=edad,
        unidad_medida=unidad_medida,
        fecha_entrega=fecha_entrega,
        descripcion=descripcion
    )
    session.add(nuevo_aviso)
    session.commit()
    session.close()
    return nuevo_aviso


def agregar_foto(aviso_id, ruta_archivo, nombre_archivo):
    session = SessionLocal()
    nueva_foto = Foto(
        actividad_id=aviso_id,
        ruta_archivo=ruta_archivo,
        nombre_archivo=nombre_archivo
    )
    session.add(nueva_foto)
    session.commit()
    session.close()

def get_fotos_por_aviso(aviso_id):
    session = SessionLocal()
    fotos = session.query(Foto).filter_by(actividad_id=aviso_id).all()
    session.close()
    return fotos


def agregar_contacto(aviso_id, nombre, identificador):
    session = SessionLocal()
    contacto = ContactarPor(
        actividad_id=aviso_id,
        nombre=nombre,
        identificador=identificador
    )
    session.add(contacto)
    session.commit()
    session.close()

def get_contactos_por_aviso(aviso_id):
    session = SessionLocal()
    contactos = session.query(ContactarPor).filter_by(actividad_id=aviso_id).all()
    session.close()
    return contactos
