---
name: repository-navigation
description: Intelligently traverses the file system using architectural heuristics rather than exhaustive directory scanning, minimizing token usage and context pollution.
---

**Trigger Conditions:**
- The user requests a modification to a specific feature, page, or component.
- The agent needs to locate the entry point of the application.

**Execution Protocol:**
1. **Heuristic Mapping:** Identify the active design pattern (e.g., Atomic Design `atoms/`, `molecules/`, or Feature-based `features/auth/`).
2. **Targeted Drill-down:** If modifying a "Header", check `components/layout/Header` or `components/Header` before searching globally.
3. **Relative Path Resolution:** When navigating between files, calculate exact relative paths (e.g., `../../utils/helpers`) to ensure imports will not break.

**Rules & Constraints:**
- Do not list or read directories blindly (e.g., do not `ls -R node_modules` or `.git`).
- Validate file existence before attempting to open or modify.

**Output:** 
Validated file paths and a localized mental map of the current feature's directory.