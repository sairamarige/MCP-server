# Employee Server Permissions

Adds role-based access control to `employee_server.py` from Day 33. Four scopes,
three roles, enforced inside each tool handler (not just hidden from a menu).

## Scopes

| Scope | Tool(s) it gates |
|---|---|
| `employee:read` | `get_employee` |
| `employee:search` | `search_employee`, `employees_by_department` |
| `employee:update` | `update_employee` |
| `employee:delete` | `delete_employee` |

`whoami` is unscoped on purpose - a caller should always be able to check what
they're allowed to do.

## Roles

| Role | Scopes |
|---|---|
| `employee` | read, search |
| `hr_manager` | read, search, update |
| `hr_admin` | read, search, update, delete |

Each tier is a strict superset of the one below it, and that's written out
explicitly in `ROLE_PERMISSIONS` rather than inherited - a flat table is
easier to audit than a chain of "inherits from X."

## How identity works here

This server runs as one stdio process per launch with no HTTP layer, so
there's no per-request token to read a role off of. Identity is simulated
the same way: one role per process, set via the `EMPLOYEE_ROLE` environment
variable before launch (defaults to `employee` if unset).

See `mcp.json` for three ready-to-use entries - `employees_as_employee`,
`employees_as_hr_manager`, `employees_as_hr_admin` - so you can point a
client at any of the three roles and see the permission boundary in action.

If this ever moves to `streamable-http`/SSE with real auth, only `CURRENT_ROLE`
needs to change (pull it from the request's auth context instead of
`os.environ`). `ROLE_PERMISSIONS` and `require_scope()` stay the same.

## Enforcement point

Every gated tool is wrapped with `@require_scope("...")`, applied *under*
`@mcp.tool()` so it runs before the tool body on every call:

```python
@mcp.tool()
@require_scope("employee:update")
def update_employee(...):
    ...
```

A denied call raises `PermissionDenied`, which surfaces to the client as a
tool error - not a silently empty result and not a hidden tool. The tool
still shows up in `list_tools()` for every role; the check happens when
it's actually invoked. That's deliberate: hiding a tool from a menu is a
UX nicety, not a security control, since nothing stops a client from
calling it by name regardless of what's listed.

## Other decisions baked in

- **`delete_employee` is a soft delete.** It flips an `active` flag rather
  than removing the record, so `get_employee` / `search_employee` /
  `employees_by_department` all filter to `active` employees. Cheap to
  recover from a mistake; the record isn't gone, just hidden from normal
  reads.
- **`update_employee` can't touch `id` or `active`.** Those aren't exposed
  as update parameters at all, so there's no path to reactivating a
  deleted record or reassigning an ID through the update tool.
- **Audit logging on `update` and `delete` only.** These are the two
  scopes that mutate data, so every call to either prints an
  `[AUDIT]` line with role, tool, and arguments. Swap `print()` for a real
  log sink in production; `read`/`search` aren't logged since they don't
  change anything.
- **No `employee:update_self`.** A normal `employee` can't update their own
  record with this design - only `hr_manager`+ can update anyone. If you
  want self-service (e.g. an employee changing their own phone number),
  that's a separate scope, not a bump to `hr_manager`, so it doesn't also
  grant the ability to edit *other* people's records.
