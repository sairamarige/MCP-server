# Calculator + Employee MCP Servers

Two small MCP servers I put together with the Python SDK's FastMCP decorator API.
One does basic math, the other serves up a fake employee directory. Both are meant
as a starting point you can point a real backend at later.

## What's in here

- `calculator_server.py` - add, subtract, multiply, divide
- `employee_server.py` - get_employee, search_employee, employees_by_department
- `requirements.txt` - just `mcp<2.0`

## Getting it running

```bash
pip install -r requirements.txt
python calculator_server.py
```

It'll just sit there waiting for a client to connect over stdio, that's normal.

If you want to poke at it without wiring up a full client, use the inspector:

```bash
mcp dev calculator_server.py
```

That opens a browser tab where you can call each tool by hand and see what
comes back.

### Hooking it up to VS Code

VS Code (Copilot Chat's agent mode) can talk to MCP servers directly. Make a
`.vscode/mcp.json` file in your project root:

```json
{
  "servers": {
    "calculator": {
      "command": "python3",
      "args": ["${workspaceFolder}/calculator_server.py"]
    },
    "employees": {
      "command": "python3",
      "args": ["${workspaceFolder}/employee_server.py"]
    }
  }
}
```

Save that, and VS Code should show a "Start" prompt above the server entries
in the file (or you can start it from the MCP Servers view). Once it's
running, switch Copilot Chat to agent mode and the tools show up as things
it can call.

If you'd rather not create the file by hand, open the Command Palette
(Ctrl+Shift+P) and run `MCP: Add Server` - it walks you through it and
writes the json for you.

One gotcha on Windows: if `python3` isn't recognized in your terminal but
`python` is, just swap the command to `"python"` in the config above.

## How it fits together

The flow is basically: you ask something in chat -> the app decides it needs
a tool -> its MCP client sends a request over to the server -> the server
runs the matching Python function -> the answer travels back the same way.

So for "what's 7 times 6" it goes User -> app -> MCP client -> calculator
server -> the `multiply` function -> back up the chain as 42.

I actually tested this end to end rather than just calling the functions
directly - spun up a real client over stdio, listed the tools, called
`multiply(7, 6)`, got `42.0` back through the whole protocol, not just from
Python. Same idea applies to the employee server, just swap "math" for
"look something up in a list."

The employee data right now is just a hardcoded list in the file. If you
want to hook it up to an actual database or HR system, you'd only touch the
inside of each function - the tool names and what arguments they take don't
need to change.

## The tools

**Calculator**

- `add(a, b)`
- `subtract(a, b)`
- `multiply(a, b)`
- `divide(a, b)` - raises an error instead of returning inf/nan if b is 0

**Employee directory**

- `get_employee(employee_id)` - one record by ID, errors if it doesn't exist
- `search_employee(query)` - case-insensitive match against name, email, or role
- `employees_by_department(department, role=None)` - everyone in a dept,
  optionally narrowed further by role

## One thing to know about versions

The `mcp` package just put out a 2.0 beta that renames `FastMCP` to
`MCPServer` and moves some import paths around, ahead of a protocol change
coming later this year. It's still beta and not every client supports it
yet, so I pinned this to the 1.x line (1.29.0 as of writing) since that's
what actually works with Claude Desktop right now. If you end up wanting
the newer API later, the decorator syntax (`@mcp.tool()`) barely changes -
it's mostly just the import line that's different.

## A heads up on a warning you might see

You might see something like:

```
IncompleteFieldDefinitionWarning: Field 'lifespan' has an incomplete definition...
```

This comes from pydantic_settings, not from anything in these files. It's
harmless - doesn't affect any of the tools - just annoying if you don't
know what it is. If it bugs you, set this env var before running:

```
PYTHONWARNINGS=ignore::UserWarning:pydantic_settings
```
