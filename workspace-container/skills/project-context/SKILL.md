---
name: project-context
description: Establishes the foundational "Mental Tech Stack Model." Before any code is written or modified, the agent must understand the constraints, architecture, and dependencies of the workspace to avoid hallucinating incompatible libraries.
---

# 1. Purpose
This is the **FIRST** core project-level skill activated immediately following `workspace-orientation`. It builds the agent's internal mental model of the project. A deep agent cannot safely write code until it knows the target framework, styling paradigm, state management approach, and configuration rules of the specific project within `/workspace`. 

# 2. Trigger Conditions
- **Session Initialization:** Always run at the start of a session after the workspace is oriented.
- **Project Switch:** When the user directs focus to a different project or package within a monorepo.
- **Configuration Changes:** Detecting changes (via user instruction or observed Git diffs) to `package.json`, `tsconfig.json`, `jsconfig.json`, bundler configs (e.g., `vite.config.ts`, `next.config.js`), or lock files.
- **Technology Mentions:** When the user mentions a specific technology or library (e.g., "let's use Zustand for this") to verify if it's already installed or needs to be added.

# 3. Discovery Protocol
To build the mental model, execute the following steps using file reading tools or `run_command` (e.g., `cat`, `grep`, `jq` if available, though direct file reading is preferred):

1. **Read `package.json`**: Extract `dependencies`, `devDependencies`, `scripts`, and custom metadata.
2. **Read Config Files**: 
   - Check for `tsconfig.json` or `jsconfig.json`.
   - Check for bundler configs: `vite.config.*`, `next.config.*`, `webpack.config.*`, `rollup.config.*`.
3. **Check Environment Variables**: Inspect `.env.example` or `.env.template` to understand required configuration. *Do not expose sensitive values from `.env` or `.env.local`.*
4. **Identify Lock Files**: Look for package manager lock files at the project or workspace root.

# 4. Framework Detection
Analyze the dependencies and file structure to determine the React framework:
- **Next.js**: Look for `next` in dependencies. 
  - *App Router*: Check for an `app/` directory (e.g., `src/app/` or `app/`).
  - *Pages Router*: Check for a `pages/` directory.
- **Vite**: Look for `vite` in devDependencies and `vite.config.ts`/`js`.
- **Remix**: Look for `@remix-run/react`.
- **Gatsby**: Look for `gatsby`.
- **Create React App (CRA)**: Look for `react-scripts`.
- **Plain React**: React is present, but no specific meta-framework is found (often bundled with Webpack, Parcel, or Rollup).

# 5. Styling Detection
Identify the primary styling paradigm to ensure consistency:
- **Tailwind CSS**: Look for `tailwindcss` and `tailwind.config.js`/`ts`.
- **CSS Modules**: Look for `.module.css` or `.module.scss` files in the codebase.
- **CSS-in-JS (styled-components)**: Look for `styled-components`.
- **CSS-in-JS (Emotion)**: Look for `@emotion/react` and `@emotion/styled`.
- **Sass/SCSS**: Look for `sass` in dependencies and `.scss` files.
- **Plain CSS**: Standard `.css` imports.
- **UI Libraries**: Note if `lucide-react`, `@mui/material`, `antd`, `@radix-ui/*`, or `framer-motion` are present.

# 6. State Management Detection
Identify how state and data fetching are handled:
- **Redux**: Look for `@reduxjs/toolkit` or `redux`.
- **Zustand**: Look for `zustand`.
- **Jotai**: Look for `jotai`.
- **Recoil**: Look for `recoil`.
- **Data Fetching/Async State**: Look for `@tanstack/react-query` (React Query), `swr`, or Apollo Client (`@apollo/client`).
- **Context API**: If no external libraries are found, assume React Context and Hooks (`useState`, `useReducer`) are the default.

# 7. Package Manager Detection
Determine the package manager by looking for lock files:
- **npm**: `package-lock.json`
- **Yarn**: `yarn.lock`
- **pnpm**: `pnpm-lock.yaml`
- **Bun**: `bun.lockb` or `bun.lock`
*Constraint: Always use the identified package manager for any install commands.*

# 8. TypeScript vs JavaScript Detection
- **TypeScript**: `typescript` is in devDependencies, `tsconfig.json` exists, and files use `.ts`/`.tsx` extensions.
- **JavaScript**: No `tsconfig.json`, files use `.js`/`.jsx`.
*Constraint: Strictly adhere to the detected language. Do not write `.tsx` in a pure JavaScript project, and ensure types are provided in a TypeScript project.*

# 9. Path Alias Resolution
Parse `tsconfig.json` or `jsconfig.json` for the `compilerOptions.paths` mapping.
- Example: If `"@/*": ["./src/*"]` is defined, recognize that `@/components/Button` resolves to `src/components/Button`.
*Constraint: Always use defined path aliases when generating new imports instead of relative paths (e.g., `../../components/Button`), unless relative paths are the established convention in that specific directory.*

# 10. Constraint Generation
Based on the discovery phase, lock in hard constraints for the session:
1. **No Hallucinated Dependencies**: Do not suggest or use libraries not in `package.json` unless explicitly requested by the user and formally installed.
2. **Paradigm Adherence**: If the project uses Tailwind, do not generate inline styles or CSS-in-JS. If it uses App Router, do not generate `getServerSideProps`.
3. **Package Manager Fidelity**: Only execute install commands using the detected package manager.
4. **Strict Typing**: If TypeScript is detected, any new code must include proper typing and interfaces. Avoid `any`.

# 11. Context Object Schema
Maintain a mental model (or physical scratchpad) matching this schema:
```json
{
  "projectType": "Next.js (App Router)",
  "language": "TypeScript",
  "packageManager": "pnpm",
  "styling": ["Tailwind CSS", "Radix UI primitives"],
  "stateManagement": ["Zustand", "React Query"],
  "pathAliases": { "@": "./src" },
  "keyConstraints": [
    "Use server components by default, 'use client' only when necessary",
    "Style strictly with Tailwind classes"
  ]
}
```

# 12. Anti-patterns (What NOT to do)
- **Do not mix paradigms**: e.g., adding `styled-components` code to a strict Tailwind project.
- **Do not ignore the package manager**: Running `npm install` in a `pnpm` workspace can break the lockfile.
- **Do not guess file locations**: Rely on the identified root (`src/` vs `app/`) and path aliases.
- **Do not install duplicate tools**: If `swr` is present, do not install `react-query` to solve a data-fetching problem.

# 13. Relationship to Downstream Skills
- **`requirement-analysis`**: Uses the project context to ensure proposed features are technically feasible with the current stack.
- **`codebase-search`**: Uses the root directories (`src/`, `app/`) and path aliases to focus searches.
- **`implementation`**: Relies on the constraints (Styling, State, TypeScript) to write accurate, idiomatic code.
- **`react-patterns`**: Filters patterns based on the framework (e.g., Next.js vs Vite).