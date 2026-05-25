# Verdant HVAC ERP / CRM / CPQ Platform

## 📌 Overview

Verdant is a full-stack ERP/CRM/CPQ system designed for HVAC service management, dispatching, inventory control, and equipment intelligence.

The platform focuses on:
- Intelligent service order dispatching
- Real-time technician scheduling
- Multi-location inventory management
- HVAC equipment lifecycle tracking
- Anomaly detection and operational intelligence

This is a **generic enterprise-grade system**, not tied to any specific company.

---

## 🏗 Architecture

### Backend
- FastAPI (Python)
- SQLAlchemy ORM
- PostgreSQL (recommended)
- Redis (real-time pub/sub)
- WebSockets for live updates

### Frontend
- SvelteKit 5
- Svelte 5 runes
- TypeScript
- TailwindCSS
- Axios for API communication

---

## ⚙️ Core Modules

### 🔧 Service Dispatch Engine
- Technician assignment system
- Slot-based scheduling (15 min intervals)
- Conflict detection (overlapping prevention)
- Daily rebalance optimization
- Real-time updates via WebSockets

### 📦 Inventory System
- Multi-location stock control
- Stock movements tracking
- Transfers between warehouses
- Inventory analytics (IRA reports)

### 🧠 HVAC Intelligence
- Equipment registry & lifecycle tracking
- Anomaly detection engine (rule-based)
- Performance & risk scoring
- Maintenance insights

### 👥 CRM
- Customer management
- Service history tracking
- Order association

---

## 🔐 Authentication

- JWT-based authentication
- Access + refresh tokens
- Role-based access control (RBAC)

---

## 📡 Real-time Features

- WebSocket communication
- Redis pub/sub event system
- Live dispatch updates
- Order status tracking

---

## 🚀 Status

This project is in **active development** and evolving toward a production-ready SaaS platform.

---

## ⚠️ Disclaimer

This repository is for educational and development purposes. It is not tied to any real company or production deployment.

---

## 🧑‍💻 Stack Summary

- FastAPI
- SvelteKit 5
- PostgreSQL
- Redis
- WebSockets
- TailwindCSS
  
Verdant_HVAC/
├── backend/ # FastAPI backend
├── frontend/ # SvelteKit frontend
├── alembic/ # Database migrations
├── docs/ # Architecture and system doc


---

## 🔐 Authentication

- JWT Access Token (short-lived)
- Refresh Token (HTTP-only cookie)
- Role-based access control (RBAC)
- Permission-based route protection (backend)

---

## 📌 Current Status

This project is actively under development and currently includes:

- Core dispatch engine (functional)
- CRM foundation
- Inventory system (multi-location)
- Equipment module
- Real-time infrastructure
- Frontend dispatch UI (partial integration)

---

## 🧩 Roadmap

### Short Term
- Fix API/Frontend alignment
- Complete CPQ proposal engine
- Add missing service endpoints
- Improve WebSocket security

### Mid Term
- PDF proposal generator
- Mobile responsiveness improvements
- Advanced scheduling optimization
- AI-assisted dispatch recommendations

### Long Term
- Full SaaS multi-tenant architecture
- Billing & invoicing module
- Customer portal
- Mobile app (technicians)

---

## 🛠 Setup (Development)

### Backend
```bash
cd verdant_erp_backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

Frontend
cd verdant-frontend
npm install
npm run dev
🌐 Environment Variables
Backend
DATABASE_URL=
SECRET_KEY=
ACCESS_TOKEN_EXPIRE_MINUTES=
REFRESH_TOKEN_EXPIRE_DAYS=
REDIS_URL=
Frontend
VITE_API_URL=http://localhost:8000
⚠️ Disclaimer

This project is a technical implementation prototype for enterprise HVAC workflow management.
It is not tied to any specific company or real-world deployment.

📄 License

This project is currently private / internal use only (no license defined yet).

🤝 Contribution

This is an active architecture-level project. Contributions are handled internally during development cycles.

🧠 Author Notes

Built as a modular enterprise simulation system for:

Field service operations
Dispatch optimization
ERP + CRM integration
Real-time operational systems

Focus: scalability, correctness, and system design over shortcuts
