import sqlalchemy as sa
import sqlalchemy.orm as so
import datetime
import uuid

from typing import Optional

from app import db

from app.models.relationships import Identity

class User(db.Model):
    __tablename__ = 'users'

    id: so.Mapped[str] = so.mapped_column(
        sa.String(36), 
        primary_key=True, 
        default = lambda: str(uuid.uuid4())
    )

    user_id: so.Mapped[str] = so.mapped_column(
        sa.CHAR(36, collation = 'utf8mb4_bin'),
        sa.ForeignKey("identities.id"), # matching the table name in the auth service
        nullable = False, 
        unique = True
    )
    
    first_name: so.Mapped[str] = so.mapped_column(sa.String(50), nullable = False)
    last_name: so.Mapped[str] = so.mapped_column(sa.String(50), nullable = False)
    
    date_joined: so.Mapped[datetime.datetime] = so.mapped_column(server_default=sa.sql.func.now())
    profile_image_url: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256), nullable = True)

    # PLACEHOLDER for relationships
    # POST.userId
    # posts: so.Mapped[list["Post"]] = so.relationship(back_populates = "user_id")

    # # REPLY.userId
    # replies: so.Mapped[list["Reply"]] = so.relationship(back_populates = "user_id")

    # # HISTORY.userId
    # # WARNING: seems to be mongo
    # histories: so.Mapped[list["History"]] = so.relationship(back_populates = "user_id")

    # # MESSAGE.userId
    # messages: so.Mapped[list["Messages"]] = so.relationship(back_populates = "user_id")
    
    def to_json(self):
        return {
            'id': self.id,
            'userId': self.user_id,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'dateJoined': self.date_joined.isoformat(),
            'profileImageUrl': self.profile_image_url
        }

