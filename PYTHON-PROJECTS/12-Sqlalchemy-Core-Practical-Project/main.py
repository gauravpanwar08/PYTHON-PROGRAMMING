
from database import engine, metadata

# Create tables
metadata.create_all(engine)


from queries import (
    search_employees,
    get_employees_sorted,
    get_employees_paginated,
    get_employee_count,
    get_average_age,
    get_employee_count_by_department,
    department_employee_report,
    employee_age_rank
)
from crud import get_employees_with_projects

from utils import (
    get_database_version,
    show_database_info
)


def main():
    print("\n--- Search Employees ---")
    print(search_employees("Gau"))

    print("\n--- Sorted Employees ---")
    print(get_employees_sorted())

    print("\n--- Paginated Employees ---")
    print(get_employees_paginated(1, 3))

    print("\n--- Employee Count ---")
    print(get_employee_count())

    print("\n--- Average Age ---")
    print(get_average_age())

    print("\n--- Department Employee Count ---")
    print(get_employee_count_by_department())

    print("\n--- Employees With Projects ---")
    print(get_employees_with_projects())

    print("\n--- Department Report ---")
    print(department_employee_report())

    print("\n--- Employee Age Rank ---")
    print(employee_age_rank())

    print("\n--- Database Version ---")
    print(get_database_version())

    print("\n--- Database Info ---")
    show_database_info()


if __name__ == "__main__":
    main()
