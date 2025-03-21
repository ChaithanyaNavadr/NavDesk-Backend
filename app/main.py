from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer

from app.api.v1.endpoints import (
    comment, product, role, priority, status, subscription, 
    super_admin, ticket, ticket_transfer, user, tenant, permission
)
from app.api.v1.endpoints.auth import login

app = FastAPI()

# ✅ Fix Swagger UI authorization issue
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Ticket Management System",
        version="1.0.0",
        description="API documentation for NavDesk Ticket System",
        routes=app.routes,
    )

    # Modify security scheme to accept JWT token
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # ✅ Apply authorization to all routes except "Users"
    for path, methods in openapi_schema["paths"].items():
        if path.startswith("/api/users"):  # Exclude users' endpoints from requiring auth
            continue
        for method in methods.values():
            security = method.get("security", [])
            security.append({"BearerAuth": []})
            method["security"] = security

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi  # Apply custom OpenAPI schema

# CORS Middleware (Enable if accessing API from frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with allowed origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include routers
app.include_router(super_admin.router, prefix="/api", tags=["Super Admin"])
app.include_router(tenant.router, prefix="/api", tags=["Tenants"])
app.include_router(role.router, prefix="/api", tags=["Roles"])
app.include_router(permission.router, prefix="/api", tags=["Permissions"])
app.include_router(product.router, prefix="/api", tags=["Products"])
app.include_router(subscription.router, prefix="/api", tags=["Subscriptions"])
app.include_router(login.router, prefix="/api", tags=["Auth"])
app.include_router(user.router, prefix="/api", tags=["Users"])
app.include_router(ticket.router, prefix="/api", tags=["Tickets"])
app.include_router(priority.router, prefix="/api", tags=["Priorities"])
app.include_router(comment.router, prefix="/api", tags=["Comments"])
app.include_router(ticket_transfer.router, prefix="/api", tags=["Ticket Transfers"])
app.include_router(status.router, prefix="/api", tags=["Status"])

@app.get("/")
def root():
    return {"message": "FastAPI Ticket System Running!"}
