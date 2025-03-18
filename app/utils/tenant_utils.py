from sqlalchemy.orm import Session
from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

def create_roles_table_in_tenant_schema(schema_name: str, db: Session):
    metadata = MetaData(schema=schema_name)
    
    # Define the 'roles' table schema within the tenant schema
    roles_table = Table(
        "roles",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("role_name", String(50), nullable=False),
    )

    try:
        # Create the table within the schema
        roles_table.create(db.bind, checkfirst=True)
        
        # Insert default roles if the table is empty
        # Check if roles already exist
        existing_roles = db.query(roles_table).all()
        if not existing_roles:
            # Define default roles
            roles = ['Admin', 'User', 'SuperUser']
            for role in roles:
                insert_stmt = roles_table.insert().values(role_name=role)
                db.execute(insert_stmt)
            db.commit()
            print(f"Roles created for schema {schema_name}.")
        else:
            print(f"Roles already exist in schema {schema_name}.")

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating roles table for tenant {schema_name}: {str(e)}")
