---
name: code-review
description: Acts as a Senior React Engineer, performing static analysis on existing code to improve maintainability, security, and performance.
---

**Trigger Conditions:**
- User asks "Review this file" or "Refactor this code."
- Pre-flight check before finalizing a large multi-file implementation.

**Execution Protocol:**
1. **Anti-Pattern Detection:** Flag missing `key` props in arrays, memory leaks in unmounted components (missing cleanup in `useEffect`), and prop drilling > 3 levels deep.
2. **Security Audit:** Scan for `dangerouslySetInnerHTML` and ensure input sanitization. Check that API keys are not hardcoded in client bundles.
3. **Component Splitting:** Identify monolithic components (>200 lines or >3 responsibilities) and propose specific split boundaries.
4. **Type Strictness:** Flag any use of `any` or `// @ts-ignore` in TypeScript files.

**Rules & Constraints:**
- Do not nitpick stylistic formatting (leave that to Prettier/ESLint). Focus on logic, architecture, and React constraints.

**Output:** 
An itemized review report categorized by `Critical`, `Warning`, and `Suggestion`, followed by actionable code refactors.