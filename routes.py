"""
    Modulos para inicializar el servidor con FastAPI y establecer conección con la BD
"""

from fastapi import FastAPI
from conecction import Employee, EmployeeDB

app = FastAPI()

# Crea una instancia de la clase EmployeeDB
employee_db = EmployeeDB()

# Crea las tablas necesarias en la base de datos
employee_db.create_tables()


@app.get("/")
def read_root():
    """Funcion que define la ruta inicial"""
    return {"message": "Bienvenido a mi aplicación FastAPI"}


@app.post("/employees")
def add_employee(employee: Employee):
    """Función que define la ruta para insertar datos de empleados mediante metodo POST"""
    # Añade el empleado a la base de datos
    employee_db.insert_employee(employee.dict())
    return {"message": "Employee added successfully"}


@app.get("/employees")
def get_employees():
    """Function que define la ruta para obtener datos de empleados mediante metodo GET"""

    # Obtiene todos los empleados de la base de datos
    employees = employee_db.get_employees()
    return employees
