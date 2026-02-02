import bcrypt
from database.models import SessionLocal, User




def hash_password(password: str) -> str:
   return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()




def verify_password(password: str, hashed: str) -> bool:
   return bcrypt.checkpw(password.encode(), hashed.encode())

def create_admin_if_not_exists():
   session = SessionLocal()
   admin = session.query(User).filter(User.username == "admin").first()
   if not admin:
      admin = User(
      username="admin",
      password=hash_password("admin123"),
      role="admin"
      )
      session.add(admin)
      session.commit()
   session.close()

def authenticate(username, password):
   session = SessionLocal()
   user = session.query(User).filter(User.username == username).first()
   session.close()
   if user and verify_password(password, user.password):
      return user
   return None