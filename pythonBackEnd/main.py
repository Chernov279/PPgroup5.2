from datetime import timedelta
from fastapi import FastAPI, HTTPException, Depends
from PPgroup5.pythonBackEnd.auth.tokens_hashs import (creating_hash_salt,
                                                      authenticate_user, create_token, token_user, generate_token)
from PPgroup5.pythonBackEnd.auth.models import UserDB, User_login
from sqlalchemy.orm import sessionmaker
from PPgroup5.pythonBackEnd.auth.database import User, Route, Coordinate, engine
from PPgroup5.pythonBackEnd.auth.schemas import Route_Data

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Session = sessionmaker(engine)

app = FastAPI(title='Veloapp')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authorization/")
def create_user(user_data: UserDB, db: Session = Depends(get_db)):
    if db.query(User).filter(User.login == user_data.login).first():
        raise HTTPException(status_code=409, detail="Login is already exists")
    token_mobile = generate_token()
    generated_salt, hashed_password = creating_hash_salt(user_data.password)
    new_user = User(
        name=user_data.name,
        login=user_data.login,
        hashed_password=hashed_password,
        token_mobile=token_mobile,
        salt_hashed_password=generated_salt
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token = create_token(new_user.id, timedelta(hours=12))
    return {"token": token, "message": f"Success, {new_user.name}, welcome!"}


@app.post("/login")
def login(login_user: User_login, entry_token: str = None, db: Session = Depends(get_db)):
    if token_user(entry_token):
        user_id = token_user(entry_token)
        if user_id:
            db_user = db.query(User).filter(User.id == user_id).first()
            if db_user:
                return {"token": entry_token, "message": f"Hello, {db_user.name}"}
            else:
                raise HTTPException(status_code=401, detail="Invalid token")
    db_user = db.query(User).filter(User.login == login_user.login).first()
    if db_user:
        if authenticate_user(login_user.password, db_user.hashed_password, db_user.salt_hashed_password):
            token = create_token(db_user.id, timedelta(hours=2))
            return {"token": token, "message": f"Hello, {db_user.name}"}
    raise HTTPException(status_code=401, detail="Incorrect login or password")


@app.get("/users/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"name": user.name, "id": user.id, "login": user.login, "token_mobile": user.token_mobile}


@app.put("/users/{user_id}", )
def update_user(user_id: int, user_data: UserDB, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    generated_salt, hashed_password = creating_hash_salt(user_data.password)
    user_data = user_data.dict()
    del user_data["password"]
    user_data["hashed_password"]= hashed_password
    user_data["salt_hashed_password"] = generated_salt


    for attr, value in user_data.items():
        setattr(user, attr, value)
    db.commit()
    db.refresh(user)
    return {"message: "f"Success, user {user.name} was updated"}


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.refresh(user)
    db.commit()
    return {"message: "f"Success, {user.name} with user id {user_id} was deleted"}


@app.get("/users_info/{user_id}")
def get_user(user_id: int, route_id: int = None):
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()
    routes = session.query(Coordinate).filter(Route.user_id == user_id and Coordinate.user_id == user_id).all()
    route_by_id = session.query(Coordinate).filter(Route.user_id == user_id and Coordinate.route_id == route_id).first()
    session.close()
    if route_id is None:
        return user, routes
    else:
        return user, route_by_id


@app.get("/route_info/{route_id}")
def get_route(route_id: int):
    session = Session()
    route = session.query(Route).filter(Route.route_id == route_id).first()
    coordinates = session.query(Coordinate.latitude, Coordinate.longitude).filter(Coordinate.route_id == route_id).all()
    session.close()
    return route, coordinates


@app.post("/route/")
def post_route(route_info: Route_Data):
    session = Session()
    us_id = 1  # session.query(User.id).filter(User.token==route_info.token).first()
    dist = None
    new_route = Route(route_id=route_info.route_id, user_id=us_id, estimation=None, distance=dist)
    session.add(new_route)
    for cord in range(len(route_info.latitude_longitude_cordid)):
        new_coordinates = Coordinate(route_id=route_info.route_id, user_id=us_id,
                                     latitude=route_info.latitude_longitude_cordid[cord][0],
                                     longitude=route_info.latitude_longitude_cordid[cord][1],
                                     cord_id=route_info.latitude_longitude_cordid[cord][2],
                                     operation_id=(max(session.query(Coordinate.operation_id).all()) + 1))
        session.add(new_coordinates)


@app.get("/free_route_id/")
def get_free_route_id():
    session = Session()
    return (max(session.query(Route.route_id).all()) + 1)
