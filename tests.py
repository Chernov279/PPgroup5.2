import datetime
from geopy.distance import great_circle as GC
from geopy.geocoders import Nominatim
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import func

from PPgroup5.pythonBackEnd.auth.auth import router
from PPgroup5.pythonBackEnd.auth.schemas import is_login, error_login_telephone_userexists, \
    error_login_email_userexists, error_login_udentified, is_valid_email
from PPgroup5.pythonBackEnd.auth.tokens_hashs import creating_hash_salt
from PPgroup5.pythonBackEnd.models.models import UserDB, Coordinate_get, Estimation_get
from PPgroup5.pythonBackEnd.auth.database import User, Route, Coordinate, Estimation, get_db, Session
from PPgroup5.pythonBackEnd.schemas.schemas import Route_Data, has_not_permission_error, not_found_error

app = FastAPI(title='Veloapp')


@app.get("/users/{user_id}")
def get_user_by_id(user_id: int, session: Session = Depends(get_db)):
    user = session.query(User).filter(User.id == user_id).first()
    not_found_error(user, "User")
    return {"status": "success",
            "data": {
                "user": user
            },
            "details": None
            }


@app.put("/users/{user_id}")
def update_user(user_id: int, user_data: UserDB, permission: bool = False, session: Session = Depends(get_db)):
    has_not_permission_error(permission)
    user = session.query(User).filter(User.id == user_id).first()
    not_found_error(user, "User")
    if session.query(User).filter(User.telephone_number == user_data.telephone_number).first():
        user_data.telephone_number = user.telephone_number
    if session.query(User).filter(User.email == user_data.email).first() or (not is_valid_email(user_data.email)):
        user_data.email = user.email
    generated_salt, hashed_password = creating_hash_salt(user_data.password)

    setattr(user, "hashed_password", hashed_password)
    setattr(user, "salt_hashed_password", generated_salt)
    for attr, value in user_data.dict(exclude_unset=True, exclude={"password"}).items():
        setattr(user, attr, value)
    session.commit()
    return {"status": "success",
            "data": user,
            "details": None
            }


@app.delete("/users/{user_id}")
def delete_user(user_id: int, permission: bool = False, session: Session = Depends(get_db)):
    has_not_permission_error(permission)
    user = session.query(User).filter(User.id == user_id).first()
    not_found_error(user, "User")

    session.query(Estimation).filter(Estimation.estimator_id == user_id).update({'estimator_id': 0})
    session.query(Estimation).filter(Estimation.user_id == user_id).update({'user_id': 0})
    session.query(Coordinate).filter(Coordinate.user_id == user_id).update({'user_id': 0})
    session.query(Route).filter(Route.user_id == user_id).update({'user_id': 0})
    session.delete(user)
    session.commit()
    return {
        "status": "success",
        "data": None,
        "details": None
    }


@app.get("/users_info/{user_id}")
def get_user(user_id: int, route_id: int = None, session: Session = Depends(get_db)):
    user = session.query(User).filter(User.id == user_id).first()
    not_found_error(user, "User")
    routes = session.query(Coordinate).filter((Coordinate.user_id == user_id)).all()
    if route_id is None:
        return {
            "status": "success",
            "data": {
                "id": user.id,
                "name": user.name,
                "routes": routes
            },
            "details": None
        }
    route_by_id = session.query(Coordinate).filter((Coordinate.user_id == user_id),
                                                   (Coordinate.route_id == route_id)).all()
    return {
        "status": "success",
        "data": {
            "id": user.id,
            "name": user.name,
            "routes": route_by_id
        },
        "details": None
    }


@app.get("/route_info/{route_id}")
def get_route(route_id: int, session: Session = Depends(get_db)):
    route = session.query(Route).filter(Route.route_id == route_id).first()
    not_found_error(route, "Route")
    coordinates = session.query(Coordinate).filter(Coordinate.route_id == route_id).all()
    geoLoc = Nominatim(user_agent="GetLoc")
    locname = geoLoc.reverse(
        str(session.query(Coordinate.latitude).filter(Coordinate.route_id == route_id).first())[1:-2] + ", " + str(
            session.query(Coordinate.longitude).filter(Coordinate.route_id == route_id).first())[1:-2])
    return {
        "status": "success",
        "data": {"route": route,
                 "coordinates": coordinates,
                 "locname": str(locname)},
        "details": None
    }
