# Aegis AI Auditor

> Ship LLM products with confidence: find prompt injection, unsafe agent actions, leaked credentials, and governance gaps before they ship.

**Aegis AI Auditor** is a premium micro-SaaS foundation for AI security governance and deterministic vulnerability scanning across LLM applications, RAG systems, prompt chains, and agentic workflows. It converts risky code and workflow patterns into a prioritized risk score, evidence-backed findings, and clear remediation guidance aligned to the **OWASP Top 10 for LLM Applications** and the **NIST AI Risk Management Framework**.

## Why buyers care

The rapid enterprise adoption of generative AI has created a durable security category: organizations need practical controls around prompt injection, data exposure, unsafe tool use, and ungoverned agent behavior. Aegis provides a focused, easy-to-demo product wedge for that market.

### Core value proposition

- **Security signal in seconds:** paste a workflow or source code and receive a 0–100 risk score with Low, Medium, or High posture.
- **AI-native coverage:** detects prompt-injection indicators, hardcoded credentials, system-prompt exposure, dangerous `eval()` usage, command execution, risky outbound requests, weak safety configuration, and RAG trust-boundary signals.
- **Actionable remediation:** every finding includes severity, evidence, location, applicable framework context, and a specific mitigation.
- **Built to extend:** the deterministic rule engine is intentionally modular, making it straightforward to add custom enterprise policies, repository scanning, CI integrations, and paid compliance reports.

## Product preview

Aegis includes:

- A polished dark-mode Next.js marketing site and audit dashboard.
- A FastAPI backend with CORS enabled for local frontend development.
- SQLite persistence for users and scan records.
- Registration and development-session login endpoints.
- A deterministic, explainable scanning engine that avoids opaque findings.
- Findings mapped to relevant OWASP LLM and NIST AI RMF themes.

## Architecture

| Layer | Technology | Responsibility |
| --- | --- | --- |
| Web product | Next.js App Router, React, TypeScript | Premium landing page and interactive audit dashboard |
| Styling | Tailwind CSS, Lucide | Responsive security-product UI and iconography |
| API | FastAPI, Pydantic | Typed REST API, input validation, CORS |
| Data | SQLAlchemy, SQLite | User and scan-history persistence |
| Security engine | Python deterministic rules | Pattern detection, risk scoring, remediation generation |

## Repository layout

```text
aegis-ai-auditor/
├── backend/
│   ├── requirements.txt
│   ├── database.py
│   ├── models.py
│   ├── main.py
│   └── scanner.py
├── frontend/
│   ├── package.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── src/app/
│       ├── globals.css
│       ├── layout.tsx
│       ├── page.tsx
│       └── dashboard/page.tsx
└── README.md
```

## Quick local setup

### 1. Start the API

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

The API is now available at `http://localhost:8000`, with interactive API documentation at `http://localhost:8000/docs`.

### 2. Start the frontend

Open a second terminal:

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`, select **Run a free audit**, and submit a workflow or code snippet. The included sample demonstrates multiple scanner detections immediately.

### Optional frontend API configuration

The dashboard defaults to `http://localhost:8000`. For a deployed API, add a `frontend/.env.local` file:

```bash
NEXT_PUBLIC_API_URL=https://your-api-domain.example
```

## API contract

### `POST /api/register`

```json
{
  "email": "founder@example.com",
  "password": "secure-password"
}
```

### `POST /api/login`

```json
{
  "email": "founder@example.com",
  "password": "secure-password"
}
```

This product build returns an ephemeral development session token. Replace it with signed JWTs, password hashing such as Argon2 or bcrypt, and production rate limiting before exposing authentication publicly.

### `POST /api/scan`

```json
{
  "target_text": "SYSTEM_PROMPT = '...'\neval(user_input)"
}
```

The response contains a persistent `scan_id`, timestamp, risk score, severity breakdown, structured findings, and recommended action.

## Monetization thesis

Aegis can support several high-margin revenue paths:

- **Self-serve SaaS:** price by monthly scans, connected repositories, team seats, or monitored AI applications.
- **Developer and CI tiers:** sell GitHub/GitLab checks, pull-request comments, policy-as-code rules, and release gates.
- **Enterprise governance:** charge for SSO, audit logs, custom rule packs, private deployment, retention policies, and compliance exports.
- **Professional services:** offer AI security posture assessments, red-team prompt testing, remediation workshops, and implementation retainers.
- **API-first platform:** expose paid scan endpoints for AI development platforms, consultancies, and internal developer portals.

### High-value expansion roadmap

1. Add JWT/SSO, Argon2 password hashing, rate limiting, tenant isolation, and role-based access control.
2. Introduce repository ingestion, GitHub/GitLab apps, pull-request annotations, and CI/CD policy gates.
3. Add model-driven semantic analysis alongside deterministic rules, with human-review workflows for false-positive triage.
4. Build scheduled monitoring, evidence retention, PDF compliance reports, and executive risk dashboards.
5. Offer integrations for LangChain, LangGraph, OpenAI, Anthropic, AWS Bedrock, Azure AI, Datadog, and SIEM platforms.

## Production hardening checklist

Before a public launch, implement the following controls:

- Move SQLite to managed Postgres and add migrations.
- Replace development login behavior with verified email flow, Argon2/bcrypt hashing, JWT rotation, and secure cookie handling.
- Restrict CORS to the deployed frontend domain.
- Add API rate limits, request IDs, structured logs, monitoring, alerting, and error tracking.
- Encrypt sensitive stored inputs, define retention limits, and redact detected secrets from persisted evidence.
- Run scans asynchronously through a queue for large repositories and long-running analysis.
- Add test coverage, dependency scanning, containerization, infrastructure-as-code, and continuous deployment checks.

## Positioning

Aegis AI Auditor is positioned at the intersection of AI application development, DevSecOps, and emerging AI governance. It is ideal for teams building copilots, RAG assistants, autonomous agents, internal LLM tools, and customer-facing AI features that need a tangible security control before enterprise rollout.

---

Built for founders and security-conscious AI teams that want to make AI governance operational—not theoretical.
