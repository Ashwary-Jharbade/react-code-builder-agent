---
name: implementation
description: Writes high-quality, production-ready React code strictly adhering to modern standards, the project context, and the task plan.
---

# Implementation Skill

## 1. Purpose
The primary purpose of the `implementation` skill is to write production-ready, highly maintainable, and typed React code. This skill takes the atomic steps defined during the `coding-task-planning` phase and translates them into concrete code within the `/workspace`, ensuring alignment with the project's existing architecture and best practices.

## 2. Trigger Conditions
This skill is triggered when:
- Active execution of the `coding-task-planning` checklist is underway.
- The agent needs to create new files or modify existing files to fulfill a functional requirement.
- Handoff from `repository-navigation` or `codebase-search` to begin writing code.

## 3. Pre-Implementation Checklist
Before writing or modifying any code, ALWAYS verify the following:
- [ ] **Project Context:** Ensure `project-context` has been read (tech stack, styling approach, state management).
- [ ] **Plan Clarity:** The current step from the `coding-task-planning` checklist is unambiguous and clearly scoped.
- [ ] **Target Identification:** The exact file path (relative to `/workspace/<project>/`) is known.
- [ ] **Existing Code Context:** For file modifications, the latest version of the file has been reviewed to prevent regressions.

## 4. Modern React Standards
- **Strictly Functional:** Use functional components exclusively. Do not use or write Class components.
- **Hooks:** Leverage React Hooks for state and lifecycle management.
- **TypeScript First:** All code must be strongly typed unless the project is strictly JavaScript. Avoid `any`.
- **Destructuring:** Use object destructuring for props and state for cleaner syntax.

## 5. Component Structure Template
Maintain a consistent internal structure for every React component file:
1.  **Imports:** Group imports logically (React, external libraries, internal components, hooks, utils, types, styles).
2.  **Types/Interfaces:** Define props and local types immediately after imports.
3.  **Component Definition:** Standard arrow function or standard function definition.
4.  **Hooks / State:** Group `useState`, `useRef`, `useContext`, etc., at the top of the component.
5.  **Derived State / Memos:** Place `useMemo` and derived variables next.
6.  **Callbacks:** Define `useCallback` and standard helper functions.
7.  **Effects:** Place `useEffect` blocks just before the return statement.
8.  **Return Statement:** Render JSX clearly, minimizing complex inline logic.
9.  **Exports:** Default or named exports at the bottom of the file (or inline if preferred by project style).

## 6. Hook Rules
- **Top Level Only:** Never call hooks inside loops, conditions, or nested functions.
- **Dependency Arrays:** Always provide accurate dependency arrays for `useEffect`, `useCallback`, and `useMemo`. Exhaustive deps rule must be respected.
- **Custom Hooks:** Abstract complex, reusable state logic into custom hooks (`use<Name>`).

## 7. State Management Patterns
- **Local State:** Use `useState` for simple component-level state (UI toggles, form inputs).
- **Lifted State:** Lift state up to the nearest common ancestor when multiple components need to share it.
- **Context API:** Use React Context for global UI state (themes, authentication status) but avoid it for high-frequency updates.
- **External Stores:** Respect the project's chosen state management library (Zustand, Redux, Jotai) for complex, shared application state.

## 8. Side Effects
- **useEffect Cleanups:** Always return a cleanup function from `useEffect` when dealing with subscriptions, timers, or event listeners.
- **Avoid Infinite Loops:** Ensure dependency arrays are stable (use `useCallback` or `useMemo` for objects/functions passed as dependencies).
- **Data Fetching in Effects:** If fetching data in `useEffect`, handle race conditions (e.g., using an `ignore` flag).

## 9. Performance
- **useMemo:** Use to memoize computationally expensive calculations. Do not use for simple operations (e.g., array mapping of 5 items) as the overhead is worse.
- **useCallback:** Use to maintain referential equality of functions passed as props to highly optimized child components (e.g., wrapped in `React.memo`).
- **React.memo:** Use only for pure components that render often with the exact same props.

## 10. Accessibility (a11y)
- **Semantic HTML:** Use native elements (`<nav>`, `<header>`, `<main>`, `<article>`, `<button>`, `<a>`) instead of generic `<div>`s.
- **ARIA:** Apply appropriate `aria-` labels, roles, and states for complex widgets (tabs, modals).
- **Keyboard Navigation:** Ensure interactive elements are focusable (`tabIndex={0}`) and triggerable via `Enter` or `Space`.
- **Focus Management:** Manage focus explicitly when rendering modals or dynamic overlays.

## 11. Styling
- **Respect Context:** Strictly adhere to the styling methodology identified in `project-context` (e.g., Tailwind CSS, CSS Modules, styled-components).
- **Avoid Inline Styles:** Do not use `style={{...}}` unless for truly dynamic, javascript-calculated values (like mouse position).
- **Responsive Design:** Implement mobile-first responsive patterns using standard breakpoints.

## 12. Error Handling
- **Error Boundaries:** Utilize Error Boundaries for catching rendering errors in distinct subtrees.
- **Async Operations:** Always wrap `async`/`await` calls in `try/catch` blocks and handle error states gracefully in the UI.
- **Graceful Degradation:** Provide meaningful fallback UI for failed data loads or empty states.

## 13. Next.js Specific (If Applicable)
- **'use client':** Automatically prepend `"use client";` to the top of files that require browser APIs, state (`useState`), effects (`useEffect`), or interactive event listeners (`onClick`).
- **Server Components:** Default to Server Components. Do not use `'use client'` unnecessarily.
- **Data Fetching:** Prefer Next.js App Router data fetching patterns (`fetch` in Server Components) over client-side fetching where possible.

## 14. File Output Rules
- **Complete Output:** When generating a file, output the FULL, complete file content. 
- **No Placeholders:** NEVER use placeholders like `// ...existing code...` or `/* rest of the component */` unless explicitly instructed to use a patch/diff tool. The output must be immediately executable.
- **Valid Imports:** Ensure all relative and absolute imports resolve correctly within the `/workspace`.

## 15. Code Quality
- **Naming Conventions:** 
  - Components/Files: PascalCase (`UserProfile.tsx`).
  - Variables/Functions: camelCase (`handleUpdate`, `userData`).
  - Constants: UPPER_SNAKE_CASE (`MAX_RETRY_COUNT`).
- **Consistency:** Follow the established patterns found in adjacent project files.
- **Clean Up:** Remove all `console.log` statements and commented-out dead code before final output.

## 16. Anti-patterns to Avoid
- **Mutating State:** NEVER mutate state directly (e.g., `state.value = 1;`). ALWAYS use the provided setter function.
- **Conditional Hooks:** Never place hooks inside `if` statements or loops.
- **Inline Component Definitions:** Never define a component inside another component's render function (it destroys the component state on every parent render).
- **Over-abstraction:** Do not create abstractions, contexts, or custom hooks prematurely. Keep code simple until complexity necessitates abstraction.
- **Index as Key:** Avoid using the array `index` as a `key` prop in `.map()` unless the list is purely static and never changes order or size.

## 17. Post-Implementation
- **Update Plan:** Mark the current step as complete in the `coding-task-planning` checklist.
- **Handoff:** If the task is fully implemented, transition to the `testing`, `verification` or `code-review` skill.
- **Feedback Loop:** If errors occur or assumptions are broken during implementation, immediately hand off to `debugging`.
