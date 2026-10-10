---
name: codebase-search
description: Executes semantic, Regex, and AST-aware searches to locate usages, definitions, and dependencies, preventing breaking changes caused by isolated modifications.
---

# 1. Purpose
The primary purpose of `codebase-search` is to locate code safely and accurately **before** making changes. This ensures that modifications to shared UI components, hooks, utility functions, or types do not introduce breaking changes in isolated or dependent parts of the application. Find before you change.

# 2. Trigger Conditions
Invoke this skill under the following circumstances:
- **Before Modifying Shared Code:** When updating the signature, props, or behavior of a shared component, hook, or utility function.
- **Locating Definitions:** When trying to find where a specific state, context, type, or component is initialized.
- **Tracing Dependencies:** When you need to understand how data or control flows through multiple files.
- **Refactoring:** When renaming or moving a file or exported symbol.

# 3. Workspace Scoping
The agent operates within a sandboxed environment. All code lives inside the `/workspace` directory, which may contain multiple projects.
- **Always narrow the search scope:** Target your search to `/workspace/<project-name>/src/` or a specific subdirectory within it.
- **Always exclude build and vendor directories:** Ensure your search excludes `node_modules`, `.git`, `build`, `dist`, `.next`, and `coverage`.
  - Example `grep` flag: `--exclude-dir={node_modules,.git,dist,build,.next}`

# 4. Search Strategies
Use standard Unix tools (or your designated search tool) effectively:
- **`grep` / `ripgrep`:** Ideal for finding exact strings, Regex patterns, or symbol names.
- **`find`:** Ideal for locating files by name, extension, or path pattern.
- **Barrel Files (`index.ts`):** Pay attention to barrel files. If `Button` is exported from `components/index.ts`, consumers will likely import it from the folder rather than the specific file. Check the barrel file exports first.

# 5. Definition Search
To find where a specific entity is defined, use precise queries to filter out usage:
- **Components:** `grep -rnw "export const Button" src/` or `grep -rnw "function Button" src/`
- **Interfaces/Types:** `grep -rnw "interface User" src/` or `grep -rnw "type User" src/`
- **Hooks:** `grep -rnw "export function useUser" src/` or `grep -rn "const useUser = " src/`
- **Default Exports:** `grep -rn "export default function Button" src/`

# 6. Usage Tracing
If you are modifying `ComponentA`, you MUST find all of its parents (consumers).
- **Import Statements:** Search for how it is imported. `grep -rnw "import .* ComponentA" src/`
- **JSX Invocation:** Search for its usage in JSX. `grep -rn "<ComponentA" src/`
- **Hook Usage:** Search for hook calls. `grep -rn "useUser(" src/`
- **Dynamic Imports:** Be aware of `React.lazy` or `next/dynamic` imports.

# 7. Import Chain Analysis
When tracing complex data flows, follow the import chain:
1. Find the definition of `useAuth`.
2. Find all files importing `useAuth`.
3. For a specific consumer `Header.tsx`, find all files importing `Header`.
4. Document this flow hierarchically before making architectural changes.

# 8. Pattern Matching
To find specific React behaviors or anti-patterns, search for exact code constructs:
- **Context:** `grep -rn "createContext(" src/`
- **Effects:** `grep -rn "useEffect(" src/`
- **State:** `grep -rn "useState(" src/`
- **Routes:** Look for `<Route`, `<Link`, or Next.js `useRouter`.
- **API Calls:** `grep -rn "fetch(" src/` or `grep -rn "useQuery(" src/`

# 9. Impact Assessment
If a component, hook, or utility function has **more than 5 consumers**, generating an impact report is mandatory before modifying its signature.
- **Action:** Stop and list all affected files.
- **Review:** Present the list of consumers to the user or cross-reference with the `requirement-analysis` skill to ensure the proposed change scales to all usages without breaking them.
- **Handoff:** If changes span many files, coordinate with `coding-task-planning`.

# 10. Search Commands Reference Table

| Task | Command Example |
| :--- | :--- |
| **Find file by name** | `find /workspace/<project>/src -name "Button.tsx"` |
| **Find component definition** | `grep -rnw '/workspace/<project>/src' -e "export const Button"` |
| **Find component usage (JSX)** | `grep -rn '/workspace/<project>/src' -e "<Button"` |
| **Find named import** | `grep -rn '/workspace/<project>/src' -e "import { Button }"` |
| **Find type definition** | `grep -rnw '/workspace/<project>/src' -e "interface UserData"` |
| **Find string literal** | `grep -rn '/workspace/<project>/src' -e "'/api/v1/users'"` |

*Note: Adjust `/workspace/<project>/src` to match the specific project folder.*

# 11. Anti-patterns
- ❌ **Broad Recursive Searches:** Searching the entire `/workspace` without specifying the project or `src/` directory, causing slow execution and noisy results.
- ❌ **Searching `node_modules`:** Failing to exclude vendor directories, leading to massive output.
- ❌ **Fuzzy Matching for Refactoring:** Relying on loose, case-insensitive searches (e.g., `grep -i "button"`) when precision is needed for renaming a specific component, resulting in false positives.
- ❌ **Blindly Modifying Shared Code:** Changing a prop signature in a component without first searching for and updating all of its consumers.

# 12. Expected Output
When a search is completed, structure the findings clearly before passing them to the next skill (e.g., `implementation` or `coding-task-planning`):
- Provide file paths (relative to `/workspace/<project>/src/`) with exact line numbers.
- Illustrate dependency direction: `[File A (Consumer) -> imports -> File B (Definition)]`.
- Summarize the total number of usages found to trigger Impact Assessment if necessary.
