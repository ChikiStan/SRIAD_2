from datetime import date

from asyncpg import Pool
from pydantic import BaseModel


class Patient(BaseModel):
    first_name: str
    middle_name: str | None
    last_name: str
    gender: str
    birthday: date
    height: int | None
    weight: int | None
    diagnosis: int | None


class PatientRepository:
    def __init__(self, db: Pool):
        self._db = db

    async def add_new(
        self,
        first_name: str,
        middle_name: str | None,
        last_name: str,
        gender: str,
        birthday: date,
        height: int | None,
        weight: int | None,
        diagnosis: int | None,
    ) -> None:
        sql = """
            insert into "patients" (
            first_name,
            middle_name,
            last_name,
            gender,
            birthday,
            height,
            weight,
            diagnosis)
            values ($1, $2, $3, $4, $5, $6, $7, $8)"""
        async with self._db.acquire() as c:
            await c.execute(
                sql,
                first_name,
                middle_name,
                last_name,
                gender,
                birthday,
                height,
                weight,
                diagnosis,
            )

    async def delete(self, id: int) -> None:
        sql = """
            delete from "patients"
            where id = $1
            """
        async with self._db.acquire() as c:
            await c.execute(sql, id)

    async def show_by_id(self, id: str) -> Patient | None:
        sql = """
            select *
            from "patients"
            where "id" = $1
        """
        async with self._db.acquire() as c:
            row = await c.fetchrow(sql, id)

        if not row:
            return

        return Patient.parse_obj(row)

    async def show_all(self):
        sql = """
            select *
            from "patients"
        """
        async with self._db.acquire() as c:
            row = await c.fetch(sql)

        if not row:
            return

        return row
