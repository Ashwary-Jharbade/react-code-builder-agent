---
name: debugging
description: Diagnoses and resolves React-specific runtime errors, build failures, console warnings, logic bugs, and visual hydration mismatches through systematic analysis.
---

# Debugging Skill

## 1. Purpose
The goal of this skill is to diagnose and fix React errors systematically, relying on logical deduction, stack trace analysis, and deep understanding of React's lifecycle and rendering mechanics, rather than trial-and-error (shotgun debugging).

## 2. Trigger Conditions
Invoke this skill when:
- The build command fails (e.g., `npm run build`, `tsc`, `next build`).
- The application crashes at runtime (white screen, Error Boundary triggered).
- The user reports a bug, unexpected behavior, or console error (e.g., "infinite loop", "state not updating").
- The verification or testing phase fails.
- High severity console warnings appear (e.g., hydration mismatches, missing keys).

## 3. Error Classification
Before diving into code, classify the error into one of the following categories to narrow down the investigation:
- **Build Errors:** TypeScript errors, Webpack/Vite compilation failures, missing modules/dependencies, syntax errors.
- **Runtime Exceptions:** "Cannot read property of undefined", "Not a function", React Error Boundary catch.
- **Logic Bugs:** State updating incorrectly, UI not reflecting state, incorrect data fetching results.
- **Performance/Lifecycle Issues:** Infinite re-render loops, memory leaks, stale closures.
- **Hydration/SSR Issues:** Text content mismatch between server and client in Next.js or Remix.

## 4. Diagnostic Protocol (Systematic Approach)
Follow this step-by-step process for every debugging task:
1. **Reproduce & Understand:** Read the error message or bug description carefully. What is the expected behavior vs. actual behavior?
2. **Isolate:** Use stack traces to pinpoint the exact file, component, and line number causing the issue.
3. **Diagnose:** Form a hypothesis based on React mechanics (e.g., "The useEffect dependency array is missing a value, causing a stale closure").
4. **Fix:** Implement a targeted, minimal fix that addresses the root cause.
5. **Verify:** Ensure the fix resolves the error without introducing regressions (e.g., check that fixing a dependency array doesn't trigger an infinite loop).

## 5. Stack Trace Parsing
- **Identify the Origin:** Look for the top-most line in the stack trace that references application code (e.g., `src/components/MyComponent.tsx`), ignoring internal React/framework code unless it's a specific framework bug.
- **React Error Boundaries:** If an error boundary caught the error, look at the `componentStack` to see the exact component tree hierarchy that led to the crash.
- **Minified Traces:** If dealing with a production trace, look for source map context or identify the failing component by recognizing the logic described by the user.

## 6. Common React Errors & Solutions

### Missing `key` Prop
- **Diagnosis:** Console warning: "Each child in a list should have a unique 'key' prop."
- **Fix:** Add a unique, stable string/number `key` to the outermost element returned by the `.map()` callback. Avoid using array index as keys if the list can be reordered or filtered.

### Rules of Hooks Violations
- **Diagnosis:** "Rendered fewer hooks than expected" or "Hooks can only be called inside the body of a function component".
- **Fix:** Ensure hooks (`useState`, `useEffect`, custom hooks) are called at the top level. Move hooks above any `if` statements, early `return`s, or loops.

### Infinite Re-render Loops
- **Diagnosis:** "Maximum update depth exceeded."
- **Fix:** 
  - Check for state updates directly inside the component body (should be in an event handler or `useEffect`).
  - Audit `useEffect` dependency arrays. Ensure you aren't causing a state update that immediately triggers the effect again.
  - Check for object/array/function recreation on every render triggering child re-renders or effects (use `useMemo`/`useCallback`).

### `useEffect` Dependency Issues (Stale Closures)
- **Diagnosis:** State or props inside a `useEffect` or `useCallback` do not reflect the latest values. ESLint `react-hooks/exhaustive-deps` warnings.
- **Fix:** Add the missing variables to the dependency array. If this causes loops, rethink the effect logic (e.g., use updater functions `setState(prev => prev + 1)` or move logic out of the effect).

### State Updates on Unmounted Components
- **Diagnosis:** "Can't perform a React state update on an unmounted component" (Warning in older React versions, memory leak indicator).
- **Fix:** Use an `abortController` for network requests or a cleanup function in `useEffect` to cancel pending async operations when the component unmounts.

### Hydration Mismatches (SSR / Next.js)
- **Diagnosis:** "Text content did not match. Server: 'A' Client: 'B'" or "Hydration failed because the initial UI does not match what was rendered on the server."
- **Fix:** 
  - Ensure HTML rules aren't broken (e.g., `<p>` cannot contain `<div>`).
  - If rendering browser-only APIs (like `window.localStorage`), delay rendering that specific UI until after the initial mount using a `mounted` state (`useEffect(() => setMounted(true), [])`).

### Module Not Found / Import Errors
- **Diagnosis:** "Cannot resolve module..." or "Export not found".
- **Fix:** Check file paths (case-sensitivity matters!), verify `package.json` dependencies, ensure named vs. default exports match the import statement.

### Type Errors (TypeScript)
- **Diagnosis:** `tsc` fails with "Type X is not assignable to type Y".
- **Fix:** Correct the interface/type definitions. Do NOT blindly use `any` or `@ts-ignore` unless absolutely necessary as a temporary bridge.

## 7. Build Failure Diagnosis
- **Next.js / Vite / Webpack:** Read the terminal output. It usually points directly to the syntax error or missing module.
- **TypeScript (`tsc`):** Run `npx tsc --noEmit` to get a list of all type errors. Fix them systematically from the ground up (shared types first, then components).
- **Dependencies:** If dealing with "missing peer dependency" or version conflicts, inspect `package.json` and suggest `npm install` or version resolutions.

## 8. Runtime Error Diagnosis
- Use the console logs provided by the user.
- If an object might be undefined, check the line throwing the error and ensure proper null-checking (`?.` optional chaining or conditional rendering).
- Verify that props passed to components match the expected types and shapes.

## 9. Logic Bug Diagnosis
When the app doesn't crash but behaves incorrectly:
- Mentally trace the state flow: Where is the state initialized? Where is it updated? Where is it consumed?
- Identify missing updates (e.g., mutating state directly instead of using the setter: `state.push(1)` vs `setState([...state, 1])`).
- Check for race conditions in async data fetching.

## 10. Debugging Commands
When diagnosing, you may propose running specific commands to gather more information (using the `run_command` tool):
- `npm run dev` / `npm run build` to see exact output.
- `npx tsc --noEmit` for type checking.
- `npm run lint` for catching hook rule violations.

## 11. Fix Validation
After implementing a fix, you must verify it:
- Mentally dry-run the changed code.
- Ensure the fix doesn't introduce side effects (e.g., fixing an infinite loop by removing a dependency might introduce a stale closure).
- If tests exist, recommend running them (`npm test`).

## 12. Root Cause Communication
Always explain the *Why*, not just the *What*.
- **Bad:** "I changed `useEffect([],)` to `useEffect([id])`."
- **Good:** "The component was capturing a stale value of `id` because it wasn't in the dependency array. By adding it, the effect re-runs when `id` changes, fetching the correct data."

## 13. Anti-patterns (What NOT to do)
- **Shotgun Debugging:** Guessing at fixes, blindly changing variable names, or randomly moving code around without understanding the problem.
- **`useEffect` Abuse:** Do not use `useEffect` just to sync state or fix lifecycle issues when deriving state during render would work.
- **Overusing `try-catch`:** Do not wrap everything in `try-catch` to suppress errors. Fix the underlying null-reference or logic bug.
- **`@ts-ignore` / `any`:** Avoid bypassing the type system to fix build errors. Fix the actual types.
- **Suppressing Warnings:** Do not ignore React console warnings (like missing keys or exhaust-deps); they often precede actual bugs.

## 14. Escalation
If you cannot reproduce the error mentally or through analysis, or if the stack trace is ambiguous, ask the user for:
- The specific steps to reproduce the bug.
- The exact error text from the browser console or terminal.
- Relevant component code if it wasn't provided or found in the codebase.
