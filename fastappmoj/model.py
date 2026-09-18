from __future__ import annotations

from sqlalchemy import String, Integer, ForeignKey,DateTime, Text
from datetime import UTC, datetime
#Foreignekey je bitan za relaciju jer ce preko njega da se povezu
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base


class data(Base):
    __tablename__ = "podaci1"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    marka_auta: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    model_auta: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    godiste: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    cenu_po_danu: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    lokacija: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    menjac: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    gorivo: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    broj_sedista: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    opis: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    # STVARNA VEZA IZMEĐU TABELA
    izdavac_id: Mapped[int] = mapped_column(
        ForeignKey("izdavac.id"),
        nullable=False
    )

    # RELACIJA
    izdavac: Mapped[izdavac] = relationship(
        back_populates="automobili"
    )


class izdavac(Base):
    __tablename__ = "izdavac"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )
    automobili: Mapped[list[data]] = relationship(
        back_populates="izdavac",cascade="all,delete-orphan"
    )

    Ime:Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
    vreme_kreiranja_naloga: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            default=lambda: datetime.now(UTC),
        )
    