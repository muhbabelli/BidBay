from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser
from app.core.database import get_db
from app.models import Address
from app.schemas import AddressCreate, AddressResponse

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.get("/", response_model=list[AddressResponse])
def list_addresses(
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    return db.query(Address).filter(Address.user_id == current_user.id).all()


@router.post("/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
def create_address(
    address_in: AddressCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    address = Address(user_id=current_user.id, **address_in.model_dump())
    db.add(address)
    db.commit()
    db.refresh(address)
    return address


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(
    address_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentUser,
):
    address = db.query(Address).filter(Address.id == address_id).first()
    if not address or address.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Address not found")
    db.delete(address)
    db.commit()
    return None
