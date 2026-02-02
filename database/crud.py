from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, date
from .models import (
    Contact, Entrant, Sortant, Jointe, 
    Rappel, Parametre
)

# دوال CRUD للجهات
def create_contact(db: Session, **kwargs):
    contact = Contact(**kwargs)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact

def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Contact).offset(skip).limit(limit).all()

def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()

def update_contact(db: Session, contact_id: int, **kwargs):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        for key, value in kwargs.items():
            setattr(contact, key, value)
        db.commit()
        db.refresh(contact)
    return contact

def delete_contact(db: Session, contact_id: int):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact

# دوال CRUD للبريد الوارد
def create_entrant(db: Session, **kwargs):
    # تأكد من أننا لا نحاول تمرير حقل expediteur ككائن
    # يجب أن يكون expediteur_id فقط
    if 'expediteur' in kwargs:
        del kwargs['expediteur']
    
    entrant = Entrant(**kwargs)
    db.add(entrant)
    db.commit()
    db.refresh(entrant)
    return entrant

def get_entrants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Entrant).offset(skip).limit(limit).all()

def get_entrant_by_ref(db: Session, reference: str):
    return db.query(Entrant).filter(Entrant.reference == reference).first()

# دوال CRUD للبريد الصادر
def create_sortant(db: Session, **kwargs):
    sortant = Sortant(**kwargs)
    db.add(sortant)
    db.commit()
    db.refresh(sortant)
    return sortant

def get_sortants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Sortant).offset(skip).limit(limit).all()

# دوال CRUD للبريد المشترك
def create_jointe(db: Session, **kwargs):
    jointe = Jointe(**kwargs)
    db.add(jointe)
    db.commit()
    db.refresh(jointe)
    return jointe

def get_jointe(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Jointe).offset(skip).limit(limit).all()

# دوال CRUD للتذكيرات
def create_rappel(db: Session, **kwargs):
    rappel = Rappel(**kwargs)
    db.add(rappel)
    db.commit()
    db.refresh(rappel)
    return rappel

def get_rappels(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Rappel).filter(
        Rappel.date_rappel >= date.today()
    ).offset(skip).limit(limit).all()

# دوال CRUD للإعدادات
def get_parametre(db: Session, nom_parametre: str):
    return db.query(Parametre).filter(
        Parametre.nom_parametre == nom_parametre
    ).first()

def set_parametre(db: Session, nom_parametre: str, valeur: str, description: str = None):
    param = get_parametre(db, nom_parametre)
    if param:
        param.valeur = valeur
        param.description = description
        param.date_modification = datetime.now()
    else:
        param = Parametre(
            nom_parametre=nom_parametre,
            valeur=valeur,
            description=description
        )
        db.add(param)
    db.commit()
    return param