---
name: implementation
description: Writes high-quality, production-ready React code strictly adhering to modern standards, the project context, and the task plan.
---

**Trigger Conditions:**
- Active execution of the `coding-task-planning` checklist.

**Execution Protocol:**
1. **Modern React Standards:** Write purely functional components. Use hooks.
2. **Next.js Awareness (If applicable):** Automatically determine if a file requires the `"use client"` directive based on the presence of hooks (`useState`, `useEffect`) or event listeners (`onClick`).
3. **Performance Optimization:** Wrap expensive calculations in `useMemo`. Wrap functions passed as props in `useCallback` to prevent child re-renders.
4. **Accessibility (a11y):** Apply correct semantic HTML (`<nav>`, `<main>`, `<button>` instead of `<div onClick>`) and `aria-` labels for dynamic content.

**Rules & Constraints:**
- Output FULL, complete files. Do not use placeholders like `// ...existing code...` unless utilizing a specific patch/diff tool.
- Never mutate state directly (e.g., `state.value = 1`). Always use setters.

**Output:** 
Syntactically correct, type-safe React code committed to the file system.
