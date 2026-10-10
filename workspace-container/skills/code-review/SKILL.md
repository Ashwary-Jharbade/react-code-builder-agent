---
name: code-review
description: Acts as a Senior React Engineer, performing deep static analysis on existing code to improve maintainability, security, performance, and accessibility.
---

# 1. Purpose
This skill executes a rigorous, senior-engineer-level code review focusing on logic, architecture, React ecosystem correctness, and security. It ensures that code within `/workspace/<project>/` adheres to enterprise standards without wasting time on subjective styling or formatting differences.

# 2. Trigger Conditions
Execute this skill when:
- The user explicitly requests a review: "Review this file," "Can you check my code?", or "Refactor this component."
- Performing a pre-flight check before finalizing a large multi-file `implementation`.
- Post-implementation QA gate before handing off to the `testing` or `verification` skills.
- The user asks to audit for performance, security, or accessibility issues.

# 3. Review Scope
**What to Review:**
- Component architecture, state management, and lifecycle logic.
- React-specific design patterns and hook correctness.
- Security vulnerabilities, performance bottlenecks, and a11y compliance.
- Type safety and correct TypeScript usage.

**What NOT to Review:**
- Code formatting, indentation, or quotation mark styles (leave these to Prettier/ESLint).
- Subjective naming conventions, unless they actively obscure the code's purpose.

# 4. Anti-Pattern Checklist
Actively scan for and flag the following React anti-patterns:
- **State Mutation:** Mutating state directly instead of using setter functions (e.g., `state.items.push(newItem)`).
- **Missing Keys:** Missing or non-unique `key` props in mapped arrays (e.g., using array index as keys for dynamic lists).
- **Derived State:** Storing derived data in `useState` instead of calculating it on the fly during render.
- **Stale Closures:** Referencing outdated state/props inside asynchronous callbacks or effects.
- **Unnecessary Effects:** Using `useEffect` to synchronize state when event handlers could do the job.

# 5. Security Audit
Inspect the codebase for common frontend vulnerabilities:
- **XSS (Cross-Site Scripting):** Flag any use of `dangerouslySetInnerHTML`. If it is absolutely necessary, verify that the input is being explicitly sanitized using a library like `DOMPurify`.
- **Hardcoded Secrets:** Ensure no API keys, tokens, or sensitive URLs are hardcoded in client bundles. Require environment variables (e.g., `process.env.NEXT_PUBLIC_API_KEY`).
- **Unsafe Evaluation:** Flag any use of `eval()` or `new Function()`.
- **Unvalidated Input:** Ensure user input used in client-side routing or state is properly validated.

# 6. Performance Review
Identify bottlenecks that cause unnecessary re-renders or inflate bundle size:
- **Unnecessary Re-renders:** Flag inline objects, arrays, or arrow functions passed as props to memoized child components.
- **Missing Memoization:** Suggest `useMemo` for expensive calculations and `useCallback` for functions passed as dependencies or to heavily re-rendered children.
- **Large Bundle Imports:** Flag namespace imports of large libraries (e.g., `import { get } from 'lodash'`). Suggest tree-shakeable imports (e.g., `import get from 'lodash/get'`).

# 7. Accessibility (a11y) Review
Ensure UI components are accessible to all users:
- **Missing Alt Text:** Flag `<img>` tags without meaningful `alt` attributes.
- **Non-Semantic Elements:** Flag `<div>` or `<span>` elements used with `onClick` handlers. Suggest native `<button>` elements instead.
- **Missing ARIA:** Suggest appropriate `aria-*` attributes for custom interactive widgets (e.g., custom dropdowns or modals).
- **Keyboard Navigation:** Ensure interactive elements have proper `tabIndex` and focus states.

# 8. Component Architecture
Evaluate structural integrity and separation of concerns:
- **Single Responsibility Principle (SRP):** Identify monolithic components (>200 lines or handling >3 responsibilities) and propose specific split boundaries (e.g., extracting a complex form into its own file).
- **Prop Drilling:** Flag instances where props are passed down more than 3 levels deep. Suggest using React Context or composition (passing components as `children`).

# 9. Type Safety (TypeScript)
Enforce strict typing rules if working in `.ts` or `.tsx` files:
- **Avoid `any`:** Flag all uses of the `any` type. Suggest proper interfaces or generics.
- **No Ignoring:** Flag `// @ts-ignore` or `// @ts-nocheck`. If type errors exist, resolve the underlying types instead of suppressing them.
- **Strict Typing:** Ensure event handlers (e.g., `React.MouseEvent`) and component return types (`React.FC` or explicit `JSX.Element`) are properly annotated.

# 10. Hook Correctness
Enforce the Rules of Hooks:
- **Dependency Arrays:** Check `useEffect`, `useCallback`, and `useMemo` for missing or extraneous dependencies.
- **Cleanup Functions:** Flag missing cleanup functions in `useEffect` when subscribing to events, intervals, or WebSocket connections to prevent memory leaks.
- **Conditional Hooks:** Ensure hooks are not called inside loops, conditions, or nested functions.

# 11. Severity Classification
Categorize findings using the following scale:
- **[CRITICAL]:** Bugs, security vulnerabilities, memory leaks, or breaking changes. Must be fixed immediately.
- **[WARNING]:** Performance issues, anti-patterns, or a11y violations that degrade user experience but do not break the app.
- **[SUGGESTION]:** Architectural improvements, readability enhancements, or strict typing recommendations.

# 12. Output Format
When generating a review report, use the following structured Markdown format:

```markdown
## Code Review Report: `/workspace/<project>/path/to/file.tsx`

### Summary
[1-2 sentences summarizing the overall quality and main issues found.]

### Findings
- **[CRITICAL]** Line 45: `useEffect` missing cleanup function for `setInterval`.
- **[WARNING]** Line 12: Object literal passed to `data` prop causes child re-renders.
- **[SUGGESTION]** Line 80-150: Consider extracting the `UserForm` into a separate component to adhere to SRP.

### Proposed Refactoring
[Provide a snippet or plan for the fixes. If auto-fixing, state what you will do.]
```

# 13. Auto-Fix vs Report
- **When to Report:** For broad architectural changes (e.g., replacing prop drilling with Redux/Context) or destructive changes, present the report and wait for user approval.
- **When to Auto-Fix:** If instructed to "fix these issues," or if the issues are isolated `[CRITICAL]` or `[WARNING]` bugs in a targeted file, use the `react-file-operations` skill to implement the fixes directly after generating the report.

# 14. AI Anti-Patterns to Avoid
- **Nitpicking Style:** Do not comment on spacing, quotes, or trailing commas.
- **Unnecessary Rewrites:** Do not rewrite completely working, performant code just to use a "newer" syntax if the current syntax is standard and correct.
- **Hallucinated Files:** Always verify the file exists at `/workspace/<project>/...` using codebase search before reviewing it.