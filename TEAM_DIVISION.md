# NarrativeOS Team Work Division

This document outlines the responsibilities of the three team members, integrating **Apify**, **Zynd**, and **Superplane** as core technologies, with **GitHub Copilot** as the primary development accelerator.

---

## 🏗️ Team Responsibilities (3 Members)

### 👤 Member 1: The Sensory Lead
**Core Tool:** **Apify**
*   **Primary Ownership:** **Agent 1 (Data Acquisition Agent)**
*   **Focus:**
    *   Developing Apify Actors for internet-scale data collection (Reddit, News, SEC).
    *   Normalization of financial events into a structured stream.
    *   Building the data persistence layer (PostgreSQL/Vector DB).
    *   Grounding agent responses with factual web data.

### 👤 Member 2: The Cognitive Lead
**Core Tool:** **Zynd**
*   **Primary Ownership:** **Agent 2 (Narrative), Agent 3 (Sentiment), Agent 5 (Debate)**
*   **Focus:**
    *   Implementing the Zynd Agent Mesh for inter-agent communication.
    *   Designing the adversarial debate system (Bull/Bear/Arbiter).
    *   Multi-agent reasoning logic and decentralized identity management.
    *   Narrative propagation and emotional momentum modeling.

### 👤 Member 3: The Platform Lead
**Core Tool:** **Superplane**
*   **Primary Ownership:** **Agent 4 (Market Correlation), Agent 6 (Risk), Agent 7 (Strategy), Agent 8 (Visualization)**
*   **Focus:**
    *   Orchestrating the end-to-end event-driven workflows with Superplane.
    *   CI/CD pipelines, agent runtime management, and state transitions.
    *   Developing the real-time Visualization Dashboard (Next.js/React Flow).
    *   Risk-adjusted strategy generation and signal validation.

---

## 🤖 Shared Accelerator: GitHub Copilot
All members leverage Copilot for:
*   **Code Generation:** Fast-tracking boilerplate for FastAPI and Zynd.
*   **Workflow Design:** Planning complex Superplane execution traces.
*   **Repo Context:** Using `@workspace` to ensure cross-agent compatibility.


---

## 🤖 AI-Accelerated Development
**Shared Tool:** **GitHub Copilot**

All team members must utilize GitHub Copilot to maintain high velocity:
*   **Copilot Chat:** For debugging complex logic and generating boilerplate.
*   **Copilot Agents:** To perform repository-wide research and plan multi-file changes.
*   **Copilot Extensions:** For integrating specialized documentation directly into the IDE.

---

## 📂 Project Structure Proposal

To support this division, the repository will be organized as follows:

- `/data`: Apify Actors, scrapers, and data transformation scripts.
- `/agents`: Agent logic, Zynd protocol implementations, and prompt templates.
- `/infra`: Superplane configurations, Dockerfiles, and CI/CD workflows.
- `/docs`: Project documentation and team guidelines.
