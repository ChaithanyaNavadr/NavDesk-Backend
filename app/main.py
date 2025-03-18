from fastapi import FastAPI
from app.api.v1.endpoints import comment, product, role, priority, status, subscription, super_admin, ticket, ticket_transfer, user, tenant, permission
from app.api.v1.endpoints.auth import login, register
app = FastAPI()

# Include routers
app.include_router(user.router, prefix="/api", tags=["Users"])
app.include_router(role.router, prefix="/api", tags=["Roles"])
app.include_router(priority.router, prefix="/api", tags=["Priorities"])
app.include_router(ticket.router, prefix="/api", tags=["Tickets"])
app.include_router(tenant.router, prefix="/api", tags=["Tenants"])
app.include_router(permission.router, prefix="/api", tags=["Permissions"])
app.include_router(comment.router, prefix="/api", tags=["Comments"])
app.include_router(product.router, prefix="/api", tags=["Products"])
app.include_router(subscription.router, prefix="/api", tags=["Subscriptions"])
app.include_router(ticket_transfer.router, prefix="/api", tags=["Ticket Transfers"])
app.include_router(status.router, prefix="/api", tags=["Status"])
app.include_router(super_admin.router, prefix="/api", tags=["Super Admin"])
app.include_router(login.router, prefix="/api", tags=["Auth"])
# app.include_router(register.router, prefix="/api", tags=["Auth"])


@app.get("/")
def root():
    return {"message": "FastAPI Ticket System Running!"}
