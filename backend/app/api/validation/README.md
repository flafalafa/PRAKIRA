# Enterprise API Integration Validation

This module contains the integration validation suite for Flood Guardian Sprint 7.
It tests the end-to-end routing, security, rate limiting, and domain responses for all public API endpoints.

## Structure
- `runner.py`: The entry point for running the complete validation suite.
- `scenarios.py`: Orchestrates multi-step scenarios (e.g. End-to-End Emergency Scenario).
- `contracts.py`: Validates the T-706 uniform response and error contracts.
- `security.py`: Validates the T-702 security boundary.
- `rate_limit.py`: Validates the T-707 token bucket protection.
- `performance.py`: Measures basic latency and overhead.
- `health.py`: Verifies system endpoints aren't blocked by protection layers.
- `report.py`: Generates the final Sprint 7 Readiness Report.
