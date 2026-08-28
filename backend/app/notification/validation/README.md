# Enterprise Notification Validation & End-to-End Simulation

This framework acts as the final Quality Assurance (QA) gatekeeper for the entire Notification Layer. Before any code is deployed to production, this simulator artificially injects synthetic predictions and traces them through every single layer (Policy, Preferences, Escalation, Scheduler, Tracking) to guarantee systemic integrity.

## Architecture
- **Scenarios (`scenario.py`)**: Defines discrete, highly-specific test cases (e.g. `EmergencyOverrideScenario`). Each scenario defines its own setup data and expected outcomes.
- **Simulator (`simulator.py`)**: The executor that takes a scenario, spins up an isolated execution environment, runs it through the notification pipeline, and records the raw output.
- **Validator & Consistency (`validator.py`, `consistency.py`)**: Takes the raw output from the Simulator and mathematically proves that it matches the expected outcomes, while ensuring no logical paradoxes occurred (e.g. "Status is DELIVERED but priority was LOW during an EMERGENCY").
- **Runner & Report (`runner.py`, `report.py`)**: The orchestrator that loops through all registered scenarios in the `ScenarioRegistry`, runs them via the Simulator, aggregates the results, calculates metrics, and generates a final `ValidationReport`.

## Usage Context
This module is strictly for internal engineering use, CI/CD pipelines, and calibration. It does NOT generate or intercept real production notifications. It is a sterile laboratory for ensuring our flood warning logic behaves exactly as designed under extreme conditions.
