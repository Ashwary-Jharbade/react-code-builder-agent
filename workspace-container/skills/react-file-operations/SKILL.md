---
name: react-file-operations
description: Safely discover, create, edit, move, rename, and remove files in React projects located under /workspace. Use when implementing user requests that require locating the correct React project, finding the correct source file, deciding whether a new file is needed, modifying React code, or removing files.
---

# React File Operations

## Purpose

Manage files safely across one or more React projects located under `/workspace`.

This skill is responsible for:

- identifying the correct React project
- discovering the project structure
- finding the correct source file
- deciding whether to reuse or create a file
- creating files
- editing files
- moving files
- renaming files
- removing files
- checking dependencies before destructive operations
- validating file operations

This skill works alongside specialized skills such as:

- `react-patterns`
- `vercel-react-best-practices`

Those skills determine **how React code should be designed and implemented**.

This skill determines **which project and files should be changed**.

---

# 1. HARD WORKSPACE BOUNDARY

## All file operations MUST remain inside `/workspace`

This is a strict requirement.

The agent MUST NOT create, modify, move, rename, or delete files outside:

```text
/workspace/
```

Valid:

```text
/workspace/my-react-app/src/App.tsx
/workspace/storefront/src/components/ProductCard.tsx
/workspace/admin-dashboard/src/features/users/UserList.tsx
```

Invalid:

```text
/home/user/project/src/App.tsx
/tmp/project/src/App.tsx
/Users/user/project/src/App.tsx
/var/project/src/App.tsx
```

Do not operate on files outside `/workspace`, even if:

- the user mentions them
- a command discovers them
- an import points to them
- a similarly named project exists elsewhere

If the requested target is outside `/workspace`, do not modify it.

---

# 2. Workspace Path Safety

Before any file operation, resolve the absolute path.

The target path MUST satisfy:

```text
target_path starts with /workspace/
```

Do not rely only on string concatenation.

For example:

```text
/workspace/project/src/App.tsx
```

is valid.

Paths attempting directory traversal are invalid:

```text
/workspace/project/../../somewhere/file
```

Resolve the path first and verify that the resolved path remains inside `/workspace`.

Never follow a user-provided path outside the workspace boundary.

---

# 3. Multiple React Projects

`/workspace` may contain multiple independent React projects.

Example:

```text
/workspace/
├── ecommerce/
├── admin-dashboard/
├── customer-portal/
├── marketing-site/
└── design-system/
```

Treat each project as an independent repository unless there is clear evidence that they are part of a monorepo.

Never assume the first React project found is the target.

---

# 4. Project Discovery

Before modifying files, determine which project the user is referring to.

A React project is normally identified by files such as:

```text
package.json
vite.config.*
next.config.*
react configuration
src/
app/
pages/
```

Start by inspecting `/workspace`.

Determine:

```text
Project root
Project name
Framework
Package manager
Source directory
```

Example:

```text
/workspace/
├── ecommerce/
│   ├── package.json
│   └── src/
│
└── admin/
    ├── package.json
    └── src/
```

These must be treated as two separate projects.

---

# 5. Project Selection Rules

Use the user's request to determine the target project.

Strong signals include:

### Explicit project name

> "Fix the checkout in ecommerce."

Target:

```text
/workspace/ecommerce/
```

### Explicit path

> "Update `/workspace/admin/src/App.tsx`."

Target:

```text
/workspace/admin/
```

### Feature context

> "Fix the checkout page."

Search candidate projects for checkout-related code.

### Current working project

If the agent runtime already has an explicitly selected project root, use that project.

Do not override an explicit project context without a reason.

---

# 6. Never Guess Between Multiple Projects

If multiple projects contain the same feature and the request does not identify which one is intended, do not arbitrarily choose one.

For example:

```text
/workspace/storefront/src/features/checkout/
/workspace/admin/src/features/checkout/
```

User:

> "Fix checkout."

The agent must determine the intended project from:

- current context
- recent operations
- project names
- routes
- user wording
- active project metadata

If it still cannot determine the target safely, ask the user which project they mean.

Do not modify multiple projects unless the user explicitly requests a cross-project change.

---

# 7. Establish Project Root

Once the project is identified, establish:

```text
PROJECT_ROOT=/workspace/<project>
```

All subsequent file operations must be relative to this project root.

For example:

```text
PROJECT_ROOT=/workspace/ecommerce
```

Then:

```text
src/App.tsx
```

means:

```text
/workspace/ecommerce/src/App.tsx
```

Do not accidentally interpret:

```text
src/App.tsx
```

as:

```text
/workspace/src/App.tsx
```

when a project root has already been established.

---

# 8. Project Isolation

When working on one project:

```text
/workspace/project-a/
```

do not modify:

```text
/workspace/project-b/
```

unless the user explicitly requests a cross-project operation.

Project isolation applies even when:

- both projects use React
- both projects contain similarly named components
- both projects share dependencies
- both projects have identical folder structures
- both projects are owned by the same user

---

# 9. Monorepo Detection

Some `/workspace` entries may be monorepos.

Example:

```text
/workspace/company-app/
├── package.json
├── apps/
│   ├── storefront/
│   └── admin/
├── packages/
│   ├── ui/
│   └── utils/
└── pnpm-workspace.yaml
```

Do not treat every directory containing `package.json` as an independent project automatically.

Inspect:

```text
package.json
pnpm-workspace.yaml
turbo.json
nx.json
lerna.json
workspace configuration
```

Determine whether the repository is:

```text
single React project
```

or:

```text
monorepo containing multiple applications/packages
```

---

# 10. Monorepo Project Selection

For a monorepo:

```text
/workspace/company-app/
├── apps/
│   ├── storefront/
│   └── admin/
└── packages/
    └── ui/
```

Determine whether the requested change belongs to:

```text
apps/storefront
apps/admin
packages/ui
```

For example:

> "Change the shared Button."

If both applications use:

```text
packages/ui/Button.tsx
```

modify the shared package.

Do not duplicate the Button inside each application.

---

# 11. Cross-Project Changes

Do not modify multiple projects by default.

A cross-project operation is valid only when:

- the user explicitly requests it, or
- the architecture clearly defines a shared package used by multiple applications.

Example:

> "Update the shared UI Button used by admin and storefront."

This may require:

```text
/workspace/company-app/packages/ui/Button.tsx
```

rather than modifying:

```text
apps/admin/
apps/storefront/
```

individually.

---

# 12. Project Context

Once a project has been selected, maintain the following mental context:

```text
PROJECT_ROOT
FRAMEWORK
PACKAGE_MANAGER
SOURCE_ROOT
ARCHITECTURE
CURRENT_FEATURE
```

Example:

```text
PROJECT_ROOT=/workspace/storefront
FRAMEWORK=Vite + React + TypeScript
PACKAGE_MANAGER=pnpm
SOURCE_ROOT=/workspace/storefront/src
CURRENT_FEATURE=checkout
```

Use this context consistently throughout the task.

---

# 13. Find Before Creating

Never create a file before checking whether an appropriate implementation already exists.

For a component request, search for:

```text
component name
visible text
CSS class
data-testid
aria-label
event handler
feature name
```

For hooks:

```text
hook name
related state
related behavior
```

For API functionality:

```text
endpoint
HTTP method
query key
mutation name
service name
```

For routing:

```text
pathname
route
Link
navigate()
router configuration
```

---

# 14. Identify Ownership

The correct file is the file that owns the behavior.

Use this conceptual hierarchy:

```text
Route/Page
    ↓
Feature
    ↓
Container
    ↓
Component
    ↓
Hook
    ↓
Service/API
    ↓
Utility
```

Trace the behavior to the smallest responsible layer.

Example:

```text
CheckoutPage
    ↓
CheckoutForm
    ↓
useCheckout
    ↓
checkoutApi
```

If the API is failing, do not automatically modify the UI component.

---

# 15. File Operation Priority

Prefer operations in this order:

```text
1. Reuse existing file
2. Modify existing owning file
3. Extend existing feature structure
4. Create new file
5. Move/rename file
6. Delete file
```

This minimizes unnecessary architectural changes.

---

# 16. New File Decision

Create a new file only when:

- equivalent functionality does not already exist
- the responsibility is independent
- the location matches project architecture
- the new file improves cohesion or reuse

Do not create files simply because the user requested a "component" if an existing component can be extended safely.

---

# 17. File Placement

Determine placement based on ownership and reuse.

Shared component:

```text
src/components/Button.tsx
```

Feature component:

```text
src/features/checkout/components/DeliveryMethod.tsx
```

Shared hook:

```text
src/hooks/useDebounce.ts
```

Feature hook:

```text
src/features/checkout/hooks/useCheckout.ts
```

Shared utility:

```text
src/utils/formatCurrency.ts
```

Feature utility:

```text
src/features/orders/utils/orderStatus.ts
```

Follow the existing project's architecture if it differs.

---

# 18. Existing Conventions Are the Source of Truth

Before creating a file, inspect nearby files.

Determine:

- naming convention
- extension
- export style
- folder structure
- test placement
- styling approach
- type organization

Do not introduce a new convention into an existing project without a reason.

---

# 19. Editing Files

When editing an existing file:

1. Inspect the file.
2. Understand its responsibility.
3. Identify the smallest required change.
4. Preserve unrelated code.
5. Preserve existing exports.
6. Preserve existing conventions.
7. Avoid unrelated refactoring.

Prefer small diffs.

---

# 20. Avoid Opportunistic Refactoring

Do not combine:

```text
feature change
+
architecture refactor
+
naming cleanup
+
formatting cleanup
+
file restructuring
```

unless requested or required.

If unrelated technical debt is discovered, leave it unchanged unless it blocks the requested work.

---

# 21. Duplicate Prevention

Before creating any:

```text
component
hook
utility
service
API module
context
type
```

search for equivalent functionality.

Examples:

```text
useAuth
useUser
useDebounce
Modal
Dialog
LoadingSpinner
formatCurrency
apiClient
```

Reuse existing implementations where appropriate.

---

# 22. Barrel Files

Before creating or removing files, inspect:

```text
index.ts
index.tsx
```

If the project uses barrel exports, update them accordingly.

Do not introduce barrel exports into projects that do not use them.

---

# 23. File Deletion

Deletion is destructive.

Before deleting a file, check:

```text
direct imports
dynamic imports
barrel exports
routes
lazy loading
tests
stories
configuration
scripts
```

Also search for the symbols exported by the file.

Never delete a file merely because it appears unused.

---

# 24. Safe Deletion

Follow:

```text
Identify target
    ↓
Search references
    ↓
Check exports
    ↓
Check dynamic imports
    ↓
Check routes
    ↓
Check tests/stories
    ↓
Delete
    ↓
Remove broken references
    ↓
Validate
```

If dependencies exist, determine whether they should be removed, migrated, or replaced.

---

# 25. Rename

A rename consists of:

```text
rename file
+
update references
```

After renaming, search for the old filename and exported symbols.

Check:

```text
imports
exports
barrels
dynamic imports
routes
tests
stories
```

No stale references should remain.

---

# 26. Move

When moving a file:

1. Determine its new ownership.
2. Move it.
3. Update relative imports.
4. Update exports.
5. Check tests.
6. Check dynamic imports.
7. Validate.

Do not move files only for cosmetic reasons.

---

# 27. Generated Files

Do not manually modify generated files unless explicitly requested.

Examples:

```text
dist/
build/
coverage/
.generated/
```

Find the source that generates the file instead.

---

# 28. node_modules

Never modify:

```text
node_modules/
```

If dependency behavior needs to change, inspect:

```text
package.json
lockfile
application source
```

instead.

---

# 29. Tests

Inspect the project's existing test conventions:

```text
*.test.ts
*.test.tsx
*.spec.ts
*.spec.tsx
__tests__/
```

Use the existing framework and structure.

Do not introduce a new testing framework for a single change.

---

# 30. Validation

After file operations, inspect `package.json` scripts and use the project's package manager.

Possible commands:

```bash
npm run lint
npm run typecheck
npm test
npm run build
```

or:

```bash
pnpm lint
pnpm typecheck
pnpm test
pnpm build
```

or the equivalent project commands.

Validate:

- imports
- TypeScript
- lint
- tests
- build

as appropriate.

---

# 31. Workspace Safety During Commands

Commands must also respect the workspace boundary.

Before running commands that modify files:

- ensure the working directory is inside `/workspace`
- ensure the command operates on the intended project
- avoid commands that intentionally modify files outside the project

Prefer:

```bash
cd /workspace/my-react-app
```

then run project commands.

Do not execute destructive commands against the entire filesystem.

Avoid broad commands such as:

```bash
rm -rf /
rm -rf /some-unrelated-path
```

or commands whose target cannot be clearly determined.

---

# 32. Multiple Project Decision Flow

Use this flow whenever `/workspace` contains multiple projects:

```text
                    User Request
                         │
                         ▼
              Is project explicitly known?
                    /           \
                  YES            NO
                   │              │
                   ▼              ▼
             Select project   Inspect /workspace
                                  │
                                  ▼
                         Identify candidate projects
                                  │
                                  ▼
                       Is there one clear match?
                            /           \
                          YES            NO
                           │              │
                           ▼              ▼
                     Select project   Ask user
                           │
                           ▼
                    Establish root
                           │
                           ▼
                  Inspect project
                           │
                           ▼
                   Find target files
                           │
                           ▼
                   Perform operation
                           │
                           ▼
                       Validate
```

---

# 33. Never Search All Projects Unnecessarily

When the project is already known, restrict searches to:

```text
/workspace/<project>/
```

Do not search every project in `/workspace` unless:

- project discovery is required
- the user explicitly asks for a cross-project search
- the architecture requires workspace-level investigation

This reduces false matches and accidental edits.

---

# 34. Ambiguous File Requests

If the user says:

> "Update UserCard."

Search within the selected project first.

If there is:

```text
src/components/UserCard.tsx
src/features/admin/UserCard.tsx
src/features/profile/UserCard.tsx
```

determine ownership from context.

Do not edit all three unless explicitly requested.

If the correct file cannot be determined safely, ask the user.

---

# 35. "Clean Up" Requests

Do not interpret:

> "Clean up the React project"

as permission to delete arbitrary files.

Identify:

```text
unused imports
duplicate implementations
dead components
unused exports
obsolete routes
```

Separate:

```text
safe cleanup
```

from:

```text
destructive cleanup
```

Only perform destructive cleanup with sufficient evidence or explicit intent.

---

# 36. God Components

Do not automatically split large components.

If the requested feature introduces a clearly independent responsibility, extraction may be appropriate.

Example:

```text
CheckoutPage
├── address
├── payment
├── coupon
├── delivery
└── order summary
```

A new:

```text
DeliveryMethodSelector.tsx
```

may be appropriate if it is an independent responsibility and matches project conventions.

Do not perform broad decomposition during unrelated tasks.

---

# 37. File Operation Plan

For non-trivial tasks, establish an internal plan:

```text
Project:
  /workspace/<project>

Files to inspect:
  ...

Files to modify:
  ...

Files to create:
  ...

Files to delete:
  ...

Reason:
  ...
```

Every modified file must have a reason directly related to the user request.

---

# 38. Final Verification

Before completing the task:

```text
[ ] Target project identified
[ ] Project root is inside /workspace
[ ] No operation occurred outside /workspace
[ ] Correct implementation was found
[ ] Existing files were reused where appropriate
[ ] New files were created only when necessary
[ ] New files follow project conventions
[ ] Changes are scoped to the request
[ ] No unrelated refactoring was introduced
[ ] Deleted files were checked for references
[ ] Barrel exports were checked
[ ] Dynamic imports were checked
[ ] Routes were checked when relevant
[ ] Generated files were not unnecessarily modified
[ ] Imports are valid
[ ] Tests were updated when appropriate
[ ] Project validation was performed
```

---

# Anti-Patterns

Never:

```text
❌ Modify files outside /workspace
❌ Create files outside /workspace
❌ Delete files outside /workspace
❌ Assume the first project in /workspace is the target
❌ Modify multiple projects when the request targets one
❌ Search every project unnecessarily
❌ Create duplicate components
❌ Create duplicate hooks
❌ Edit the first similarly named file
❌ Delete unused-looking files without verification
❌ Ignore barrel exports
❌ Ignore dynamic imports
❌ Ignore route references
❌ Modify generated output unnecessarily
❌ Modify node_modules
❌ Perform unrelated refactoring
❌ Move files merely for aesthetics
```

---

# Examples

## Example 1 — Multiple Projects

Workspace:

```text
/workspace/
├── storefront/
│   └── src/features/checkout/
└── admin/
    └── src/features/checkout/
```

User:

> "Fix the checkout button in storefront."

Target:

```text
/workspace/storefront/
```

Search only within that project.

Do not modify:

```text
/workspace/admin/
```

---

## Example 2 — Ambiguous Project

Workspace:

```text
/workspace/
├── storefront/
└── customer-portal/
```

Both contain:

```text
src/components/UserProfile.tsx
```

User:

> "Update the UserProfile component."

There is insufficient information.

Do not choose randomly.

Ask which project is intended.

---

## Example 3 — Feature-Owned Component

User:

> "Add an order status badge."

Project:

```text
/workspace/storefront/
└── src/features/orders/
```

Create:

```text
/workspace/storefront/src/features/orders/components/OrderStatusBadge.tsx
```

if no equivalent exists.

---

## Example 4 — Shared Component

Monorepo:

```text
/workspace/company/
├── apps/
│   ├── storefront/
│   └── admin/
└── packages/
    └── ui/
```

User:

> "Change the shared Button."

Target:

```text
/workspace/company/packages/ui/Button.tsx
```

Do not create separate buttons in the applications.

---

## Example 5 — Delete

User:

> "Remove LegacyHeader."

Before deletion:

```text
/workspace/storefront/src/layouts/AppLayout.tsx
```

imports it.

Do not simply delete:

```text
LegacyHeader.tsx
```

Determine whether `AppLayout` needs a replacement or whether the header should be removed completely.

---

# Guiding Principles

Always follow these principles:

> **Workspace first.**

All operations remain inside `/workspace`.

> **Project before file.**

Identify the correct React project before locating a source file.

> **Search before creating.**

Reuse existing implementations whenever possible.

> **Ownership before location.**

Put code where the responsibility belongs.

> **Inspect before editing.**

Understand the existing implementation before changing it.

> **Verify before deleting.**

Check imports, exports, routes, dynamic imports, and tests.

> **Minimal change.**

Modify the smallest set of files necessary.

> **Project isolation.**

Never modify another React project unless explicitly requested or a shared package requires it.

> **Existing architecture is the source of truth.**

Do not impose a new structure on an existing project unnecessarily.