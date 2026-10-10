---
name: codebase-search
description: Executes semantic, Regex, and AST-aware searches to locate usages, definitions, and dependencies, preventing breaking changes caused by isolated modifications.
---

**Trigger Conditions:**
- Before modifying a shared UI component or utility function.
- When trying to find where a specific state or context is initialized.

**Execution Protocol:**
1. **Definition Search:** Use precise queries (e.g., `export const Button`, `interface User`) to find source files.
2. **Usage Tracing:** If modifying Component A, execute a search for `<Component A` or `import Component A` to find all parents.
3. **Pattern Matching:** To find specific React behaviors, search for hook invocations (e.g., `useQuery(`, `createContext(`).

**Rules & Constraints:**
- If a component has more than 5 consumers, generate an impact report before modifying its prop signature.
- Prefer exact match or Regex over fuzzy search for accurate refactoring.

**Output:** 
A dependency graph array showing `[File A -> imports -> File B]`, and exact line numbers of target code.
