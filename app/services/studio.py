from typing import TYPE_CHECKING, List

from app.models import studio as studio_models
from app.schemas import studio as studio_schemas

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


# create a studio instance in database using the studio data passed in
async def create_studio(
    studio: studio_schemas.CreateStudio, db: "Session"
) -> studio_schemas.Studio:
    studio = studio_models.Studio(**studio.dict())
    db.add(studio)
    db.commit()
    db.refresh(studio)
    return studio_schemas.Studio.from_orm(studio)


# query database to get all studios
async def get_all_studios(db: "Session") -> List[studio_schemas.Studio]:
    studios = db.query(studio_models.Studio).all()
    return list(map(studio_schemas.Studio.from_orm, studios))


# query database for a specific studio with the studio id
async def get_studio(studio_id: int, db: "Session"):
    studio = (
        db.query(studio_models.Studio)
        .filter(studio_models.Studio.id == studio_id)
        .first()
    )
    return studio


# delete a specific studio from the database
async def delete_studio(studio: studio_models.Studio, db: "Session"):
    db.delete(studio)
    db.commit()


# update a specific studio in the database
async def update_studio(
    studio_data: studio_schemas.CreateStudio,
    studio: studio_models.Studio,
    db: "Session",
) -> studio_schemas.Studio:
    # feed data one to one into the studio object
    studio.name = studio_data.name
    studio.instagram_handle = studio_data.instagram_handle
    studio.youtube_channel = studio_data.youtube_channel
    studio.address = studio_data.address
    studio.email = studio_data.email
    studio.phone = studio_data.phone
    studio.opening_hours = studio_data.opening_hours
    studio.website = studio_data.website
    studio.owner = studio_data.owner
    studio.room_count = studio_data.room_count
    studio.since = studio_data.since

    db.commit()
    db.refresh(studio)

    return studio_schemas.Studio.from_orm(studio)
