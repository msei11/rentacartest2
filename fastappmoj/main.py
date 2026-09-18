from fastapi import FastAPI
from fastapi import Request, HTTPException, status, Depends

from sqlalchemy import select
from sqlalchemy.orm import Session
from schema import data,izdavac,update_data
from typing import Annotated

import model
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI()


# GET — vraća SVE podatke
@app.get("/api/podaci", response_model=list[data])  # ← ISPRAVKA
def podaci_ispis(
    db: Annotated[Session, Depends(get_db)]
):
    result = db.execute(select(model.data))

    user = result.scalars().all()  # ← .all() znači LISTA

    return user


# POST — upisuje JEDAN podatak
@app.post("/api/upis", response_model=data)
def podaci_upis(
    podatak: data,
    db: Annotated[Session, Depends(get_db)]
):
    # podatak je Pydantic objekat
    # podatak.podaci je vrednost koju je korisnik poslao
    #
    # model.data je SQLAlchemy model
    # zato ovde pravimo SQLAlchemy objekat
    
    new_user = model.data(
        id = podatak.id,
        marka_auta = podatak.marka_auta,# ← ISPRAVKA: podaci, a ne podatak
        model_auta = podatak.model_auta,
        godiste = podatak.godiste,
        cenu_po_danu = podatak.cenu_po_danu,
        lokacija = podatak.lokacija,
        menjac = podatak.menjac,
        gorivo = podatak.gorivo,
        broj_sedista = podatak.broj_sedista,
        opis = podatak.opis,
        izdavac_id = podatak.izdavac_id
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/api/user/{izdavac_id}", response_model=list[data])
def get_user(izdavac_id: int,db:Annotated[Session,Depends(get_db)]):
    result = db.execute(select(model.data).where(model.data.izdavac_id == izdavac_id),)
    user = result.scalars().all()

    if user:
        return user


@app.post("/api/makeuser",response_model=izdavac)
def napravi_nalog_izdavac(izdavac:izdavac,db:Annotated[Session,Depends(get_db)]):
    novi_izdavac = model.izdavac(
        id = izdavac.id,
        Ime = izdavac.Ime,
        email = izdavac.email
    )

    db.add(novi_izdavac)
    db.commit()
    db.refresh(novi_izdavac)
    return novi_izdavac


@app.get("/api/dataofuser/{idizdavaca}", response_model=list[izdavac])
def get_aggen(idizdavaca:int,db:Annotated[Session,Depends(get_db)]):
    result = db.execute(select(model.izdavac).where(model.izdavac.id ==idizdavaca),)
    user = result.scalars().all()
    if user:
        return user

@app.get("/api/dataofcarofuser/{idizdavaca}", response_model=list[data])
def get_aggen(idizdavaca:int,db:Annotated[Session,Depends(get_db)]):
    result = db.execute(select(model.data).where(model.data.izdavac_id ==idizdavaca),)
    user = result.scalars().all()
    if user:
        return user

@app.get("/api/{idizdavaca}/{id_vozila}", response_model=data)
def get_aggen(idizdavaca:int,id_vozila:int,db:Annotated[Session,Depends(get_db)]):
    result = db.execute(
    select(model.data)
    .join(model.izdavac)
    .where(
        model.izdavac.id == idizdavaca,
        model.data.id == id_vozila
    )
    )
    user = result.scalars().first()
    if user:
       return user

@app.patch("/api/{idizdavaca}/{id_vozila}",response_model=data)
def patch_car(idizdavaca:int,id_vozila:int,user_update: update_data,db:Annotated[Session,Depends(get_db)]):
    result = db.execute(
    select(model.data).where(
    model.data.id == id_vozila,
    model.data.izdavac_id == idizdavaca
    )
    )
    user = result.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Vozilo nije pronađeno"
        )
    updates = user_update.model_dump(exclude_unset=True)

    for field, value in updates.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user

@app.delete("/api/{idizdavaca}")
def delete_car(idizdavaca: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(model.izdavac).where(model.izdavac.id == idizdavaca))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="Izdavalac nije pronađen"
        )
    
    db.delete(user)
    db.commit()