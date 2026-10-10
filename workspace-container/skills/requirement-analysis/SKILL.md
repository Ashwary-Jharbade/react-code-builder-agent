---
name: requirement-analysis
description: Translates ambiguous, natural-language user prompts into a rigorous React Technical Specification (Tech Spec/PRD).
---

**Trigger Conditions:**
- Receipt of a new user feature request or complex bug report.

**Execution Protocol:**
1. **Component Hierarchy Extraction:** Break the requested UI down into a visual tree (`Parent -> ChildA, ChildB`).
2. **State & Prop Mapping:** Define exactly what state is needed, where it lives (lifting state up), and what props pass downward.
3. **Side-Effect Identification:** List all required API calls, subscriptions, and DOM mutations. Map these to `useEffect` or data-fetching hooks.
4. **Edge Case Definition:** Explicitly define loading states, error states, and empty states.

**Rules & Constraints:**
- Do not assume UI details; if the user says "add a user list", define the pagination and loading skeleton requirements automatically.
- Differentiate clearly between client-side state (UI toggles) and server state (API data).

**Output:** 
A structured Technical Specification document (JSON or Markdown) defining interfaces, components, and state trees.
