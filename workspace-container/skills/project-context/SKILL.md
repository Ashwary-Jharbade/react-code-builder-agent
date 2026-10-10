---
name: project-context
description: Establishes the foundational "Mental Tech Stack Model." Before any code is written or modified, the agent must understand the constraints, architecture, and dependencies of the workspace to avoid hallucinating incompatible libraries.
---

**Trigger Conditions:**
- Session initialization / startup.
- Detecting changes to `package.json`, `tsconfig.json`, or bundler configs.

**Execution Protocol:**
1. **Dependency Analysis:** Read `package.json` to extract core libraries (React version, Next.js/Vite, State Management, Styling).
2. **Configuration Parsing:** Read `tsconfig.json` (for strictness and path aliases) and `.env.example` (for required environment variables).
3. **Architecture Identification:** Determine if the project is a Monorepo (Turbo, Nx), Next.js App Router (`app/`), Next.js Pages Router (`pages/`), or a standard SPA (`src/`).
4. **Constraint Generation:** Lock in the identified paradigms (e.g., "This project uses Tailwind; DO NOT generate styled-components CSS-in-JS").

**Rules & Constraints:**
- *Never* suggest installing a new dependency if an existing one in `package.json` solves the problem.
- *Always* respect path aliases (e.g., `@/components/`) defined in `tsconfig.json`.

**Output:** 
A loaded internal context object defining `Stack`, `Styling`, `Routing`, and `State_Paradigm`.