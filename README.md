# PRAKIRA (Flood Guardian)

## Project Overview
PRAKIRA is an Explainable Flood Intelligence Platform. It goes beyond standard weather forecasting to predict flood probabilities, Estimated Time of Arrival (ETA), and risk severity.

## Architecture Overview
PRAKIRA utilizes an Event-Driven Architecture (EDA) comprising:
- **Backend:** Python/FastAPI microservices processing environmental data.
- **Mobile:** Flutter application for end-user alerts and mapping.
- **Data Layers:** PostgreSQL (PostGIS) and Redis.

## Folder Structure
- `backend/`: Python backend services and APIs.
- `mobile/`: Flutter mobile application.
- `docs/`: System Design Specifications (SDS) and engineering guidelines.
- `infra/`: Infrastructure as Code (IaC) and deployment scripts.
- `scripts/`: Utility and automation scripts.
- `tests/`: End-to-end and integration tests.
- `.ai/`: AI agent configurations and prompts.
- `.github/`: CI/CD workflows and GitHub templates.

## Prerequisites
- Docker & Docker Compose
- Python 3.11+
- Flutter SDK 3.x
- PostgreSQL & Redis (Provided via Docker)

## Development Workflow
Please refer to `docs/ENGINEERING_GUIDELINES.md` for our strict development workflow which requires specification before implementation.

## Getting Started
*Backend setup instructions will be updated in Sprint 1.*

## Documentation Index
- [Product Requirements Document (PRD)](docs/PRD.md)
- [System Architecture](docs/ARCHITECTURE.md)
- [Flood Prediction Model](docs/FLOOD_PREDICTION_MODEL.md)
- [Event Driven Architecture](docs/EVENT_DRIVEN_ARCHITECTURE.md)
- [Database Design](docs/DATABASE_DESIGN.md)
- [Engineering Guidelines](docs/ENGINEERING_GUIDELINES.md)
- [Engineering Backlog](docs/ENGINEERING_BACKLOG.md)

## Roadmap
For a detailed implementation schedule, see the [Engineering Backlog](docs/ENGINEERING_BACKLOG.md).

## Contribution Guide
Please read `.github/CONTRIBUTING.md` and `docs/ENGINEERING_GUIDELINES.md` before contributing.
