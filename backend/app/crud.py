import uuid
from sqlalchemy.orm import Session
from . import models

def create_user(db: Session, phone: str, email: str | None):
    uid = str(uuid.uuid4())
    u = models.User(id=uid, phone=phone, email=email)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u

def create_address(db: Session, user_id: str, name: str, phone: str, full_address: str, is_default: bool=False):
    aid = str(uuid.uuid4())
    a = models.Address(id=aid, user_id=user_id, name=name, phone=phone, full_address=full_address, is_default=is_default)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a

def get_product(db: Session, product_id: str):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def ensure_product(db: Session, product_id: str, title: str="i茅台-演示款"):
    p = get_product(db, product_id)
    if not p:
        p = models.Product(id=product_id, sku=product_id, title=title, last_in_stock=False, last_price=1299)
        db.add(p)
        db.commit()
        db.refresh(p)
    return p

def create_subscription(db: Session, user_id: str, product_id: str):
    sid = str(uuid.uuid4())
    s = models.Subscription(id=sid, user_id=user_id, product_id=product_id)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

def record_event(db: Session, product_id: str, event_type: str, payload: dict):
    eid = str(uuid.uuid4())
    ev = models.Event(id=eid, product_id=product_id, event_type=event_type, payload=payload)
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev

def list_events(db: Session, limit: int=50):
    return db.query(models.Event).order_by(models.Event.created_at.desc()).limit(limit).all()
