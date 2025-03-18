from sqlalchemy.orm import Session
from app.models.super_admin import SuperAdmin
from app.models.tenant import Tenant
from app.models.role import Role

def create_tenant_and_roles(db: Session, super_admin_email: str, tenant_name: str):
    """
    Create a new tenant and roles for that tenant.
    - A tenant schema is created dynamically.
    - Default roles (Admin and User) are added to the tenant schema.
    - The tenant is associated with the super admin.
    
    Args:
    - db (Session): The database session for committing transactions.
    - super_admin_email (str): The email of the super admin who will manage this tenant.
    - tenant_name (str): The name of the tenant to create.

    Returns:
    - tenant (Tenant): The created tenant instance.
    - admin_role (Role): The created 'Admin' role for the tenant.
    - user_role (Role): The created 'User' role for the tenant.
    """
    # Find or create the SuperAdmin
    super_admin = db.query(SuperAdmin).filter(SuperAdmin.email == super_admin_email).first()
    if not super_admin:
        super_admin = SuperAdmin(email=super_admin_email)
        db.add(super_admin)
        db.commit()

    # Create the Tenant
    tenant = Tenant(tenant_name=tenant_name, super_admin_id=super_admin.super_admin_id)
    db.add(tenant)
    db.commit()

    # Create the Tenant Schema and Roles Table
    tenant.create_schema(db)

    # Create Default Roles for the Tenant (inside the Tenant's schema)
    admin_role = Role(role_name="Admin", tenant_id=tenant.tenant_id)
    user_role = Role(role_name="User", tenant_id=tenant.tenant_id)
    db.add(admin_role)
    db.add(user_role)
    db.commit()

    # Return the created tenant and roles
    return tenant, admin_role, user_role
