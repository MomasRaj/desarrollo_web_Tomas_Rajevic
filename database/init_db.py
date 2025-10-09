from sqlalchemy import create_engine
from db import Base, engine



engine = create_engine("mysql+pymysql://cc5002:programacionweb@localhost/tarea2")
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("¡Tablas creadas!")