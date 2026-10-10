---
name: requirement-analysis
description: Translates ambiguous, natural-language user prompts into a rigorous React Technical Specification (Tech Spec/PRD) before any code is written.
---

## 1. Purpose
The `requirement-analysis` skill acts as the translation layer between vague, natural-language user requests and structured, actionable engineering specifications. Before any code is written, this skill ensures that all architectural decisions (components, state, side-effects) and edge cases are clearly defined, scoped, and agreed upon.

## 2. Trigger Conditions
Invoke this skill immediately when:
- Receiving a new feature request or "build me X" prompt.
- Tasked with a complex bug report requiring architectural changes.
- Receiving a refactoring request that alters component structure or state management.
- The user provides UI mockups or design descriptions without implementation details.

## 3. Disambiguation Protocol
Vague requests lead to incorrect implementations. If a user request lacks necessary detail, pause and ask clarifying questions.

**When to Disambiguate:**
- Missing data models (e.g., "Add a user list" -> *What fields are displayed? Are there roles?*)
- Missing pagination/scaling (e.g., "Show all transactions" -> *Do we need pagination or infinite scroll?*)
- Missing permissions (e.g., "Add a delete button" -> *Can anyone delete, or only admins?*)

**Action:** Present a short, numbered list of questions to the user. Do not proceed to full spec creation until critical ambiguities are resolved.

## 4. Component Hierarchy Extraction
Break the requested UI down into a visual and logical component tree.

**Execution:**
- Identify the root or container component.
- Break down the UI into modular, reusable child components.
- Outline the hierarchy (`Parent -> ChildA, ChildB`).

**Example:**
For a "User Directory" request:
```text
UserDirectoryPage (Container)
  ├── SearchBar (Input & Filters)
  ├── UserList (List Wrapper)
  │     ├── UserCard (Individual User Display)
  │     └── UserCard
  └── PaginationControls (Page Navigation)
```

## 5. State & Prop Mapping
Define exactly what state is needed, where it lives, and how data flows.

**Execution:**
- **Local State:** State only relevant to one component (e.g., `isDropdownOpen` in `SearchBar`).
- **Lifted State:** State shared between siblings (e.g., `searchQuery` lifted to `UserDirectoryPage`).
- **Global State:** App-wide state (e.g., `currentUserSession`). Use Context or global store.
- **Server State:** Data fetched from an API (e.g., `usersList`). Map to data-fetching hooks (e.g., SWR, React Query, or `useEffect`).
- **Props:** Define the interfaces for props passed downward to child components.

## 6. Side-Effect Identification
List all required side-effects and tie them to component lifecycles or user interactions.

**Execution:**
- **API Calls:** Define required endpoints, request payloads, and expected response formats.
- **Subscriptions:** WebSockets or real-time listeners (ensure cleanup is noted).
- **Event Listeners:** Global window/document listeners (e.g., `keydown` for modal escape).
- **Timers:** `setTimeout` or `setInterval` needs (ensure cleanup is noted).

## 7. Edge Case Matrix
Explicitly define how the application behaves outside the "happy path".

**Execution:**
For every major component or data-fetching operation, define:
- **Loading State:** Skeletons, spinners, or disabled buttons.
- **Error State:** Network failures, invalid inputs, API 500s. Provide retry mechanisms.
- **Empty State:** What shows when an array is empty or a search yields no results.
- **Permission Denied:** What happens if the user lacks authorization.
- **Offline Mode:** Behavior when the network drops.
- **Large Data Sets:** Pagination, virtualization, or truncating text.

## 8. Acceptance Criteria
Define what "done" looks like for each requirement to guide testing and verification.

**Execution:**
- Write criteria as verifiable statements.
- Example: *The search bar must debounce input by 300ms before making an API call.*
- Example: *If the API returns a 404, the `EmptyState` component must render with the text "No users found."*

## 9. Output Format: Structured Tech Spec
The final output must be a Markdown or JSON specification. If written as Markdown, use the following structure:

```markdown
# Technical Specification: [Feature Name]

## 1. Overview
[Brief summary of what is being built]

## 2. Component Architecture
[Component tree diagram]

## 3. Data & State Management
- **Interfaces/Types:** [TypeScript interfaces]
- **State Location:** [Where state lives]
- **Props:** [Key prop definitions]

## 4. Side Effects & APIs
- [List of API calls, endpoints, and triggers]

## 5. Edge Cases & Error Handling
[Edge Case Matrix: Loading, Empty, Error, etc.]

## 6. Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

## 10. Scope Control
Prevent feature creep by clearly defining what is *out of scope*.

**Execution:**
- If a request naturally implies a massive feature (e.g., "Add comments" implying threaded replies, rich text, and @mentions), define a Minimum Viable Product (MVP) scope.
- Explicitly list deferred features in an "Out of Scope (V2)" section.

## 11. Anti-Patterns
Avoid these common mistakes during requirement analysis:
- **Over-engineering:** Proposing Redux/Zustand when local state or simple Context suffices.
- **Under-specifying:** Failing to define the exact shape of API responses or prop interfaces.
- **Assuming UI details:** Inventing complex UI paradigms not requested by the user without asking first.
- **Ignoring cleanup:** Forgetting to specify cleanup functions for `useEffect` subscriptions or timers.

## 12. Handoff
Once the Technical Specification is complete and (if necessary) approved by the user, hand off the execution to the `coding-task-planning` skill to break the spec into sequential implementation steps.
