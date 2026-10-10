---
name: testing
description: Generates automated tests to verify component behavior, prevent regressions, and ensure robustness against edge cases.
---

## 1. Purpose
The `testing` skill is responsible for generating robust automated tests that verify component behavior, prevent regressions, and thoroughly cover edge cases. It ensures that changes do not break existing functionality and that new features meet their specified requirements.

## 2. Trigger Conditions
- **Post-Implementation:** After a new feature or component is fully implemented (often following the `implementation` skill).
- **User Request:** When the user explicitly requests tests (e.g., "Write tests for the UserProfile component").
- **Bug Fix Verification:** After resolving a bug (following the `debugging` skill), to ensure the issue is fixed and will not regress.

## 3. Test Framework Detection
Before writing tests, determine the project's testing stack by inspecting `package.json` and configuration files:
- **Test Runner:** Check for `jest` or `vitest`. (If `vite.config.ts` has `test` or `vitest.config.ts` exists, it's likely Vitest).
- **Testing Libraries:** Check for `@testing-library/react` and `@testing-library/user-event`.
- **Setup Files:** Look for `setupTests.ts` or `setupTests.js` to understand globally available matchers (e.g., `@testing-library/jest-dom`).

## 4. Test File Placement
Follow the project's existing conventions for test file placement:
- **Co-located (Preferred):** Place tests next to the component they test (e.g., `src/components/Button/Button.test.tsx`).
- **`__tests__` Directory:** If the project uses a separate test directory, place it there (e.g., `src/components/Button/__tests__/Button.test.tsx`).
- **Naming Conventions:** Use `.test.tsx` or `.spec.tsx` for React components. Match the casing of the component file.

## 5. Testing Philosophy
- **Test Behavior, Not Implementation:** Focus on what the user sees and interacts with, rather than how the component achieves it. Avoid asserting on internal state (`useState`), instance methods, or component lifecycle events.
- **Query Like a User:** Use queries that resemble how a user interacts with the application (e.g., finding elements by their accessible role or label rather than internal classes or IDs).

## 6. Query Priority (React Testing Library)
Always use the most semantic query available, following this priority order:
1. **`getByRole`:** The preferred way to query elements. (e.g., `getByRole('button', { name: /submit/i })`).
2. **`getByLabelText`:** Essential for form fields.
3. **`getByPlaceholderText`:** Useful for inputs without labels (though labels are preferred).
4. **`getByText`:** Good for non-interactive elements like paragraphs or headings.
5. **`getByDisplayValue`:** Useful for checking the current value of form elements.
6. **`getByAltText`:** Used for images.
7. **`getByTitle`:** Used for SVG or elements with a title attribute.
8. **`getByTestId`:** The fallback option. Use only when semantic queries are impossible or impractical (e.g., dynamic elements without text or roles).

## 7. Scenario Coverage Matrix
Ensure tests cover the following scenarios for every component:
- **Happy Path:** The primary, successful flow (e.g., form submission with valid data).
- **Loading State:** Verify that loading indicators (spinners, skeletons) appear when data is fetching, and interactive elements are disabled.
- **Error State:** Verify that error messages are displayed when operations fail.
- **Empty State:** Verify the UI when there is no data to display.
- **Edge Cases & Boundary Values:** Test unusual inputs, extremely long text, or zero/negative values.

## 8. Mocking Strategy
- **Network Requests:** Prefer using MSW (Mock Service Worker) for API mocking. If MSW is unavailable, use `jest.mock` or `vi.mock` on the API client module (e.g., `axios` or `fetch`).
- **Child Components:** Rarely mock child components unless they are extremely complex or slow down tests significantly. Test the integration where possible.
- **Third-Party Libraries:** Mock third-party libraries if they make tests difficult to run in a Node environment (e.g., charting libraries, canvas integrations, or external APIs).

## 9. Context/Provider Wrapping
Components often rely on context (Theme, Redux, React Query, Router).
- Look for a custom `render` utility in the project (e.g., `src/test-utils.tsx`).
- If no custom render exists, manually wrap the component in the necessary providers in a `beforeEach` or wrapper component within the test.
- Example: `render(<MemoryRouter><ThemeProvider><MyComponent /></ThemeProvider></MemoryRouter>)`

## 10. Async Testing
- **`findBy*` Queries:** Use `await screen.findByRole(...)` to wait for elements that appear asynchronously (e.g., after a network request).
- **`waitFor`:** Use `await waitFor(() => expect(...))` when asserting on a condition that takes time, or when multiple elements change simultaneously.
- **`act()`:** React Testing Library generally wraps interactions in `act()` automatically, but explicit `act()` usage may be necessary when triggering state updates outside of user events (e.g., timer advancements or raw promises).

## 11. User Interaction Testing
- **`userEvent` vs `fireEvent`:** Always prefer `@testing-library/user-event` over `fireEvent`. `userEvent` simulates full browser interactions (e.g., typing triggers keydown, keypress, input, keyup events).
- **Setup:** `const user = userEvent.setup();` at the beginning of the test.
- **Interactions:** `await user.click(button);`, `await user.type(input, 'hello');`.

## 12. Snapshot Testing
- Use snapshot testing sparingly. They are prone to false positives when insignificant styling or markup changes occur.
- Best used for highly stable components (e.g., core design system elements) or to capture large, complex data structures.
- Do not use snapshots as a replacement for explicit behavioral assertions.

## 13. Test Quality Rules
- **Meaningful Assertions:** Ensure every test has at least one assertion that verifies the intended outcome.
- **Descriptive Names:** Write clear `describe` and `it`/`test` blocks. (e.g., `it('should display an error message when the network request fails')`).
- **Isolation:** Tests should not depend on each other. Clean up mocks and state between tests (usually handled by RTL automatically, but be mindful of global state or timers).

## 14. Running Tests
To verify tests pass, execute the appropriate command based on the framework:
- **Jest:** `npm run test` or `npx jest --watch=false`
- **Vitest:** `npm run test` or `npx vitest run`
- Use the `run_command` tool to execute tests and capture the output.

## 15. Anti-patterns
- **Testing Implementation Details:** Asserting on internal state, checking if a specific method was called (unless it's an external side-effect).
- **Brittle Selectors:** Querying by CSS classes or complex DOM structures (e.g., `document.querySelector('.my-class > div > span')`).
- **Testing Third-Party Libraries:** Do not write tests that solely verify the functionality of a dependency (e.g., testing that React Router handles navigation correctly). Trust the library; test your usage of it.
