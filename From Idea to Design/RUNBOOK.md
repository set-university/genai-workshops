# Workshop Runbook — From Idea to Specs

Step-by-step instructions to follow during the workshop. Each step runs in a **fresh context window** (new chat).

---

## Step 1: Brainstorming

Run `/bmad-brainstorming` in a new chat.

When the agent asks about your background and goals, also **paste the constraints block** below so the ideas it generates are realistic for the course.

### Brainstorming Constraints — What to Tell the AI

Copy-paste the relevant block into the brainstorming session when prompted for context.

#### Workshop Project Prompt (copy-paste into brainstorming, fill in your details)

```
I need to find a product idea for my workshop project. Here are the constraints:

ABOUT ME:
- My role: [e.g., software engineer, data analyst, marketing manager, student...]
- My interests/hobbies: [e.g., cooking, gym, dogs, photography, gaming...]
- My daily frustrations: [e.g., I forget what I eat, I lose track of job applications, I never review my notes...]
- Domain I know well: [e.g., healthcare, finance, education, e-commerce...]

PRODUCT CONSTRAINTS:
- It must NOT be just a wrapper around ChatGPT — if a user can get the same result by pasting text into ChatGPT, it's not a product
- It must store and use MY data — the app needs a database and should get more valuable the more I use it
- It should solve a real problem that I or people around me actually have
- It should be buildable as an MVP with a basic frontend, a backend, and a database

TECHNICAL CONSTRAINTS:
- Single LLM API calls (OpenAI, Anthropic, etc.) — no multi-step agent orchestration
- Simple prompt engineering — system prompts, few-shot examples, structured output
- Basic frontend + backend + database (Streamlit/Gradio or simple web app with a DB)
- No RAG (Retrieval-Augmented Generation) — no vector databases, no document indexing — you can use mockup data
- No autonomous AI agents, no tool use, no function calling chains
- No fine-tuning or model training

EVALUATION CRITERIA:
- Can it be built as an MVP with a frontend, backend, database, and a single LLM API call?
- Does it store user data and get more valuable over time (not a stateless ChatGPT wrapper)?
- Does it solve a real problem I care about?
- Is the scope small enough to finish, but interesting enough to learn from?

IDEA SEEDS (optional — use if you're stuck):
- "I track my spending in a spreadsheet but never learn from it. I want something that remembers my transactions and tells me where my money actually goes."
- "I'm applying to jobs and keep losing track of what I applied to and what I said. I want an app that keeps my history and helps me prep for each one."
- "I take notes every day but never review them. I want something that stores my notes and helps me see patterns or quiz myself later."
- "I cook the same 5 meals every week. I want something that remembers what I eat, learns my taste, and suggests new recipes based on what's in my fridge."
- "I'm learning a new language and keep forgetting vocabulary. I want an app that tracks the words I struggle with and generates practice exercises from my weak spots."
```

#### Capstone Project Constraints (for your final project)

> **Scope:** The capstone is your main course deliverable — a real GenAI application that demonstrates what you've learned across all workshops. You will have significantly more time and will learn advanced techniques throughout the course.
>
> **What you'll learn before the capstone:**
> - **Agentic AI** — multi-step reasoning, tool use, function calling, agent loops
> - **RAG (Retrieval-Augmented Generation)** — vector databases, document chunking, embedding models, retrieval pipelines
> - **Frameworks** — LangChain, LlamaIndex, CrewAI, or similar orchestration frameworks
> - **Evaluation & testing & Security** — LLM output evaluation, prompt testing, guardrails
> - **Production patterns** — error handling, cost management, streaming, caching
>
> **Technical scope (what's available for the capstone):**
> - Multi-step AI agents with tool use and function calling
> - RAG pipelines with vector stores (Pinecone, Chroma, pgvector, etc.)
> - GenAI Data processing pipelines
> - Multi-agent systems and orchestration
> - Structured workflows with conditional logic
> - Integration with external APIs and data sources
> - Proper UI with state management
>
> **Good capstone project examples:**
> - A domain-specific research assistant that retrieves and synthesizes information from your own document corpus (RAG)
> - An AI agent that automates a multi-step workflow in your field (e.g., code review pipeline, contract analysis, onboarding assistant)
> - A multi-agent system where specialized agents collaborate (e.g., analyst + writer + reviewer)
> - A tool-augmented assistant that can query databases, call APIs, and produce reports
>
> **Evaluation criteria for idea selection:**
> - Does it use at least one advanced GenAI pattern (RAG, agents, tool use)?
> - Does it solve a meaningful problem in your domain?
> - Is it demonstrable — can you show it working end-to-end?
> - Is the scope realistic for an individual project with the techniques you'll learn?

#### How to Use These Constraints

**During today's brainstorming**, paste the **Workshop Project Constraints** block when the agent asks for context. This ensures ideas stay within the simplified scope.

**When evaluating ideas**, consider both tracks: pick a workshop project you can build today *and* note which ideas could grow into a full capstone later. Many good capstone projects start as a simple workshop prototype and expand once you learn RAG and agents.

---

## Step 2: Design Thinking

Run `/bmad-cis-design-thinking` in a new chat.

**What this does:** Walks you through empathy mapping, user personas, and pain point analysis. You'll define who your user is, what frustrates them, and how your product fits into their life.

**What to provide:** Paste your brainstorming output (the idea you picked). The agent will ask follow-up questions about the target user.

**What you'll get:** A design thinking document with user personas, empathy maps, and validated problem-solution fit.

**Tip:** When the agent asks about the user, think about a real person you know (including yourself). Concrete details produce better personas than abstract descriptions.

---

## Step 3: Market Research

Run `/bmad-bmm-market-research` in a new chat.

**What this does:** Analyzes the competitive landscape — who else solves this problem, how, and where the gaps are. Identifies your differentiation.

**What to provide:** Paste your brainstorming output and design thinking document. The agent uses these to focus the research on the right market.

**What you'll get:** A market research document with competitor analysis, market positioning, and opportunity gaps.

**Tip:** Don't skip this even if your idea feels unique. The agent will find adjacent solutions you haven't thought of, which helps sharpen your positioning and avoid blind spots.

---

## Step 4: Create Product Brief

Run `/bmad-bmm-create-product-brief` in a new chat.

**What this does:** Consolidates everything from Steps 1–3 into a concise product vision. Defines the problem statement, target audience, key features, success metrics, and scope boundaries.

**What to provide:** Paste your brainstorming output, design thinking document, and market research. The agent synthesizes all three.

**What you'll get:** A product brief — a one-document summary of what you're building, for whom, and why. This becomes the source of truth for everything that follows.

**Tip:** Be ruthless about scope here. The agent may suggest features — push back on anything that goes beyond a single LLM API call + database. The brief should describe an MVP you can actually build.

---

## Step 5: Create PRD

Run `/bmad-bmm-create-prd` in a new chat.

**What this does:** Turns the product brief into a detailed Product Requirements Document — functional requirements, user stories, data model, API surface, and acceptance criteria.

**What to provide:** Paste your product brief. The agent will ask clarifying questions to fill in the details.

**What you'll get:** A PRD with enough detail for an AI coding tool to implement the app in Workshop 2.

**Tip:** The PRD is the main input for Workshop 2 (architecture, stories, coding). Make sure it includes: what data gets stored, what the LLM does with that data, and what the user sees. If any of these three are vague, push the agent to be more specific.

---

## Step 6: Create UX Design

Run `/bmad-bmm-create-ux-design` in a new chat.

**What this does:** Defines the user interface — screens, navigation flow, layout, and key interactions. Produces wireframe descriptions and user flow diagrams that the developer agent can follow in Workshop 2.

**What to provide:** Paste your PRD. The agent uses the requirements to design screens and flows.

**What you'll get:** A UX design document with screen descriptions, user flows, and interaction patterns. This tells the AI *what to build* visually when it gets to implementation.

**Tip:** For a workshop-scoped app, keep it to 3–5 screens max. Think: a main input screen, a results/dashboard screen, and maybe a history/settings screen. The agent may over-design — remind it this is an MVP.