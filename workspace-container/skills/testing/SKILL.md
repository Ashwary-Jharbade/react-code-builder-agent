---
name: testing
description: Generates automated tests to verify component behavior, prevent regressions, and ensure robustness against edge cases.
---

**Trigger Conditions:**
- After a new feature is fully implemented.
- When explicitly requested by the user ("Write tests for this").

**Execution Protocol:**
1. **Framework Alignment:** Detect test runner (Jest, Vitest) and library (React Testing Library).
2. **Behavioral Targeting:** Query DOM elements exactly as a user would (e.g., `screen.getByRole('button', { name: /submit/i })`).
3. **Mocking Strategy:**
   - Mock network requests using MSW (Mock Service Worker) or `jest.mock`.
   - Wrap components in necessary context providers (e.g., `<ThemeProvider>`, `<Provider store={store}>`) via a custom `render` utility.
4. **Scenario Coverage:** Write assertions for: Happy Path, Loading State, Error State, and Empty State.

**Rules & Constraints:**
- Do not assert on internal component state. Assert on visible DOM changes.
- Ensure all asynchronous `fireEvent` or `userEvent` triggers are awaited inside `act()` if required.

**Output:** 
A fully functional `[component].test.tsx` file that passes without warnings.
