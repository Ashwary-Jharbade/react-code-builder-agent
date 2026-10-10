---
name: verification
description: The final quality assurance gate. Ensures the implemented code satisfies the original prompt, compiles successfully, and integrates without breaking existing routes.
---

## 1. Purpose
The Verification skill serves as the final quality assurance gate before a task can be declared complete. Its primary objective is to systematically prove that the code changes meet the requested requirements, integrate correctly with the existing codebase, do not introduce new regressions, and adhere to structural and style guidelines. 

## 2. Trigger Conditions
- Reaching the end of the `coding-task-planning` checklist.
- The user explicitly asks to verify, review, or check the work.
- Before presenting the final implementation as "done" or "ready" to the user.
- After completing a complex refactoring or codebase restructuring.

## 3. Requirements Cross-Check
The agent must load the original specification from the `requirement-analysis` output and systematically verify that each requirement is satisfied.
- **Checklist validation:** For each requirement in the spec, locate the corresponding code that implements it.
- **Edge cases:** Confirm that explicitly mentioned edge cases in the spec are handled in the code.
- **Missing functionality:** Identify any user requests that were overlooked during implementation.

## 4. Compilation Check
The code must compile successfully without type errors.
- **Command:** Run `npm run typecheck` or `npx tsc --noEmit` in the `/workspace/<project>` directory.
- **Evaluation:** 
  - If the command exits with code `0`, the compilation check passes.
  - If the command fails, examine the TypeScript errors. Pay close attention to interface mismatches, missing props, and "any" type fallbacks.
- **Action:** Fix any type errors directly or transition to the `debugging` skill if the issue is complex.

## 5. Lint Check
Code must adhere to the project's stylistic and structural guidelines.
- **Command:** Run `npm run lint` or `npx eslint .` in the `/workspace/<project>` directory.
- **Evaluation:**
  - Errors must be fixed before completion.
  - Warnings should be evaluated. If they indicate a potential bug (e.g., `react-hooks/exhaustive-deps`), they must be fixed. Stylistic warnings should be addressed if trivial, but are not strict blockers if they existed prior to the agent's work.
- **Action:** Run `npm run lint -- --fix` to automatically resolve fixable issues, then address remaining errors manually.

## 6. Import/Export Verification
Verify that the newly created or modified modules are correctly connected to the rest of the application.
- **Exports:** Ensure that new components, hooks, or utilities are properly exported (default or named).
- **Imports:** Verify that the new code is imported securely into parent pages or routers. 
- **Relative paths:** Check that relative import paths (e.g., `../../components/Button`) are correct and resolve successfully.
- **Circular dependencies:** Ensure that the new imports do not create circular dependency loops.

## 7. Route Integration
For new pages or major views, verify that they are accessible.
- **Next.js App Router:** Ensure the file is named `page.tsx` and placed in the correct directory (e.g., `app/dashboard/page.tsx`).
- **React Router (Vite/CRA):** Ensure the component is imported and added to the route definitions (e.g., `<Route path="/dashboard" element={<Dashboard />} />`).
- **Links:** Verify that existing navigation elements or links meant to point to the new route are correct.

## 8. Runtime Verification
Whenever possible, verify that the application runs without immediate crashing.
- **Start dev server:** Run `npm run dev` in the background (using a background task tool).
- **Console check:** Look for immediate runtime errors, hydration warnings, or unhandled exceptions in the server or client console output.
- **Network requests:** If the new feature fetches data, confirm that the API endpoints it calls actually exist or are mocked properly.

## 9. Code Cleanup
Ensure the codebase is left clean and professional.
- **Console logs:** Remove any temporary `console.log`, `console.debug`, or `console.warn` statements added during development.
- **Comments:** Remove commented-out blocks of old code, unnecessary `// TODO` or `// FIXME` comments that were resolved, and debug notes.
- **Unused imports:** Remove any imports that are no longer used in the files modified.

## 10. File Inventory
Compile a comprehensive list of all files created, modified, or deleted during the task.
- Group the files logically (e.g., Components, API Routes, Utilities).
- Ensure no accidental changes were made to unrelated files.
- Revert any files that were modified temporarily for testing purposes but are not part of the required changes.

## 11. Failure Protocol
If any of the verification steps fail and cannot be resolved with a quick, trivial fix:
- The agent must automatically fallback to the `debugging` skill.
- Document the exact error message, the step that failed, and the files involved.
- Pass this context to the debugging process to ensure an efficient resolution.

## 12. Completion Criteria
The task is only marked "Complete" when:
- 0 critical TypeScript errors (`tsc` passes).
- 0 critical ESLint errors.
- 100% of requirements from the `requirement-analysis` spec are mapped to implemented code.
- All modified files have been cleaned of debug artifacts.
- The build process (if applicable) succeeds.

## 13. Output Format
Generate a brief Verification Report to conclude the task, formatted as follows:

```markdown
### Verification Report
- **Requirements Check:** ✅ All requirements met.
- **Type Check (`tsc`):** ✅ Passed
- **Lint Check (`eslint`):** ✅ Passed
- **Runtime/Integration:** ✅ Verified routing and exports.
- **Cleanup:** ✅ Debug logs removed.

**Files Changed:**
- `app/dashboard/page.tsx` (created)
- `components/ui/Button.tsx` (modified)
```

## 14. Anti-patterns
- **Skipping Verification:** Never declare a task complete without running at least type and lint checks.
- **Blind Assumption:** Do not assume that just because the code looks correct, it compiles correctly.
- **Ignoring Warnings:** Do not ignore React hook dependency warnings; they often lead to stale state bugs.
- **Leaving Messes:** Never leave `console.log("here")` or commented-out trial code in the final output.
- **Scope Creep:** Do not verify or refactor unrelated files outside the scope of the user's prompt just because they have pre-existing lint errors.