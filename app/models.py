import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime

from typing import Optional

from . import db

class User(db.Model):
    __tablename__ = 'users'

    user_id: so.Mapped[str] = so.mapped_column(sa.String(36), primary_key=True)
    
    first_name: so.Mapped[str] = so.mapped_column(sa.String(50))
    last_name: so.Mapped[str] = so.mapped_column(sa.String(50))
    
    
    date_joined: so.Mapped[datetime] = so.mapped_column(server_default=sa.sql.func.now())
    profile_image_url: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255))
    
    def to_json(self):
        return {
            'userId': self.user_id,
            'firstName': self.first_name,
            'lastName': self.last_name,
            'dateJoined': self.date_joined.isoformat(),
            'profileImageUrl': self.profile_image_url
        }

