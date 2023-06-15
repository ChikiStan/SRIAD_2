from asyncpg import Pool, create_pool
from repository.experiment_values import ExperimentValuesRepository
from repository.experiments import ExperimentRepository
from repository.patients import PatientRepository


class AppState:
    def __init__(self) -> None:
        self._db = None
        self._patient_repo = None
        self._experiment_repo = None
        self._experiment_values_repo = None

    async def startup(self) -> None:
        self._db = await create_pool(
            host="localhost", user="postgres", database="test", password="admin11"
        )
        self._patient_repo = PatientRepository(db=self.db)
        self._experiment_repo = ExperimentRepository(db=self.db)
        self._experiment_values_repo = ExperimentValuesRepository(db=self.db)

    async def shutdown(self) -> None:
        if self._db:
            await self._db.close()

    @property
    def db(self) -> Pool:
        assert self._db
        return self._db

    @property
    def patient_repo(self) -> PatientRepository:
        assert self._patient_repo
        return self._patient_repo

    @property
    def experiment_repo(self) -> ExperimentRepository:
        assert self._experiment_repo
        return self._experiment_repo

    @property
    def experiment_values_repo(self) -> ExperimentValuesRepository:
        assert self._experiment_values_repo
        return self._experiment_values_repo


app_state = AppState()
