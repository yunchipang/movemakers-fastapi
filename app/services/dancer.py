from typing import TYPE_CHECKING, List

from app.models import dancer as dancer_models
from app.schemas import dancer as dancer_schemas

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

import uuid


# create a dancer instance in database using the dancer data passed in
async def create_dancer(
    dancer: dancer_schemas.CreateDancer, db: "Session"
) -> dancer_schemas.Dancer:
    dancer = dancer_models.Dancer(**dancer.model_dump())
    db.add(dancer)
    db.commit()
    db.refresh(dancer)
    return dancer_schemas.Dancer.model_validate(dancer)


# query database to get all dancers
async def get_all_dancers(db: "Session") -> List[dancer_schemas.Dancer]:
    dancers = db.query(dancer_models.Dancer).all()
    return [dancer_schemas.Dancer.model_validate(dancer) for dancer in dancers]


# query database for a specific dancer with the dancer id
async def get_dancer(dancer_id: str, db: "Session"):
    dancer = (
        db.query(dancer_models.Dancer)
        .filter(dancer_models.Dancer.id == dancer_id)
        .first()
    )
    return dancer


# update a specific dancer in the database
async def update_dancer(
    dancer_id: uuid.UUID,
    dancer_data: dancer_schemas.UpdateDancer,
    db: "Session",
) -> dancer_schemas.Dancer:

    # fetch the existing dancer from the database
    dancer = (
        db.query(dancer_models.Dancer)
        .filter(dancer_models.Dancer.id == dancer_id)
        .first()
    )
    if not dancer:
        raise Exception("Dancer not found")

    # apply the updates to the dancer, skipping any None values
    for k, v in dancer_data.model_dump(exclude_unset=True).items():
        if hasattr(dancer, k):
            setattr(dancer, k, v)

    db.commit()
    db.refresh(dancer)

    return dancer_schemas.Dancer.model_validate(dancer)


# delete a specific dancer from the database
async def delete_dancer(dancer: dancer_models.Dancer, db: "Session"):
    db.delete(dancer)
    db.commit()
