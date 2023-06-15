from datetime import date

import numpy as np
import pandas as pd
from fastapi import FastAPI, UploadFile
from functions.values import adc_convert_for_axel, adc_convert_for_gyro
from starlette.middleware.cors import CORSMiddleware
from state import app_state

app = FastAPI(title="СРиАД")

origins = [
    "https://test.test:3000",
    "https://localhost:3000",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def setup():
    await app_state.startup()


@app.on_event("shutdown")
async def shutdown():
    await app_state.shutdown()


@app.post("/api/add_new_patient")
async def add_new_patient(
    first_name: str,
    last_name: str,
    gender: str,
    birthday: date,
    height: int = None,
    weight: int = None,
    diagnosis: str = None,
    middle_name: str = None,
):
    """
    Добавляет нового пациента в базу данных.
    """
    await app_state.patient_repo.add_new(
        first_name=first_name,
        middle_name=middle_name,
        last_name=last_name,
        gender=gender,
        birthday=birthday,
        height=height,
        weight=weight,
        diagnosis=diagnosis,
    )
    return {"message": "ok"}


@app.post("/api/delete_patient")
async def delete_patient(id: int):
    """
    Удаляет пациента из базы данных
    """
    await app_state.patient_repo.delete(id)
    return {"message": "ok"}


@app.get("/api/show_by_id")
async def show_by_id(id: int):
    """
    Получает карточку пациента по id
    """
    row = await app_state.patient_repo.show_by_id(id)

    if not row:
        return {"message": "not_exist"}

    return row


@app.get("/api/show_all")
async def show_all():
    """
    Получает все карточки пациентов
    """
    row = await app_state.patient_repo.show_all()

    if not row:
        return {"message": "not_exist"}

    return row


@app.post("/api/edit_patient")
async def edit_patient():
    return "hello"


@app.post("/api/add_new_experiment")
async def add_new_experiment(patient_id: int):
    """
    Добавляет новый эксперимент.
    """
    await app_state.experiment_repo.add_new(patient_id)
    return {"message": "ok"}


app.post("/api/delete_experiment")


async def delete_experiment(id: int):
    """
    Удаляет эксперимент из базы данных
    """
    await app_state.experiment_repo.delete(id)
    return {"message": "ok"}


@app.get("/api/show_experiments_by_id")
async def show_experiment_by_id(patient_id: int):
    """
    Получает карточку пациента по id
    """
    row = await app_state.va_repo.show_by_id(patient_id)

    if not row:
        return {"message": "not_exist"}
    return row


@app.post("/api/add_new_experiment_values/")
async def add_new_values(file: UploadFile, experiment_id: int):
    """
    Добавляет новый массив измерительных данных
    """
    data = file.file
    data = data.readlines()
    data = list(filter(lambda x: x != b"\r\n" and x != b"1\r\n", data))
    data = data[::2]
    data1 = data[1::2]
    timestamp = []
    axel = np.empty((len(data), 3))
    gyro = np.empty((len(data), 3))
    for i in range(len(data)):
        time_value = data[i].partition(b"X")
        gyro_x = time_value[2].partition(b"Y")
        gyro_y = gyro_x[2].partition(b"Z")
        gyro_z = gyro_y[2].partition(b"X")
        axel_x = gyro_z[2].partition(b"Y")
        axel_y = axel_x[2].partition(b"Z")
        axel_z = axel_y[2]
        # print(axel_z)
        timestamp.append(int(time_value[0]))
        axel[i][0] = adc_convert_for_axel(axel_x[0])
        axel[i][1] = adc_convert_for_axel(axel_y[0])
        axel[i][2] = adc_convert_for_axel(axel_z)
        gyro[i][0] = adc_convert_for_gyro(gyro_x[0])
        gyro[i][1] = adc_convert_for_gyro(gyro_y[0])
        gyro[i][2] = adc_convert_for_gyro(gyro_z[0])
    axel_js = pd.DataFrame(axel, index=timestamp, columns=["a_x", "a_y", "a_z"])
    gyro_js = pd.DataFrame(gyro, index=timestamp, columns=["g_x", "g_y", "g_z"])
    data = axel_js.join(gyro_js)
    data = data.to_json(orient="index")

    timestamp = []
    axel = np.empty((len(data1), 3))
    gyro = np.empty((len(data1), 3))
    for i in range(len(data1)):
        time_value = data1[i].partition(b"X")
        gyro_x = time_value[2].partition(b"Y")
        gyro_y = gyro_x[2].partition(b"Z")
        gyro_z = gyro_y[2].partition(b"X")
        axel_x = gyro_z[2].partition(b"Y")
        axel_y = axel_x[2].partition(b"Z")
        axel_z = axel_y[2]
        # print(axel_z)
        timestamp.append(int(time_value[0]))
        axel[i][0] = adc_convert_for_axel(axel_x[0])
        axel[i][1] = adc_convert_for_axel(axel_y[0])
        axel[i][2] = adc_convert_for_axel(axel_z)
        gyro[i][0] = adc_convert_for_gyro(gyro_x[0])
        gyro[i][1] = adc_convert_for_gyro(gyro_y[0])
        gyro[i][2] = adc_convert_for_gyro(gyro_z[0])
    axel_js = pd.DataFrame(axel, index=timestamp, columns=["a_x", "a_y", "a_z"])
    gyro_js = pd.DataFrame(gyro, index=timestamp, columns=["g_x", "g_y", "g_z"])
    data1 = axel_js.join(gyro_js)
    data1 = data1.to_json(orient="index")
    await app_state.experiment_values_repo.add_new(
        experiment_id=experiment_id, feet_r=data, feet_l=data1
    )
    return {"status": "ok"}
