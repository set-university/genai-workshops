# INSTALL

## 1. AI Coding Tool (required)

You need **one** AI-powered coding tool installed and authenticated before the workshop.

### Recommended: Claude Code

Claude Code is a VS Code extension (and CLI) by Anthropic. It is the preferred tool for this course since the BMAD method is optimized for it.

Claude Code is included in Claude **Pro** and **Max** subscriptions:

| Plan | Price | Best for |
|------|-------|----------|
| **Pro** | $17/mo (annual) or $20/mo (monthly) | Short coding sprints, small codebases. Sufficient for workshops and capstone. |
| **Max 5x** | $100/mo | Everyday use in larger codebases. 5x more usage than Pro. |
| **Max 20x** | $200/mo | Power users. 20x more usage than Pro. |

**How to get started:**
1. Create an account at [claude.ai](https://claude.ai)
2. Subscribe to the **Pro** plan (minimum required)
3. Install the **Claude Code** extension in VS Code (search "Claude Code" by Anthropic in the Extensions tab)
4. Sign in with your Anthropic account

> [Claude Code product page](https://claude.com/product/claude-code) | [Pricing](https://www.anthropic.com/pricing)

### Alternatives

If you prefer a different tool, any of these will work:

| Tool | Free Tier | Paid Plan | Link |
|------|-----------|-----------|------|
| **Cursor** | Limited agent requests | Pro $20/mo (extended limits, unlimited completions) | [cursor.com](https://www.cursor.com/pricing) |
| **Windsurf** | Unlimited basic usage | Pro $15/mo (500 prompt credits/mo) | [windsurf.com](https://windsurf.com/pricing) |

All three tools support the AI-assisted coding workflow we use in the workshops. Choose one, make sure it works, and you're good to go.

### Web search for market research

The market research workflow (Step 3) requires web search to find competitors and market data.

- **Claude Code with Pro/Max subscription** — WebSearch is built-in. No extra setup needed.
- **Cursor, Windsurf, or Claude Code via API (Bedrock, Console)** — WebSearch is **not** included. You need to set up an MCP server for web search. We recommend [Firecrawl](https://firecrawl.dev):

  1. Register at [firecrawl.dev](https://firecrawl.dev) (free tier: 500 credits, enough for the workshop)
  2. Get your API key from the dashboard
  3. Add Firecrawl MCP to your project by creating `.mcp.json` in your project root:

     ```json
     {
       "mcpServers": {
         "firecrawl": {
           "command": "npx",
           "args": ["-y", "firecrawl-mcp"],
           "env": {
             "FIRECRAWL_API_KEY": "your-api-key-here"
           }
         }
       }
     }
     ```

  4. Restart your AI coding tool — it should detect the MCP server automatically

## 2. Node.js (required)

Install **Node.js 20+** from [nodejs.org](https://nodejs.org). Verify with:

```bash
node --version
```

## 3. BMAD Method (install before Workshop 1)

In your project folder, run:

```bash
npx bmad-method install
```

Verify by opening the folder in your AI coding tool and running `/bmad-help`.

### Verify BMAD

```bash
ls _bmad/
```

Open your AI-powered IDE in the project folder and run:
```
/bmad-help