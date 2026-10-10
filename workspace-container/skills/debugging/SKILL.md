---
name: debugging
description: Diagnoses and resolves React-specific runtime errors, build failures, console warnings, and visual hydration mismatches.
---

**Trigger Conditions:**
- Build command fails (`tsc`, `next build`).
- User provides a stack trace, console error, or describes a logical bug (e.g., "infinite loop").

**Execution Protocol:**
1. **Stack Trace Parsing:** Isolate the exact file and line number from standard React error boundaries.
2. **Hook Rule Validation:** Scan the failing component specifically for conditional hooks, hooks inside loops, or hooks returning after early returns.
3. **Dependency Array Auditing:** For infinite loops, audit `useEffect` arrays. Check if object/array references are being recreated on every render and triggering the effect.
4. **Hydration Check:** If SSR/Next.js, check for HTML tags mismatching between server and client (e.g., `<div>` inside `<p>`).

**Rules & Constraints:**
- Do not blindly wrap everything in `useEffect` to solve lifecycle issues. Prefer deriving state during render when possible.
- Explain the root cause briefly to the user before applying the fix.

**Output:** 
A root-cause analysis and the exact code patch that resolves the error.
