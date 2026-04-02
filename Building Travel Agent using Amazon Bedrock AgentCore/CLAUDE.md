# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A multi-agent travel concierge AI system built on AWS Bedrock AgentCore. A **Supervisor Agent** orchestrates two specialized sub-agents (Travel, Cart) via AgentCore Gateway with M2M OAuth2 authentication. The frontend is a React/TypeScript app using Amplify.

## Commands

### Install
```bash
npm install
cd amplify && npm install && cd ..
```

### Local Development
```bash
npm run dev          # Start frontend dev server at https://vcas.local.com:9000/
npm run build        # Build web UI for production
```

### Deployment (order matters)
```bash
npm run deploy:amplify      # 1st: Cognito, DynamoDB, AppSync (~4 min)
npm run deploy:mcp          # 2nd: Cart, Travel, Itinerary MCP servers (~60 sec)
npm run deploy:agent        # 3rd: Supervisor agent runtime (~4 min)
npm run deploy:frontend     # 4th: Web UI to Amplify Hosting (~3 min, optional)
npm run deploy              # All of the above in sequence
```

### Cleanup
```bash
npm run clean               # Delete all AWS resources
npm run clean:amplify / clean:mcp / clean:agent / clean:frontend
```

### Optional Setup
```bash
./scripts/set-api-keys.sh           # Configure SerpAPI, etc.
./scripts/export-visa-secrets.sh    # Setup Visa payment credentials
```

## Architecture

### Multi-Agent Topology
```
Web UI (React/Vite)
    └── Supervisor Agent (Docker, Python 3.13, Strands SDK)
            ├── Travel Agent (Docker) — weather, flights, hotels, places, search
            └── Cart Agent (Docker) — cart ops, Visa tokenization, purchase flow
```

All agent-to-agent calls go through **AgentCore Gateway** using M2M OAuth2 (Cognito client credentials). Each agent exposes tools via the **MCP Protocol**.

### Key Stacks (AWS CDK, TypeScript)
- `infrastructure/agent-stack/` — Supervisor agent runtime, AgentCore Memory, Gateway, OAuth scopes
- `infrastructure/mcp-servers/` — Travel, Cart, Itinerary MCP runtime stacks (separate deployable units)
- `infrastructure/frontend-stack/` — Amplify Hosting + CloudFront
- `infrastructure/visa-lambda-stack/` — Optional Visa API proxy Lambda

### State & Persistence
- **DynamoDB** — user profiles, wishlists, itineraries, feedback (tables provisioned in Amplify stack)
- **AgentCore Memory** — multi-turn conversation history (injected as `MEMORY_ID` env var)
- **AWS Secrets Manager** — Visa payment credentials

### Frontend (`web-ui/src/`)
- React 18 + TypeScript + Vite + Tailwind CSS
- AWS Amplify UI for auth (Cognito JWT)
- Bedrock AgentCore SDK for real-time streaming agent responses
- Split layout: main chat + tabbed sidebar (itinerary/cart/profile) + dynamic map

### Payment
- Visa VTS (tokenization) + VIC (orchestration)
- **Mock mode is the default** — works without Visa credentials, toggled via feature flag
- Visa Lambda proxy (`infrastructure/visa-lambda-stack/`) for production; local server (`concierge_agent/local-visa-server/`) for development

### Python Agents (`concierge_agent/`)
- Package manager: **UV** (not pip)
- Container base: Python 3.13 slim, non-root user `bedrock_agentcore:1000`
- OpenTelemetry auto-instrumentation included

### Auto-Generated Files (do not edit manually)
- `amplify_outputs.json` — populated by `deploy:amplify`
- `web-ui/.env.local` — populated by `scripts/setup-web-ui-env.sh`

### Deployment Identity
- `deployment-config.json` — contains a unique `deploymentId` enabling multiple independent deployments per AWS account

## Key Documentation
- `DEPLOYMENT.md` — step-by-step deployment walkthrough
- `docs/AGENT_CAPABILITIES.md` — full list of 18 tools across all agents
- `docs/FRONTEND_MOCK_MODE.md` — testing frontend without backend
- `infrastructure/README.md` — CDK stack details
