# 🏥 AcuPath LIS &mdash; Enterprise Laboratory Information & Management System

[![CI Pipeline](https://github.com/divya-8143/Laboratory-Management-System/actions/workflows/ci.yml/badge.svg)](https://github.com/divya-8143/Laboratory-Management-System/actions)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![Next.js 14](https://img.shields.io/badge/Next.js-14.1-black?logo=next.js)](https://nextjs.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker)](https://docker.com)

**AcuPath LIS** is an enterprise-grade clinical Laboratory Information System (LIS / LMS) designed to manage and automate the entire diagnostic testing lifecycle:

$$\mathbf{Patient\ Registration} \longrightarrow \mathbf{Test\ Ordering} \longrightarrow \mathbf{Sample\ Barcoding} \longrightarrow \mathbf{Lab\ Worklist} \longrightarrow \mathbf{Abnormal\ Flagging} \longrightarrow \mathbf{Doctor\ Sign-off} \longrightarrow \mathbf{PDF\ Reports}$$

---

## 🌟 Key Capabilities & Modules

- **Patient Registration & Identity Management**: Unique identifier generator (`PAT-YYYY-XXXX`), clinical history, demographics, and emergency contact tracking.
- **Dynamic Biological Reference Range Engine**: Multi-tier evaluation based on biological sex and age ranges (days/years) triggering automatic `NORMAL`, `LOW`, `HIGH`, `CRITICAL_LOW`, `CRITICAL_HIGH`, and `ABNORMAL` qualitative alerts.
- **Sample Tracking & Automatic Barcoding**: Automatic grouping of test orders into distinct specimen tube types (`EDTA Lavender`, `SST Gold`, `Sodium Fluoride Grey`, etc.) with unique Code128 barcodes (`SMP-XXXXXXXXX`).
- **Phlebotomy Station & Accessioning Worklist**: Real-time status transitions (`PENDING_COLLECTION` $\to$ `COLLECTED` $\to$ `RECEIVED_IN_LAB` $\to$ `PROCESSING` $\to$ `COMPLETED`) with rejection reason auditing.
- **Technician Laboratory Worklist**: High-density batch result entry with clinical priority sorting (`STAT` emergency alerts rendered in pulsing red).
- **Doctor / Pathologist Verification**: Dual-confirmation verification queue with digital signature stamping and automated ReportLab PDF compilation.
- **Official PDF Report Engine & QR Authenticity**: Pixel-perfect vector PDF lab reports with clinic letterhead, parameter tables, flag highlights, and cryptographic QR code for online tamper-proof verification.
- **Operational & Financial Analytics**: Daily/monthly revenue trends, turnaround time (TAT) metrics, most requested tests, and category volume breakdowns.
- **ISO 15189 / HIPAA Audit Trail**: Immutable system-wide activity logs recording actor, IP address, timestamp, and JSON state transitions.

---

## 👥 Role-Based Access Control (RBAC) Matrix

| Clinical Action | Administrator | Receptionist | Technician | Pathologist / Doctor | Patient |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Register & Manage Patients** | ✅ | ✅ | 👁️ Read | 👁️ Read | 🔒 Self Only |
| **Test Catalog Management** | ✅ | 👁️ Read | 👁️ Read | 👁️ Read | 👁️ Read |
| **Place Orders & Billing** | ✅ | ✅ | 👁️ Read | ✅ | 🔒 Self Only |
| **Collect Samples & Barcodes** | ✅ | 👁️ Read | ✅ | 👁️ Read | ❌ |
| **Lab Worklist Result Entry** | ✅ | ❌ | ✅ | ✅ | ❌ |
| **Abnormal Value Override** | ✅ | ❌ | 👁️ Read | ✅ | ❌ |
| **Doctor Digital Sign-Off** | ✅ | ❌ | ❌ | ✅ | ❌ |
| **Download Official PDF Report**| ✅ | ✅ | ✅ | ✅ | 🔒 Self Only |
| **Executive Analytics & KPIs** | ✅ | Front-desk | Lab stats | Clinical stats | ❌ |
| **Regulatory Audit Logs** | ✅ | ❌ | ❌ | ❌ | ❌ |

---

## 🔑 Pre-Seeded Demonstration Accounts

| Role | Email | Password | Access / Department |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin@acupath.com` | `Admin@12345` | Full System & Audit Access |
| **Receptionist** | `reception@acupath.com` | `Reception@12345` | Front Desk, Booking, Invoicing |
| **Technician** | `technician@acupath.com` | `Technician@12345` | Phlebotomy & Result Entry |
| **Doctor / Pathologist** | `doctor@acupath.com` | `Doctor@12345` | Clinical Verification & Sign-off |
| **Patient** | `john.doe@gmail.com` | `Patient@12345` | Personal Test History & Reports |

---

## 🏗️ Project Architecture

```
laboratory-management-system/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/       # RESTful API endpoints (Auth, Patients, Orders, Samples, Results, Reports, Analytics)
│   │   ├── core/                   # Security, Config, Database, RBAC Permissions, Exceptions
│   │   ├── models/                 # SQLAlchemy 2.0 ORM Relational Models
│   │   ├── schemas/                # Pydantic v2 Request/Response Validation Models
│   │   ├── services/               # Clinical Domain Logic, PDF Generator, Range Evaluator
│   │   ├── templates/              # Jinja2 / HTML Medical Report Templates
│   │   └── main.py                 # FastAPI Application Server Entrypoint
│   ├── alembic/                    # Database Schema Migrations
│   ├── tests/                      # Automated PyTest Suite
│   ├── seed_data.py                # Clinical Database Seed Script
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/                    # Next.js 14 App Router
│   │   ├── lib/                    # Axios API Client & Auth Context
│   │   └── types/                  # TypeScript Data Contracts
│   ├── tailwind.config.js
│   └── package.json
├── docker/
│   ├── docker-compose.yml          # Postgres + Redis + FastAPI + Next.js
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
└── README.md
```

---

## 🚀 Quick Start Guide

### Option 1: Run with Docker Compose (Recommended)

```bash
cd docker
docker-compose up --build
```

- **Frontend Application**: `http://localhost:3000`
- **Backend API & Swagger Docs**: `http://localhost:8000/api/v1/docs`

---

### Option 2: Local Development Setup

#### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Run Database Migrations & Seed Initial Catalog
python seed_data.py

# Launch FastAPI Server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start Next.js Development Server
npm run dev
```

---

## 🧪 Automated Testing

The repository includes a comprehensive automated test suite covering authentication, RBAC barrier protection, patient management, reference range boundary conditions, the complete 9-step clinical lifecycle, and financial analytics.

```bash
cd backend
pytest -v tests/
```

---

## 📄 License & Accreditation
Developed for high-throughput clinical laboratory workflows. Licensed under the [MIT License](LICENSE).
Accreditation Ready: Designed for **CLIA** & **ISO 15189:2022** Compliance.
