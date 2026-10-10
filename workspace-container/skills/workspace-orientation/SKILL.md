---
name: workspace-orientation
description: Foundational skill that explains the role, boundaries, and discovery techniques for the /workspace directory — the user's interactive play area for React project development. Use this skill before any other skill when starting a new task, when the agent needs to understand where to operate, or when discovering projects, files, and folders inside the workspace.
---

# Workspace Orientation

## Purpose

This skill tells the agent **what** the `/workspace` directory is, **why** it exists, and **how** to explore it. Every task the agent performs ultimately targets content inside this directory.

---

# 1. What Is `/workspace`?

`/workspace` (physical path: `workspace-container/workspace`) is the **user's interactive play area**.

It is the single directory where:

- users create, modify, and manage their projects
- the agent reads, writes, and executes code
- all file operations take place

Think of `/workspace` as the agent's **entire visible universe**. Nothing outside it should be created, modified, or deleted unless the user explicitly provides a path outside and confirms the intention.

---

# 2. What Lives Inside `/workspace`?

The directory typically contains one or more **React projects** (though other project types may appear). Each project is a self-contained application with its own dependencies and configuration.

Example layout:

```text
/workspace/
├── todo-list/          ← a Create React App project
│   ├── package.json
│   ├── public/
│   └── src/
│       ├── App.js
│       ├── index.js
│       └── ...
├── dashboard/          ← another project (may or may not exist yet)
│   ├── package.json
│   └── src/
└── landing-page/       ← yet another project
    ├── package.json
    └── src/
```

The workspace may start empty, contain a single project, or hold many projects. Never assume a fixed layout — always discover.

---

# 3. Hard Boundary Rule

## All agent actions MUST stay inside `/workspace`

```text
✅  /workspace/todo-list/src/App.js
✅  /workspace/new-project/package.json
❌  /home/user/other-project/src/App.js
❌  /tmp/scratch/file.js
❌  ../some-other-folder/file.js
```

This applies to:

- creating files and folders
- editing or deleting files
- running build/dev/test commands
- installing dependencies

If the user's request implies a path outside `/workspace`, **ask for clarification** rather than operating outside the boundary.

---

# 4. Discovery Protocol

Before taking any action, the agent **must discover** what currently exists in `/workspace`. Do not assume the workspace is empty or that a particular project exists.

## 4.1 List Top-Level Projects

Start every task by listing the immediate children of `/workspace`:

```bash
ls -la /workspace/
```

This reveals which projects (or empty directories) are present.

## 4.2 Identify a React Project

A directory is likely a React project if it contains:

| Signal File / Folder     | Indicates                        |
|--------------------------|----------------------------------|
| `package.json`           | Node.js project                  |
| `src/`                   | Source directory                  |
| `public/index.html`      | Create React App or static SPA   |
| `vite.config.*`          | Vite-based React project         |
| `next.config.*`          | Next.js project                  |
| `tsconfig.json`          | TypeScript configured            |
| `node_modules/`          | Dependencies installed            |

To confirm React specifically, check `package.json` for `react` in `dependencies` or `devDependencies`:

```bash
cat /workspace/<project>/package.json | grep -A2 '"react"'
```

## 4.3 Explore Project Structure (Non-Exhaustive)

Use targeted inspection — not recursive dumps:

```bash
# Top-level project layout
ls -la /workspace/<project>/

# Source directory structure (one level)
ls -la /workspace/<project>/src/

# Deeper drill-down only when needed
ls -la /workspace/<project>/src/components/
```

**Never run:**

```bash
# ❌ These produce excessive output and waste tokens
ls -R /workspace/
find /workspace/ -type f
tree /workspace/
cat -r /workspace/
```

Avoid reading `node_modules/`, `.git/`, `build/`, or `dist/` unless the user specifically asks.

## 4.4 Search for a Specific File or Pattern

When looking for a particular file, component, or code pattern:

```bash
# Find a file by name
find /workspace/<project> -name "App.js" -not -path "*/node_modules/*"

# Find files containing a keyword (e.g., a component name)
grep -rl "TodoItem" /workspace/<project>/src/ --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx"

# Find all component files
find /workspace/<project>/src -name "*.jsx" -o -name "*.tsx" | grep -v node_modules
```

Always exclude `node_modules`, `.git`, `build`, and `dist` from searches.

## 4.5 Discover Installed Dependencies

```bash
# Read the full dependency list
cat /workspace/<project>/package.json
```

Or for a quick check:

```bash
# Check if a specific package is installed
grep '"react-router"' /workspace/<project>/package.json
```

## 4.6 Check If Dependencies Are Installed

```bash
# Does node_modules exist?
ls /workspace/<project>/node_modules/ > /dev/null 2>&1 && echo "installed" || echo "not installed"
```

If `node_modules` is missing, the agent should install dependencies before running build/dev/test commands:

```bash
cd /workspace/<project> && npm install
```

---

# 5. Single Project vs. Multiple Projects

## Single Project

When `/workspace` contains exactly one project, treat it as the default target for all user requests.

```text
/workspace/
└── todo-list/
```

No ambiguity — all operations target `todo-list`.

## Multiple Projects

When multiple projects exist, the agent **must identify the correct target** before acting.

Use these signals (in priority order):

1. **Explicit mention** — user names the project: _"Fix the dashboard header"_
2. **Explicit path** — user provides a path: _"Edit /workspace/todo-list/src/App.js"_
3. **Feature context** — search projects for the relevant code
4. **Recent context** — the project most recently worked on in the conversation

If the target is still ambiguous, **ask the user**.

---

# 6. Empty Workspace

If `/workspace` is empty, the user is starting from scratch. The agent should:

1. Confirm the user's intent (e.g., _"Would you like me to create a new React project?"_)
2. Ask for a project name if not provided
3. Scaffold the project **inside `/workspace/`**:

```bash
cd /workspace && npx create-react-app <project-name>
```

or with Vite:

```bash
cd /workspace && npm create vite@latest <project-name> -- --template react
```

Never scaffold a project at `/workspace` root level (i.e., dumping files directly into `/workspace/` without a project folder).

---

# 7. Running Commands

All commands (dev server, tests, builds, installs) must be executed from within the target project directory:

```bash
cd /workspace/<project> && npm start
cd /workspace/<project> && npm test
cd /workspace/<project> && npm run build
```

Never run `npm install` or `npm start` from `/workspace/` itself unless it is a monorepo root with a configured workspace.

---

# 8. Relationship to Other Skills

This skill provides the **foundational context** that other skills depend on:

| Skill                      | Depends on Workspace Orientation for          |
|----------------------------|-----------------------------------------------|
| `react-file-operations`    | Knowing `/workspace` is the boundary          |
| `repository-navigation`    | Knowing which project root to navigate        |
| `react-patterns`           | Knowing the project framework and structure   |
| `implementation`           | Knowing where to write code                   |
| `debugging`                | Knowing where to look for bugs                |
| `testing`                  | Knowing where tests live and how to run them  |
| `coding-task-planning`     | Knowing the full project context up front     |

**Always activate this skill first** before delegating to more specialized skills.

---

# 9. Quick-Reference Cheat Sheet

| Task                             | Command                                                                                      |
|----------------------------------|----------------------------------------------------------------------------------------------|
| List all projects                | `ls -la /workspace/`                                                                         |
| Inspect a project                | `ls -la /workspace/<project>/`                                                               |
| View source tree                 | `ls -la /workspace/<project>/src/`                                                           |
| Find a file by name              | `find /workspace/<project> -name "<filename>" -not -path "*/node_modules/*"`                 |
| Search code for a keyword        | `grep -rl "<keyword>" /workspace/<project>/src/ --include="*.js" --include="*.jsx"`          |
| Read package.json                | `cat /workspace/<project>/package.json`                                                      |
| Install dependencies             | `cd /workspace/<project> && npm install`                                                     |
| Start dev server                 | `cd /workspace/<project> && npm start`                                                       |
| Run tests                        | `cd /workspace/<project> && npm test`                                                        |
| Build for production             | `cd /workspace/<project> && npm run build`                                                   |
| Create new React app             | `cd /workspace && npx create-react-app <name>`                                               |
| Create new Vite React app        | `cd /workspace && npm create vite@latest <name> -- --template react`                         |
