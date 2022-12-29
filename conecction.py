"""
Módulo para gestionar la base de datos de empleados y horas de trabajo.

"""
import sqlite3
from typing import Dict, Any
from pydantic import BaseModel


class Employee(BaseModel):
    """
    Clase para definir la estructura de propiedades los Empleados
    """

    name: str
    salary: float
    bonuses: float


class Singleton:
    """
    Clase para garantizar que solo existe una única instancia del objeto de conexión
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance


class EmployeeDB(Singleton):
    """
    Clase para gestionar la base de datos de empleados y horas de trabajo.

    """

    def __init__(self):
        self.database = "database.db"

    def create_tables(self):
        """
        Metodo para crear las tablas dentro de la base de datos

        """
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS employees
                 (id INTEGER PRIMARY KEY, name TEXT, salary REAL, bonuses REAL)"""
            )
            cursor.execute(
                """CREATE TABLE IF NOT EXISTS horas
                 (id INTEGER PRIMARY KEY, fecha DATE, employee_id INTEGER, entrada TEXT,
                  salida TEXT, FOREIGN KEY(employee_id) REFERENCES employees(id))"""
            )
            connection.commit()
            cursor.close()

    def insert_employee(self, employee: Dict[str, Any]):
        """Metodo parara insertar empleados en la base de datos

        Args:
            employee (Dict[str, Any]): Diccionario con los campos correspondiente al empleado
        """
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            # Recupera los datos del empleado
            name = employee["name"]
            salary = employee["salary"]
            bonuses = employee["bonuses"]

            # Ejecuta una consulta para añadir el empleado
            cursor.execute(
                "INSERT INTO employees (name, salary, bonuses) VALUES (?, ?, ?)",
                (name, salary, bonuses),
            )

            # Guarda los cambios
            connection.commit()
            cursor.close()

    def get_employees(self):
        """Metodo para obtener la información de los empleados"""
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM employees")
            employees = cursor.fetchall()
            cursor.close()
            return employees
