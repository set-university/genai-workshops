# Workshop 1: From Idea to Specs — AI-Assisted Product Definition

**Duration:** 2 hours

Learn how to use BMAD tools to go from a raw idea to implementation-ready product specifications. We'll walk through brainstorming, design thinking, market research, product brief, and PRD — all powered by AI agents.

By the end of this session, you'll have a clear direction for your capstone project — we'll use AI-powered brainstorming to generate ideas tailored to your background and interests, then guide you through selecting the one that best fits the course constraints and your personal goals.

**What to prepare:**
- Have an AI coding tool installed and authenticated. Claude Code (VS Code extension) is preferred; Cursor and Windsurf also work.

**What to bring:**
- Your laptop with the setup completed
- A few sentences about yourself: your role, hobbies, daily frustrations, and any product ideas you've been thinking about — this is the raw material for finding your capstone topic

**What you'll walk away with:**
- A capstone project topic selected (or strong candidates to choose from)
- A complete product specification package (user personas, market analysis, product brief, PRD)
- The ability to run the same process independently for your own project

---

## Step 1: Introduction — What Is BMAD and Why Use It?

### The Problem

When you ask an AI to "help me plan a product," you get a generic wall of text. There's no structure, no follow-up, no quality gate. You end up doing the heavy lifting of figuring out *what to ask*, *in what order*, and *whether the output is good enough*.

### What BMAD Is

**BMAD (BMad Method)** is an open-source framework that gives AI agents structured workflows for building software products — from initial idea through implementation. Think of it as a playbook: instead of free-form prompting, you invoke specific **workflows** that guide the AI through a proven process, producing concrete **artifacts** (documents, specs, plans) at each step.

BMAD installs into your project as a `_bmad/` folder and works inside your AI coding tool (Claude Code, Cursor, Windsurf).

### Key Concepts You Need

| Concept | What It Means |
|---------|--------------|
| **Workflow** | A step-by-step process you invoke with a slash command (e.g., `/bmad-brainstorming`). The AI follows the workflow's instructions, asks you questions, and produces an output artifact. |
| **Agent** | A persona the AI takes on for a workflow — Business Analyst, Product Manager, UX Designer, Architect, etc. Each agent has domain expertise baked into its prompt. |
| **Artifact** | The deliverable a workflow produces — a brainstorming session, product brief, PRD, architecture doc, etc. Artifacts are saved as files and feed into subsequent workflows. |
| **Module** | A collection of related agents and workflows. This workshop uses the **BMM** (Build My MVP) and **CIS** (Creative & Innovation Studio) modules. |
| **`/bmad-help`** | Your navigation command. Run it anytime to see where you are in the process and what to do next. |

### Why This Matters

- **Consistency** — Every run follows the same structured process, so you don't skip steps or forget questions.
- **Quality** — Workflows include validation steps and cross-references between artifacts.
- **Speed** — Instead of crafting prompts from scratch, you invoke a command and the agent drives the conversation.
- **Portability** — The same workflow works across Claude Code, Cursor, and Windsurf.

### How the Workshop Maps to BMAD

In this session we'll run through these workflows in order:

1. **Brainstorming** (`/bmad-brainstorming`) — Generate capstone project ideas based on your background
2. **Design Thinking** (`/bmad-cis-design-thinking`) — Explore user needs and validate your chosen idea
3. **Market Research** (`/bmad-bmm-market-research`) — Understand the competitive landscape
4. **Create Product Brief** (`/bmad-bmm-create-product-brief`) — Lock down the product vision
5. **Create PRD** (`/bmad-bmm-create-prd`) — Produce implementation-ready requirements
6. **Create UX Design** (`/bmad-bmm-create-ux-design`) — Define screens, navigation, and user flows

Each workflow runs in a **fresh context window** (new chat). The output from one step feeds into the next.

### Usefull BMAD Modules and Workflows

To get up to date available commands use `/bmad-help`

Below is the full catalog of what BMAD ships with. This workshop focuses on a subset — but everything here is available for your capstone and beyond.

#### Core — Universal Tools (work across all modules)

| Command | Workflow | Description |
|---------|----------|-------------|
| `/bmad-help` | Help | Get unstuck by showing what workflow steps come next or answering BMAD questions |
| `/bmad-brainstorming` | Brainstorming | Generate diverse ideas through interactive techniques |
| `/bmad-party-mode` | Party Mode | Orchestrate multi-agent discussions for multiple perspectives |
| `/bmad-index-docs` | Index Docs | Create lightweight index for quick LLM scanning of available docs |
| `/bmad-shard-doc` | Shard Document | Split large documents into smaller files by sections |
| `/bmad-editorial-review-prose` | Editorial Review — Prose | Review prose for clarity, tone, and communication issues |
| `/bmad-editorial-review-structure` | Editorial Review — Structure | Propose cuts, reorganization, and simplification |
| `/bmad-review-adversarial-general` | Adversarial Review | Critically review content to find issues and weaknesses |

#### BMM — Build My MVP (the main product development module)

**Phase 1: Analysis**

| Command | Workflow | Agent | Description |
|---------|----------|-------|-------------|
| `/bmad-brainstorming` | Brainstorm Project | 📊 Mary (Business Analyst) | Expert guided brainstorming facilitation |
| `/bmad-bmm-market-research` | Market Research | 📊 Mary (Business Analyst) | Market analysis, competitive landscape, customer needs |
| `/bmad-bmm-domain-research` | Domain Research | 📊 Mary (Business Analyst) | Industry domain deep dive, subject matter expertise |
| `/bmad-bmm-technical-research` | Technical Research | 📊 Mary (Business Analyst) | Technical feasibility, architecture options |
| `/bmad-bmm-create-product-brief` | Create Brief | 📊 Mary (Business Analyst) | Guided experience to nail down your product idea |

**Phase 2: Planning**

| Command | Workflow | Agent | Description |
|---------|----------|-------|-------------|
| `/bmad-bmm-create-prd` | Create PRD *(required)* | 📋 John (Product Manager) | Produce your Product Requirements Document |
| `/bmad-bmm-validate-prd` | Validate PRD | 📋 John (Product Manager) | Validate PRD is comprehensive, lean, and cohesive |
| `/bmad-bmm-edit-prd` | Edit PRD | 📋 John (Product Manager) | Improve and enhance an existing PRD |
| `/bmad-bmm-create-ux-design` | Create UX | 🎨 Sally (UX Designer) | Plan your UX — recommended if UI is a primary piece |

**Phase 3: Solutioning**

| Command | Workflow | Agent | Description |
|---------|----------|-------|-------------|
| `/bmad-bmm-create-architecture` | Create Architecture *(required)* | 🏗️ Winston (Architect) | Document technical decisions and system design |
| `/bmad-bmm-create-epics-and-stories` | Create Epics & Stories *(required)* | 📋 John (Product Manager) | Break the plan into epics and stories |
| `/bmad-bmm-check-implementation-readiness` | Check Readiness *(required)* | 🏗️ Winston (Architect) | Ensure PRD, UX, Architecture, and Stories are aligned |

**Phase 4: Implementation**

| Command | Workflow | Agent | Description |
|---------|----------|-------|-------------|
| `/bmad-bmm-sprint-planning` | Sprint Planning *(required)* | 🏃 Bob (Scrum Master) | Generate sprint plan for development tasks |
| `/bmad-bmm-sprint-status` | Sprint Status | 🏃 Bob (Scrum Master) | Summarize sprint status and route to next workflow |
| `/bmad-bmm-create-story` | Create Story *(required)* | 🏃 Bob (Scrum Master) | Prepare the next story for development |
| `/bmad-bmm-dev-story` | Dev Story *(required)* | 💻 Amelia (Developer) | Execute story implementation tasks and tests |
| `/bmad-bmm-qa-automate` | QA Automation Test | 🧪 Quinn (QA Engineer) | Generate automated API and E2E tests |
| `/bmad-bmm-code-review` | Code Review | 💻 Amelia (Developer) | Review implemented code for quality |
| `/bmad-bmm-retrospective` | Retrospective | 🏃 Bob (Scrum Master) | Review completed work and lessons learned |

**BMM — Anytime Tools**

| Command | Workflow | Agent | Description |
|---------|----------|-------|-------------|
| `/bmad-bmm-document-project` | Document Project | 📊 Mary (Business Analyst) | Analyze an existing project to produce documentation |
| `/bmad-bmm-generate-project-context` | Generate Project Context | 📊 Mary (Business Analyst) | Scan codebase to generate LLM-optimized project context |
| `/bmad-bmm-quick-spec` | Quick Spec | 🚀 Barry (Quick Flow Solo Dev) | Quick one-off tasks without extensive planning |
| `/bmad-bmm-quick-dev` | Quick Dev | 🚀 Barry (Quick Flow Solo Dev) | Quick implementation without full workflow |
| `/bmad-bmm-correct-course` | Correct Course | 🏃 Bob (Scrum Master) | Navigate significant changes mid-project |

#### CIS — Creative & Innovation Studio

| Command | Workflow | Agent | Description |
|---------|----------|-------|-------------|
| `/bmad-cis-innovation-strategy` | Innovation Strategy | ⚡ Victor (Disruptive Innovation Oracle) | Identify disruption opportunities and business model innovation |
| `/bmad-cis-problem-solving` | Problem Solving | 🔬 Dr. Quinn (Master Problem Solver) | Systematic problem-solving methodologies |
| `/bmad-cis-design-thinking` | Design Thinking | 🎨 Maya (Design Thinking Maestro) | Human-centered design using empathy-driven methods |
| `/bmad-cis-brainstorming` | Brainstorming | 🧠 Carson (Elite Brainstorming Specialist) | Facilitate brainstorming sessions with multiple techniques |
| `/bmad-cis-storytelling` | Storytelling | 📖 Sophia (Master Storyteller) | Craft compelling narratives using story frameworks |


