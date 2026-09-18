from pydantic import BaseModel, Field, ConfigDict,EmailStr
from datetime import datetime


class data(BaseModel):

    model_config = ConfigDict(protected_namespaces=())

    id: int
    marka_auta: str = Field(min_length=1, max_length=50)
    model_auta: str = Field(min_length=1, max_length=50)
    godiste: int
    cenu_po_danu: int
    lokacija: str = Field(min_length=1, max_length=50)
    menjac: str = Field(min_length=1, max_length=50)
    gorivo: str = Field(min_length=1, max_length=50)
    broj_sedista: int
    opis: str = Field(min_length=1, max_length=500)

    izdavac_id: int  # ← DODAJ OVO


class izdavac(BaseModel):
    id: int
    Ime:str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length= 120)
    vreme_kreiranja_naloga:datetime


class update_data(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    marka_auta: str | None = Field(default=None, min_length=1, max_length=50)
    model_auta: str | None = Field(default=None, min_length=1, max_length=50)
    godiste: int | None = None
    cenu_po_danu: int | None = None
    lokacija: str | None = Field(default=None, min_length=1, max_length=50)
    menjac: str | None = Field(default=None, min_length=1, max_length=50)
    gorivo: str | None = Field(default=None, min_length=1, max_length=50)
    broj_sedista: int | None = None
    opis: str | None = Field(default=None, min_length=1, max_length=500)