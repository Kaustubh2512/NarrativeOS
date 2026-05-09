#!/usr/bin/env bash
# =============================================================================
# NarrativeOS — Production Deployment Script
# Deploys Superplane + all NarrativeOS agents on a single host.
# Usage: ./deploy.sh [--domain narrativeos.example.com]
# =============================================================================
set -euo pipefail

DOMAIN="${1:-}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "=== NarrativeOS Production Deployment ==="

# ── Step 1: Check prerequisites ──────────────────────────────────────────
command -v docker >/dev/null 2>&1 || { echo "Error: Docker not installed"; exit 1; }
command -v docker compose >/dev/null 2>&1 || { echo "Error: Docker Compose not installed"; exit 1; }

# ── Step 2: If domain provided, use official Superplane installer ────────
if [ -n "$DOMAIN" ]; then
    echo "=== Step 2: Running Superplane single-host installer for $DOMAIN ==="

    TMP_DIR=$(mktemp -d)
    cd "$TMP_DIR"
    wget -q https://install.superplane.com/superplane-single-host.tar.gz
    tar -xf superplane-single-host.tar.gz
    cd superplane

    export SUPERPLANE_DOMAIN="$DOMAIN"
    ./install.sh

    echo "=== Superplane installed. Merging NarrativeOS agents... ==="

    # Merge our NarrativeOS services into the generated docker-compose.yml
    # The installer generates docker-compose.yml in the current directory
    GENERATED_COMPOSE="$TMP_DIR/superplane/docker-compose.yml"

    # Append our agent services to the generated compose file
    # We extract the agent services from our project's docker-compose.yml
    python3 -c "
import yaml

# Load generated compose
with open('$GENERATED_COMPOSE') as f:
    compose = yaml.safe_load(f)

# Load our NarrativeOS agent services
with open('$PROJECT_DIR/infra/deploy/docker-compose.yml') as f:
    our_compose = yaml.safe_load(f)

# Merge agent services (skip postgres and superplane — installer provides those)
for svc_name, svc_config in our_compose.get('services', {}).items():
    if svc_name in ('postgres', 'superplane'):
        continue
    compose.setdefault('services', {})[svc_name] = svc_config

# Write merged compose
with open('$GENERATED_COMPOSE', 'w') as f:
    yaml.dump(compose, f, default_flow_style=False)
print('Merged NarrativeOS agents into Superplane stack')
"

    cd "$TMP_DIR/superplane"
    docker compose pull
    docker compose up -d

    # Import canvases
    echo "=== Importing NarrativeOS canvases... ==="
    for canvas in "$PROJECT_DIR/infra/superplane/canvases/"*.yaml; do
        echo "Importing $(basename "$canvas")..."
        superplane canvas import -f "$canvas" 2>/dev/null || \
        docker compose exec -T superplane superplane canvas import -f "/etc/superplane/canvases/$(basename "$canvas")" 2>/dev/null || \
        echo "  (will need manual import via UI at https://$DOMAIN)"
    done

    echo "=== Deployment complete ==="
    echo "Superplane: https://$DOMAIN"
    echo "Dashboard: https://$DOMAIN:5173 (if configured)"
    echo ""
    echo "Next steps:"
    echo "  1. Open https://$DOMAIN and complete the Superplane setup wizard"
    echo "  2. Point Member 1's Apify webhook to https://$DOMAIN/api/v1/webhooks/apify-event"
    echo "  3. Configure Zynd agent URLs in the .env file"

else
    # ── Local / no-domain deployment ──────────────────────────────────────
    echo "=== Step 2: Local deployment (no domain) ==="
    echo "Using docker compose with production Superplane image"

    cd "$PROJECT_DIR/infra/deploy"

    if [ ! -f .env ]; then
        echo "Creating .env from .env.example"
        cp .env.example .env
        echo "⚠️  Edit .env and fill in secrets before running"
    fi

    docker compose pull
    docker compose up -d

    echo ""
    echo "=== Local deployment complete ==="
    echo "Superplane:  http://localhost:3000"
    echo "Dashboard:   http://localhost:5173"
    echo "Correlation: http://localhost:8002"
    echo "Risk:        http://localhost:8003"
    echo "Strategy:    http://localhost:8004"
    echo "Execution:   http://localhost:8005"
    echo "Viz Agent:   http://localhost:8001"
    echo ""
    echo "⚠️  Webhooks from external services (Apify, Zynd) won't reach localhost."
    echo "   Use a tunnel (ngrok, cloudflared) or deploy with --domain <your-domain>"
fi
