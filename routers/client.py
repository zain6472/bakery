from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.product import Client
from schemas.product import ClientCreate, ClientResponse

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.get("/", response_model=list[ClientResponse])
def get_clients(db: Session = Depends(get_db)):

    clients = db.query(Client).all()
    return clients


@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: int, db: Session = Depends(get_db)):

    client = db.query(Client).filter(Client.id == client_id).first()

    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    return client


@router.post("/", response_model=ClientResponse)
def create_client(client_data: ClientCreate, db: Session = Depends(get_db)):

    new_client = Client(
        name=client_data.name,
        phone=client_data.phone,
        city=client_data.city
    )

    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    return new_client


@router.put("/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, client_data: ClientCreate, db: Session = Depends(get_db)):

    client = db.query(Client).filter(Client.id == client_id).first()

    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    client.name = client_data.name
    client.phone = client_data.phone
    client.city = client_data.city

    db.commit()
    db.refresh(client)

    return client


@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):

    client = db.query(Client).filter(Client.id == client_id).first()

    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(client)
    db.commit()

    return {"message": "Client deleted successfully"}
