import sys
import os

# Add the project root to sys.path to allow imports
sys.path.append(os.getcwd())

from sqlalchemy.orm import Session
from Db.Dbase import engine
from Db.SC import User
from Auth.JWTAuth import get_password_hash

def setup_admin():
    username = "admin"
    password = "admin"
    
    with Session(engine) as db:
        user = db.query(User).filter(User.username == username).first()
        hashed_password = get_password_hash(password)
        
        if user:
            print(f"User '{username}' already exists. Updating password and ensuring admin role.")
            user.password = hashed_password
            user.role = "admin"
            user.is_active = True
        else:
            print(f"Creating new admin user '{username}'.")
            user = User(
                username=username,
                password=hashed_password,
                email="admin@darbast.com",
                role="admin",
                is_active=True
            )
            db.add(user)
        
        db.commit()
        print("Success: admin:admin is ready.")

if __name__ == "__main__":
    setup_admin()
