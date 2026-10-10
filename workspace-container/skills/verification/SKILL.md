---
name: verification
description: The final quality assurance gate. Ensures the implemented code satisfies the original prompt, compiles successfully, and integrates without breaking existing routes.
---

**Trigger Conditions:**
- Reaching the end of the `coding-task-planning` checklist.

**Execution Protocol:**
1. **Requirements Cross-Check:** Load the output of `requirement-analysis` and verify every mapped requirement exists in the new code.
2. **Compilation Simulation:** Execute (or simulate executing) `npm run typecheck` (`tsc --noEmit`) and `npm run lint`.
3. **Integration Verification:** Check that the newly created component is actually exported properly and imported securely into a parent page or router.
4. **Cleanup:** Remove any temporary `console.log` statements or commented-out code blocks generated during implementation.

**Rules & Constraints:**
- If verification fails, the agent must automatically fallback to the `debugging` skill.
- The task is not marked "Complete" until verification passes with 0 critical errors.

**Output:** 
A terminal confirmation stating compilation success, requirement fulfillment, and a summary of the files changed.