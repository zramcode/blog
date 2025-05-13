from db.database import Sessionlocal
from db import models

db = Sessionlocal()


db.query(models.Post).delete()
db.query(models.User).delete()

db.commit()
db.close()
print("All data has been deleted.")