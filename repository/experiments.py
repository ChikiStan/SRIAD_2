from datetime import datetime

from asyncpg import Pool
from pydantic import BaseModel


class Experiment(BaseModel):
    id: int
    patient_id: int
    created_timestamp: datetime


class ExperimentRepository:
    def __init__(self, db: Pool):
        self._db = db

    async def add_new(self, patient_id: int) -> None:
        sql = """
            insert into "experiments" (
            "patient_id")
            values ($1)"""
        async with self._db.acquire() as c:
            await c.execute(sql, patient_id)

    async def delete(self, id: int) -> None:
        sql = """
            delete from "experiments"
            where id = $1
            """
        async with self._db.acquire() as c:
            await c.execute(sql, id)

    async def show_by_id(self, id: str):
        sql = """
            select *
            from "experiments"
            where "patient_id" = $1
        """
        async with self._db.acquire() as c:
            row = await c.fetch(sql, id)

        if not row:
            return
        return row

    async def show_all(self):
        sql = """
            select *
            from "experiments"
        """
        async with self._db.acquire() as c:
            row = await c.fetch(sql)

        if not row:
            return

        return row
