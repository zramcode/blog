
from db.database import Sessionlocal
from sqlalchemy.orm import Session

def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()