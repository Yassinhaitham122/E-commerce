from app.database import get_session
from app.core.security import hash_password
from app import models
from sqlmodel import Session

def main():
    session: Session = next(get_session())

    user = session.get(models.User, 1)  # ID للمستخدم اللي عايز تعدل الباسورد بتاعه
    if not user:
        print("User not found")
        return

    user.password_hash = hash_password("vvvyassin0")
    session.add(user)
    session.commit()
    session.refresh(user)

    print("Password updated successfully!")

if __name__ == "__main__":
    main()
