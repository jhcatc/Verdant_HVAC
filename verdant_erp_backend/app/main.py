from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import *
from app.core.redis_subscriber import redis_listener
import asyncio
import os
from app.routes import (
    auth,
    users,
    service_orders,
    ws,
    customers,
    inventory,
    customer_locations,
    telemetry,
    pm_engine,
    pm_generator,
    sla_engine,
)
from app.routes.hvac import equipment, maintenance_logs, anomaly, intelligence, component_registry
from app.jobs.pm_scheduler import start_pm_scheduler, stop_pm_scheduler
from app.routes.maintenance import pm_generator, maintenance_plans
from app.modules.catalogs import router as catalogs_routers
from app.modules.equipment_documents import router as router_equipment_docs
from app.modules.equipment_photos import router as router_photos
from app.modules.equipment_qr import router as router_qr
from app.routes.crm import (
    contracts, 
    leads, 
    opportunities, 
    dashboard, 
    intelligence, 
    proposals, 
    renewals, 
    proposal_line_items, 
    proposal_versions,
    equipment_catalog, 
)
from app.routes.crm import customers as crm_customers



app = FastAPI(title="Verdant ERP API")


# =========================================================
# 🔥 CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# 🚀 STARTUP
# =========================================================

@app.on_event("startup")
async def startup_infra():


    use_redis = os.getenv(
        "USE_REDIS",
        "false"
    ).lower() == "true"

    if use_redis:

        try:

            asyncio.create_task(
                redis_listener()
            )

            print("✅ Redis listener started")

        except Exception as e:

            print(
                "❌ Failed to start Redis listener:",
                e
            )

    else:

        print("⚠️ Redis disabled (dev mode)")

@app.on_event("startup")
async def startup_scheduler():
    start_pm_scheduler()


@app.on_event("shutdown")
async def shutdown_event():
    stop_pm_scheduler()

# =========================================================
# ROUTERS
# =========================================================

app.include_router(ws.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(customers.router)
app.include_router(service_orders.router)
app.include_router(inventory.router)
app.include_router(equipment.router)
app.include_router(customer_locations.router)
app.include_router(maintenance_logs.router)
app.include_router(telemetry.router)
app.include_router(anomaly.router)
app.include_router(intelligence.router)
app.include_router(pm_generator.router)
app.include_router(maintenance_plans.router)
app.include_router(pm_engine.router)
app.include_router(sla_engine.router)   
app.include_router(catalogs_routers.router)
app.include_router(router_equipment_docs.router)
app.include_router(router_qr.router)
app.include_router(router_photos.router)    
app.include_router(component_registry.router)
app.include_router(leads.router)
app.include_router(opportunities.router)
app.include_router(contracts.router)
app.include_router(dashboard.router)
app.include_router(crm_customers.router)
app.include_router(intelligence.router)
app.include_router(proposals.router)
app.include_router(renewals.router)
app.include_router(proposal_line_items.router)
app.include_router(proposal_versions.router)
app.include_router(equipment_catalog.router)