---
name: repository-navigation
description: Intelligently traverses the file system using architectural heuristics rather than exhaustive directory scanning, minimizing token usage and context pollution.
---

# Repository Navigation Skill

## 1. Purpose
The purpose of this skill is to navigate the project workspace efficiently and intelligently. Instead of brute-force directory scanning, the agent applies architectural heuristics to locate components, features, configurations, and utilities. This minimizes unnecessary file system operations, prevents context pollution with irrelevant files, and speeds up the resolution of user requests. Always assume actions take place within `/workspace` or a specific project directory like `/workspace/<project>`.

## 2. Trigger Conditions
- The user requests a modification to a specific feature, page, or component.
- The agent needs to locate the entry point of the application to trace logic.
- The agent is handed a bug report and needs to find the relevant source file.
- The agent needs to understand the routing or state management configuration of the app.
- A previous skill (like `codebase-search`) returned no results, requiring manual traversal based on naming conventions.

## 3. Architecture Pattern Detection
Before blindly navigating, establish the architectural pattern of the React project by inspecting the top-level directories within `src/` or `app/`.

- **Atomic Design:** Look for `atoms/`, `molecules/`, `organisms/`, `templates/`, and `pages/`.
- **Feature-based (Feature Sliced):** Look for `features/`, `modules/`, or domains inside `src/`. Inside each feature, you might find its own `components/`, `hooks/`, `api/`, and `utils/`.
- **Domain-driven:** Look for domain names (e.g., `user/`, `auth/`, `product/`) directly under `src/` or `app/`.
- **Flat Layout:** Everything is mostly directly under `src/components/` and `src/pages/`.
- **Next.js App Router:** Look for `app/` containing `page.tsx`, `layout.tsx`, `route.ts`.
- **Next.js Pages Router:** Look for `pages/` containing `index.tsx`, `_app.tsx`, `_document.tsx`.

## 4. Common React Project Layouts
Familiarize yourself with standard project layouts to anticipate file locations:

### Create React App (CRA) / Vite Default
```text
/src
  /assets
  /components
  /hooks
  /pages or /views
  /services or /api
  /utils
  App.jsx / App.tsx
  main.jsx / main.tsx / index.js
```

### Next.js (App Router)
```text
/src (optional)
  /app
    layout.tsx
    page.tsx
    /api
      route.ts
    /[dynamic_route]
      page.tsx
  /components
  /lib
```

## 5. Entry Point Discovery
When you need to understand the application shell, global providers, or layout, locate the entry point first:
- **Vite/CRA:** Check `src/main.tsx`, `src/main.jsx`, `src/index.js`, or `src/index.tsx`. Then follow imports to `src/App.tsx`.
- **Next.js App Router:** Check `app/layout.tsx` (or `src/app/layout.tsx`) for the root layout and `app/page.tsx` for the home page.
- **Next.js Pages Router:** Check `pages/_app.tsx` for global setup and `pages/index.tsx` for the home page.
- **React Native / Expo:** Check `App.tsx` or `index.js` in the root, or `app/_layout.tsx` if using Expo Router.

## 6. Heuristic Navigation Rules
Use these rules to infer where files should live without scanning everything:
- **Components:** Look in `src/components/`, `src/ui/`, or `src/features/<name>/components/`.
- **Custom Hooks:** Look in `src/hooks/` or `src/features/<name>/hooks/`. Filenames usually start with `use` (e.g., `useAuth.ts`).
- **Utilities/Helpers:** Look in `src/utils/`, `src/lib/`, or `src/helpers/`.
- **State/Store:** Look in `src/store/`, `src/state/`, or `src/context/`.
- **Styles:** Look alongside the component (e.g., `Button.module.css`), in `src/styles/`, or check if Tailwind is configured (`tailwind.config.js`).
- **Tests:** Look for `__tests__/` directories, or files ending in `.test.ts`, `.spec.tsx` adjacent to the source files.

## 7. Targeted Drill-down Examples
If modifying a specific type of UI element, use targeted drill-downs:
- **Header/Footer:** Check `src/components/layout/`, `src/components/common/`, or `src/components/Global/`.
- **Buttons/Inputs:** Check `src/components/ui/`, `src/components/core/`, or `src/components/atoms/`.
- **Login/Registration:** Check `src/features/auth/`, `src/pages/auth/`, or `src/app/(auth)/`.
- **API calls:** Check `src/api/`, `src/services/`, or `src/features/<name>/api/`.

## 8. Path Resolution
When analyzing imports or planning to create new files, resolve paths accurately:
- **Relative Imports:** Calculate exact relative paths (e.g., `../../utils/helpers.ts`) based on the current file's location.
- **Absolute / Alias Imports:** Check `tsconfig.json` or `jsconfig.json` for `paths` or `baseUrl` configurations (e.g., `@/components/Button` mapping to `src/components/Button`). Check `vite.config.ts` or `webpack.config.js` for alias resolution.

## 9. File Existence Validation
- **Rule:** NEVER attempt to read or modify a file without first confirming it exists.
- **Action:** If an import path points to `components/Header`, check if it's `components/Header.tsx`, `components/Header.jsx`, `components/Header/index.tsx`, or `components/Header/Header.tsx`.

## 10. Directory Reading Rules
When you must list directory contents to find what you need:
- **Limit Depth:** Only list one directory at a time. Do not use recursive listing unless strictly constrained to a very small, known subfolder.
- **Skip Ignored Folders:** Never list `node_modules`, `.git`, `.next`, `dist`, `build`, or `coverage`.
- **Filter Early:** If looking for a component, list only the `components/` directory first before expanding your search.

## 11. Mental Map Building
As you navigate, construct a localized mental map of the feature area you are working on.
- Note the relationship between the Page, its constituent Components, its Hooks, and its API definitions.
- Keep track of where global state or context is injected.
- If you modify a shared component, use `codebase-search` to find other usages before assuming the change is safe.

## 12. Anti-patterns
Avoid the following behaviors at all costs:
- **Brute-force Scanning:** Running `ls -R` or `find .` across the entire project. This wastes tokens and pollutes context.
- **Reading Blacklisted Directories:** Scanning `node_modules` or `.git`.
- **Guessing Paths:** Attempting to `view_file` on a guessed path without checking if it exists, leading to repetitive "file not found" errors.
- **Reading Everything:** Opening files that are not directly relevant to the current feature or bug just to "understand the app". Rely on `project-context` and targeted reading instead.
- **Ignoring Aliases:** Failing to check `tsconfig.json` and misinterpreting alias imports as missing modules.