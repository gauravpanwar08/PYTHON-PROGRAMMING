from sqlalchemy import insert, select, update, delete, bindparam
from database import engine
from tables import departments
from tables import employees
from tables import projects
from tables import employee_projects


# -------------- insert departments -------------

# stmt = insert(departments).values(
#     [
#         {"name" : "Engineering"},
#         {"name" : "HR"},
#         {"name" : "Marketing"},
#         {"name" : "Finance"}
#     ]
#     )


# -------------- insert employees -------------

# stmt = insert(employees).values(
#     [
#         {"name":"Gaurav", "email":"gaurav@example.com", "age":23, "department_id":1},
#         {"name":"Ajay", "email":"ajay@example.com", "age":22, "department_id":1},
#         {"name":"Gautam", "email":"gautam@example.com", "age":21, "department_id":2},
#         {"name":"Balram", "email":"balram@example.com", "age":24, "department_id":3},
#         {"name":"Aditya", "email":"aditya@example.com", "age":23, "department_id":4},
#     ]
# )

# -------------- insert projects -------------

# stmt = insert(projects).values(
#     [
#         {"name":"Employee Portal", "description":"Internal employee management system", "department_id":1},
#         {"name":"Recruitment System", "description":"Recruitment and hiring system", "department_id":2},
#         {"name":"Marketing Dashboard", "description":"Marketing analytics dashboard", "department_id":3},
#         {"name":"Finance Tracker", "description":"Financial tracking system", "department_id":4},
#     ]
# )

# ----------Assign Employees to Projects-----------

# stmt = insert(employee_projects).values(
#     [
#         {"employee_id":1, "project_id":1},
#         {"employee_id":2, "project_id":1},
#         {"employee_id":1, "project_id":4},
#         {"employee_id":3, "project_id":2},
#         {"employee_id":4, "project_id":3},
#         {"employee_id":5, "project_id":4},
#     ]
# )


# ---------- update data -----------

# stmt = (
#     update(employees)
#     .where(employees.c.id == bindparam("employee_id"))
#     .values(department_id=bindparam("department_id"))
# )

# with engine.begin() as connection:
#     connection.execute(stmt, [
#         {"employee_id": 1, "department_id": 1},
#         {"employee_id": 2, "department_id": 1},
#         {"employee_id": 3, "department_id": 2},
#         {"employee_id": 4, "department_id": 3},
#         {"employee_id": 5, "department_id": 4},
#     ])


# ------------- execute query ---------------

# with engine.begin() as connection:
#     connection.execute(stmt)


# ------------ select data ---------------

# with engine.connect() as connection:
#     result = connection.execute(select(employee_projects))
#     for row in result:
#         print(row)

def create_department(name):
    with engine.begin() as connection:
        result = connection.execute(insert(departments).values(
                name=name
            ))
        return result.inserted_primary_key[0]


def create_employee(name, email, age, department_id):
    with engine.begin() as connection:
        result = connection.execute(insert(employees).values(
                name=name,
                email=email,
                age=age,
                department_id=department_id,
            ))
        return result.inserted_primary_key[0]


def create_project(name, description, department_id):
    with engine.begin() as connection:
        result = connection.execute(insert(projects).values(
                name=name,
                description=description,
                department_id=department_id,
            ))
        return result.inserted_primary_key[0]


def assign_employee_to_project(employee_id, project_id):
    with engine.begin() as connection:
        result = connection.execute(insert(employee_projects).values(
                employee_id=employee_id,
                project_id=project_id,
            ))
        return result.inserted_primary_key[0]

def get_departments():
    with engine.connect() as connection:
        result = connection.execute(select(departments))
        return result.all()


def get_employees():
    with engine.connect() as connection:
        result = connection.execute(select(employees))
        return result.all()


def get_projects():
    with engine.connect() as connection:
        result = connection.execute(select(projects))
        return result.all()


def get_employee_projects():
    with engine.connect() as connection:
        result = connection.execute(select(employee_projects))
        return result.all()


def get_employee_by_id(employee_id):
    with engine.connect() as connection:
        result = connection.execute(select(employees).where(employees.c.id==employee_id))
        return result.one_or_none()


def update_employee(employee_id, name, email, age, department_id):
    with engine.begin() as connection:
        result = connection.execute(
            update(employees)
            .where(employees.c.id == employee_id)
            .values(name=name, email=email, age=age, department_id=department_id)
        )
        return result


def delete_employee(employee_id):
    with engine.begin() as connection:
        result = connection.execute(
            delete(employees)
            .where(employees.c.id == employee_id)
        )
        return result.rowcount


def get_employees_with_departments():
    with engine.begin() as connection:
        result = connection.execute(
            select(
                employees.c.id,
                employees.c.name,
                employees.c.email,
                employees.c.age,
                departments.c.name,
            ).select_from(
                employees.join(departments, employees.c.department_id == departments.c.id)
            )
        )
        return result.all()


def get_employees_with_projects():
    with engine.connect() as connection:
        result = connection.execute(
            select(employees.c.name, projects.c.name)
            .select_from(employees)
            .join(employee_projects, employees.c.id == employee_projects.c.employee_id)
            .join(projects, employee_projects.c.project_id == projects.c.id)
        )
        return result.all()

def get_employee_department_projects():
    with engine.connect() as connection:
        result = connection.execute(
            select(
                employees.c.name.label("employee_name"),
                departments.c.name.label("department_name"),
                projects.c.name.label("project_name")
                )
            .select_from(employees)
            .join(departments, employees.c.department_id == departments.c.id)
            .join(employee_projects, employees.c.id == employee_projects.c.employee_id)
            .join(projects, employee_projects.c.project_id == projects.c.id)
        )
        return result.all()

    
    
#  ---------- Test functions ---------------

# department_id = create_department("Sales")
# print("Department ID:", department_id)

# employee_id = create_employee(
#     "Rohit",
#     "rohit@example.com",
#     25,
#     5
# )
# print("Employee ID:", employee_id)

# project_id = create_project(
#     "Sales Dashboard",
#     "Sales performance tracking system",
#     5
# )
# print("Project ID:", project_id)

# print(assign_employee_to_project(6, 5))

# departments_list = get_departments()
# for department in departments_list:
#     print(department)

# employees_list = get_employees()
# for employee in employees_list:
#     print(employee)

# employees_list = get_projects()
# for employee in employees_list:
#     print(employee)

# assignments = get_employee_projects()
# for assignment in assignments:
#     print(assignment)

# print(get_employee_by_id(3))
# print(get_employee_by_id(999))

# update_employee(1, "Gaurav", "gaurav@example.com", 24, 1)
# print(get_employee_by_id(1))

# deleted = delete_employee(6)
# print("Deleted rows:", deleted)
# print(get_employee_by_id(6))

# employees_list = get_employees_with_departments()
# for employee in employees_list:
#     print(employee)

# employees_list = get_employees_with_projects()
# for employee in employees_list:
#     print(employee)

employees_list = get_employee_department_projects()
for employee in employees_list:
    print(employee)
