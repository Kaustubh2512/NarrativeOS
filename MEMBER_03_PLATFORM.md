# Member 3: The Platform Lead (Superplane)

You own the **execution and orchestration layer** of NarrativeOS. You build the control plane that ties data ingestion, agent reasoning, and signal generation into reliable event-driven workflows.

## Domain

```
/infra/
├── superplane/
│   ├── canvases/       # YAML/JSON canvas definitions
│   ├── components/     # Custom component node configs
│   └── secrets/        # Encrypted credential configs
├── monitoring/         # Grafana dashboards, PagerDuty alerts
├── deploy/             # Dockerfiles, CI/CD pipelines
└── dashboard/          # Next.js/React Flow frontend
```

## Core Tool: Superplane — Full Feature Map

| Feature | How You Use It |
|---------|----------------|
| **Canvas** (visual workflow editor) | Model the full NarrativeOS pipeline visually: Apify ingest → normalize → Zynd analysis → debate → risk check → signal output |
| **Component Nodes** (50+ integrations) | Connect GitHub (auto-deploy), Grafana/Datadog (monitoring), Slack/Discord (alerts), PagerDuty (incidents), OpenAI/Claude (LLM calls within canvas), HTTP Request (APIs) |
| **Data flow + Message chains** | Payload flows between canvas nodes — Apify dataset output → normalized JSON → Zynd agent input → analysis result → signal |
| **Human-in-the-loop** | Pause pipeline before trade execution for manual approval; collect decisions and resume automatically |
| **Expressions + Expression Functions** | Transform and route data between pipeline stages (e.g., `$['Ingest'].data.body | to_upper`) |
| **Canvas Memory** | Persist narrative context across multi-hour analysis runs so agents don't lose state |
| **RBAC + Service Accounts** | Separate access for each team member + read-only monitoring accounts |
| **Secrets management** | Store all API keys (Apify token, Zynd keys, OpenAI keys, exchange credentials) centrally |
| **Scheduling** | Recurring pipeline runs (market-open analysis at 9:30 AM ET, hourly narrative check) |
| **CLI** | Trigger workflows manually for debugging, inspect run history, replay failed steps |
| **LLM/agent tooling** (Skills repo) | AI-assisted canvas design and pipeline debugging |
| **Self-hosted install** | Run Superplane on your own infra (Docker, K8s, EC2, GCP) |
| **Public API** | Programmatic canvas creation, run triggering, and run history queries |
| **Beacon** | Lightweight Superplane agent for edge deployment |

## Sprint 1 Tasks

1. Deploy Superplane locally (Docker) — `docker pull ghcr.io/superplanehq/superplane-demo:stable`
2. Explore the UI — create a test canvas with Manual Run → HTTP Request → If → NoOp to understand the mental model
3. Plan canvas architecture:
   - **Ingress Canvas**: Apify webhook receiver → data normalization → store in dataset
   - **Analysis Canvas**: Trigger → feed NarrativeEvents to Zynd agents → collect AnalysisSignals
   - **Execution Canvas**: Risk check → Human approval (HITL) → Signal output → Notification
4. Build **Ingress Canvas**: webhook trigger → HTTP Request node (fetch Apify dataset) → Expression node (normalize) → NoOp (store)
5. Set up **GitHub Component Node** — auto-build and deploy when code is pushed to main
6. Set up **Slack Component Node** — notify team on pipeline failures and new BUY/SELL signals
7. Set up **RBAC** — 3 accounts (one per member) + read-only viewer
8. Set up **PagerDuty integration** for critical pipeline failures
9. Build **Ingest → Analysis** canvas linking (Apify dataset → Zynd agent webhook)
10. Write infrastructure-as-code for Superplane deployment (`docker-compose.yml`, env configs)

## Deliverables

- Running Superplane instance (local or cloud)
- 3 operational canvases (Ingest, Analyze, Execute) connected end-to-end
- GitHub CI/CD integration (push → build → deploy)
- Slack/Discord alerting on pipeline events
- RBAC configured for 3 team members
- Grafana dashboard for pipeline observability

## API Contract (Consumed)

Relays `NarrativeEvent` from Member 1 to Member 2, and `AnalysisSignal` from Member 2 to output. Uses Superplane expressions to transform data between pipeline stages as needed. See `API_CONTRACT.md` for schema definitions.

## Dependencies

- Needs Member 1's Apify webhook URL to configure the Ingress Canvas trigger
- Needs Member 2's agent webhook endpoints to pipe data into analysis
- Needs both members to provide API keys for secrets management

## GitHub Copilot Usage

- Use **Copilot Chat** with `@workspace` to understand event schemas across the repo
- Use **Copilot** to generate Superplane canvas YAML configurations
- Use **Copilot** for Dockerfile and CI/CD pipeline scripts
- Use **Copilot** for the Next.js/React Flow dashboard boilerplate
- Use **Copilot Agents** for repo-wide refactors when pipeline contracts change
