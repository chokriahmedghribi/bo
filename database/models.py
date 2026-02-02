from sqlalchemy import create_engine, Column, Integer, String, Text, Date, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

Base = declarative_base()

class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    nom = Column(String(200), nullable=False)
    type_contact = Column(String(50))  # داخلية، خارجية، وزارة، إلخ
    adresse = Column(Text)
    telephone = Column(String(50))
    email = Column(String(100))
    notes = Column(Text)
    date_creation = Column(DateTime, default=lambda: datetime.now())

class Entrant(Base):
    __tablename__ = 'entrant'
    id = Column(Integer, primary_key=True)
    reference = Column(String(100), unique=True, nullable=False)
    date_reception = Column(Date, nullable=False)
    type_document = Column(String(100))
    expediteur_id = Column(Integer, ForeignKey('contacts.id'))
    objet = Column(Text, nullable=False)
    fichier_joint = Column(String(500))
    priorite = Column(String(20))  # عادية، عاجلة، مهمة
    statut = Column(String(50), default='غير معالج')  # غير معالج، معالج، متابعة
    notes = Column(Text)
    date_creation = Column(DateTime, default=lambda: datetime.now())
    
    expediteur = relationship("Contact")

class Sortant(Base):
    __tablename__ = 'sortant'
    id = Column(Integer, primary_key=True)
    reference = Column(String(100), unique=True, nullable=False)
    date_envoi = Column(Date, nullable=False)
    type_document = Column(String(100))
    destinataire_id = Column(Integer, ForeignKey('contacts.id'))
    objet = Column(Text, nullable=False)
    fichier_joint = Column(String(500))
    moyen_envoi = Column(String(50))  # بريد، فاكس، إيميل، يدوي
    statut = Column(String(50), default='مسودة')  # مسودة، مرسل، مؤرشف
    notes = Column(Text)
    date_creation = Column(DateTime, default=lambda: datetime.now())
    
    destinataire = relationship("Contact")

class Jointe(Base):
    __tablename__ = 'jointe'
    id = Column(Integer, primary_key=True)
    reference = Column(String(100), unique=True, nullable=False)
    date_document = Column(Date, nullable=False)
    type_document = Column(String(100))
    parties = Column(Text)
    objet = Column(Text, nullable=False)
    fichier_joint = Column(String(500))
    notes = Column(Text)
    date_creation = Column(DateTime, default=lambda: datetime.now())

class Rappel(Base):
    __tablename__ = 'rappel'
    id = Column(Integer, primary_key=True)
    titre = Column(String(200), nullable=False)
    description = Column(Text)
    date_rappel = Column(Date, nullable=False)
    priorite = Column(String(20))  # منخفضة، متوسطة، عالية
    statut = Column(String(50), default='معلق')  # معلق، مكتمل، ملغى
    document_lie = Column(String(100))
    date_creation = Column(DateTime, default=lambda: datetime.now())

class Parametre(Base):
    __tablename__ = 'parametres'
    id = Column(Integer, primary_key=True)
    nom_parametre = Column(String(100), unique=True, nullable=False)
    valeur = Column(Text)
    description = Column(Text)
    date_modification = Column(DateTime, default=lambda: datetime.now())

def init_db():
    from datetime import datetime
    db_path = "database/db.sqlite3"
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)
    return engine