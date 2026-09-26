from database import engine
from tables import employees


def transfer_employee(employee_id, department_id):
    try:
        with engine.begin() as connection:
            connection.execute(
                employees.update()
                .where(employees.c.id == employee_id)
                .values(department_id=department_id)
            )

        return True

    except Exception as error:
        print("Transaction failed:", error)
        return False
