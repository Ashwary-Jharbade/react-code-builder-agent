---
name: coding-task-planning
description: Converts the Technical Specification into a Directed Acyclic Graph (DAG) of actionable, sequential coding steps.
---

**Trigger Conditions:**
- Successful completion of `requirement-analysis`.

**Execution Protocol:**
1. **Type Definition (Step 1):** Plan the creation of TypeScript interfaces/types first.
2. **Skeleton UI (Step 2):** Plan the creation of dumb/presentational components with hardcoded data.
3. **State Management (Step 3):** Plan the implementation of hooks and local state wiring.
4. **Integration (Step 4):** Plan the connection to external APIs or global stores.
5. **Review (Step 5):** Plan a self-review step to check for prop drilling or re-render issues.

**Rules & Constraints:**
- Steps must be small enough that a single file modification can fulfill one step.
- Never plan to build a consuming component before its children are planned.

**Output:** 
An ordered Execution Checklist. The agent must update this checklist state as steps are completed.
