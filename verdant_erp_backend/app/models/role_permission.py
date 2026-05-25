from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class RolePermission(Base):
    __tablename__ = "role_permissions"

    role_id = Column(Integer, ForeignKey("roles.id"), primary_key=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), primary_key=True)

    # relaciones opcionales (recomendado)
    role = relationship(
        "Role",
        back_populates="role_permissions",
        overlaps="permissions,roles"
    )

    permission = relationship(
        "Permission",
        back_populates="role_permissions",
        overlaps="permissions,roles"
    )