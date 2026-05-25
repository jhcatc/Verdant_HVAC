# app/core/seed.py
from app.models.role import Role
from app.models.permission import Permission
from app.core.permissions import PERMISSIONS

ROLES = {
    "CEO": PERMISSIONS,

    "OPERATIONAL_DIRECTOR": [
        "inventory.read", "inventory.update",
        "dispatch.view", "dispatch.edit"
    ],

    "COMMERCIAL_DIRECTOR": [
        "crm.view", "crm.edit", "billing.create"
    ],

    "ADMIN_SUPPORT": [
        "billing.create", "billing.send",
        "payroll.view", "payroll.manage"
    ],

    "DISPATCHER": [
        "dispatch.view", "dispatch.edit"
    ],

    # 👇 aquí es clave tu cambio arquitectónico
    "TECHNICIAN": [
        "dispatch.view", "dispatch.edit",
        "work_orders.update"
    ]
}


async def seed_roles_permissions(db):
    permissions_map = {}

    # crear permisos
    for perm in PERMISSIONS:
        p = Permission(name=perm)
        db.add(p)
        permissions_map[perm] = p

    await db.commit()

    # crear roles
    for role_name, perms in ROLES.items():
        role = Role(name=role_name)
        role.permissions = [permissions_map[p] for p in perms]
        db.add(role)

    await db.commit()