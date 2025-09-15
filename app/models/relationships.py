import sqlalchemy as sa
import sqlalchemy.orm as so

from app import db

class Identity(db.Model):
    """
    - A mirrored model for the 'identities' table, which is managed externally
    by the auth service.
    - Its purpose is to inform SQLAlchemy of the table's existence for creating FKs.
    """
    __tablename__ = 'identities'
    
    # The PK's type must match the real table, which is `CHAR` instead of `String` here
    id: so.Mapped[str] = so.mapped_column(sa.CHAR(36), primary_key=True)

# Other relationships
