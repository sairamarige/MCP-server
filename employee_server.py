from typing import Optional

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("EmployeeDirectory")


EMPLOYEES: list[dict] = [
    {
        "id": 1,
        "name": "Alice Johnson",
        "department": "Engineering",
        "role": "Senior Software Engineer",
        "email": "alice.johnson@company.com",
        "location": "Hyderabad",
    },
    {
        "id": 2,
        "name": "Brian Chen",
        "department": "Engineering",
        "role": "Engineering Manager",
        "email": "brian.chen@company.com",
        "location": "Bengaluru",
    },
    {
        "id": 3,
        "name": "Chloe Davis",
        "department": "Sales",
        "role": "Account Executive",
        "email": "chloe.davis@company.com",
        "location": "Mumbai",
    },
    {
        "id": 4,
        "name": "David Patel",
        "department": "Sales",
        "role": "VP of Sales",
        "email": "david.patel@company.com",
        "location": "Delhi",
    },
    {
        "id": 5,
        "name": "Emma Wilson",
        "department": "Marketing",
        "role": "Marketing Specialist",
        "email": "emma.wilson@company.com",
        "location": "Hyderabad",
    },
    {
        "id": 6,
        "name": "Farhan Ahmed",
        "department": "Engineering",
        "role": "DevOps Engineer",
        "email": "farhan.ahmed@company.com",
        "location": "Pune",
    },
    {
        "id": 7,
        "name": "Grace Lee",
        "department": "Human Resources",
        "role": "HR Business Partner",
        "email": "grace.lee@company.com",
        "location": "Bengaluru",
    },
    {
        "id": 8,
        "name": "Henry Kumar",
        "department": "Finance",
        "role": "Financial Analyst",
        "email": "henry.kumar@company.com",
        "location": "Mumbai",
    },
]

# Index by ID for O(1) lookups in get_employee.
_EMPLOYEES_BY_ID = {emp["id"]: emp for emp in EMPLOYEES}


@mcp.tool()
def get_employee(employee_id: int) -> dict:
    """Fetch a single employee record by their unique ID.

    Args:
        employee_id: The employee's numeric ID.

    Returns:
        The employee's full record.

    Raises:
        ValueError: If no employee exists with the given ID.
    """
    employee = _EMPLOYEES_BY_ID.get(employee_id)
    if employee is None:
        raise ValueError(f"No employee found with id {employee_id}.")
    return employee


@mcp.tool()
def search_employee(query: str) -> list[dict]:
    """Search employees by a free-text query.

    Matches (case-insensitively) against name, email, and role. Useful when
    the caller doesn't know the exact ID or department.

    Args:
        query: Search text, e.g. a full or partial name ("davis"),
            an email fragment ("alice"), or a role keyword ("engineer").

    Returns:
        A list of matching employee records (empty list if none match).
    """
    q = query.strip().lower()
    if not q:
        return []
    return [
        emp
        for emp in EMPLOYEES
        if q in emp["name"].lower()
        or q in emp["email"].lower()
        or q in emp["role"].lower()
    ]


@mcp.tool()
def employees_by_department(department: str, role: Optional[str] = None) -> list[dict]:
    """List all employees in a given department, optionally filtered by role.

    Args:
        department: Department name, e.g. "Engineering", "Sales",
            "Marketing", "Human Resources", "Finance". Matched
            case-insensitively.
        role: Optional role keyword to further filter results
            (case-insensitive substring match against each employee's role).

    Returns:
        A list of matching employee records (empty list if none match).
    """
    dept = department.strip().lower()
    results = [emp for emp in EMPLOYEES if emp["department"].lower() == dept]
    if role:
        r = role.strip().lower()
        results = [emp for emp in results if r in emp["role"].lower()]
    return results


if __name__ == "__main__":
    mcp.run()
