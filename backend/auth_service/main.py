from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, engine, Base
from models import User, Organisation, RoleEnum
from auth import hash_password, verify_password, create_access_token, decode_token

Base.metadata.create_all(bind=engine)

app = FastAPI(title="NexaIQ Auth Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@app.get("/")
def root():
    return {"message": "NexaIQ Auth Service running"}

@app.post("/auth/register")
def register(email: str, password: str, org_name: str, db: Session = Depends(get_db)):
    try:
        if db.query(User).filter(User.email == email).first():
            raise HTTPException(400, "Email already registered")
        org = Organisation(name=org_name)
        db.add(org)
        db.flush()
        user = User(
            org_id=org.id,
            email=email,
            hashed_password=hash_password(password),
            role=RoleEnum.admin
        )
        db.add(user)
        db.commit()
        return {"message": "Organisation created", "org_id": str(org.id)}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(500, detail=str(e))
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(400, "Email already registered")
    org = Organisation(name=org_name)
    db.add(org)
    db.flush()
    user = User(
        org_id=org.id,
        email=email,
        hashed_password=hash_password(password),
        role=RoleEnum.admin
    )
    db.add(user)
    db.commit()
    return {"message": "Organisation created", "org_id": str(org.id)}

@app.post("/auth/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token({
        "sub": str(user.id),
        "org_id": str(user.org_id),
        "role": user.role
    })
    return {"access_token": token, "token_type": "bearer"}

@app.get("/auth/me")
def get_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_token(token)
        user = db.query(User).filter(User.id == payload["sub"]).first()
        return {
            "email": user.email,
            "role": user.role,
            "org_id": str(user.org_id)
        }
    except:
        raise HTTPException(401, "Invalid token")

