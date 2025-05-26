from fastapi import FastAPI, HTTPException, Request
import uvicorn
from app.controlador.PatientCrud import GetPatientById,WritePatient,GetPatientByIdentifier
from app.controlador.ConditionCrud import WriteCondition
from app.controlador.ConditionCrud import GetConditionsByPatient
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://hl7-patient-write-gabriela-787.onrender.com","https://condition-write-gabriela-787.onrender.com","https://busqueda-h5jv.onrender.com"],  # Permitir solo este dominio
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

@app.get("/patient", response_model=dict)
async def get_patient_by_identifier(system: str,value: str):
    print("Solicitud datos:",system,value)
    status,patient = GetPatientByIdentifier(system,value)
    if status=='success':
        return patient  # Return patient
    elif status=='notFound':
        raise HTTPException(status_code=204, detail="Patient not found")
    else:
        raise HTTPException(status_code=500, detail=f"Internal error. {status}")

@app.get("/patient/{patient_id}", response_model=dict)
async def get_patient_by_id(patient_id: str):
    status,patient = GetPatientById(patient_id)
    if status=='success':
        return patient  # Return patient
    elif status=='notFound':
        raise HTTPException(status_code=404, detail="Patient not found")
    else:
        raise HTTPException(status_code=500, detail=f"Internal error. {status}")


@app.post("/patient", response_model=dict)
async def add_patient(request: Request):
    new_patient_dict = dict(await request.json())
    status,patient_id = WritePatient(new_patient_dict)
    if status=='success':
        return {"_id":patient_id}  # Return patient id
    else:
        raise HTTPException(status_code=500, detail=f"Validating error: {status}")
        
from fastapi import HTTPException, Request

@app.get("/condition", response_model=dict)
async def get_conditions_by_patient(patient: str = None):
    if not patient:
        raise HTTPException(status_code=400, detail="Missing patient parameter")
    
    status, conditions = GetConditionsByPatient(patient)
    
    if status == 'success':
        return {
            "resourceType": "Bundle",
            "type": "searchset",
            "entry": [{"resource": cond} for cond in conditions]
        }
    elif status == 'notFound':
        return {
            "resourceType": "Bundle",
            "type": "searchset",
            "entry": []
        }
    else:
        raise HTTPException(status_code=500, detail=f"Internal error. {status}")

@app.post("/condition", response_model=dict)
async def add_condition(request: Request):
    try:
        print("Recibiendo solicitud POST en /condition")  # Verifica que la solicitud llega

        new_condition_dict = dict(await request.json())
        print(f" Datos recibidos: {new_condition_dict}")  # Imprime los datos enviados desde Postman

        status, condition_id = WriteCondition(new_condition_dict)
        print(f"Resultado de WriteCondition: {status}, ID: {condition_id}")  # Muestra si se guardó bien o no

        if status == 'success':
            print(f"Condición guardada con ID {condition_id}")
            return {"_id": condition_id}  # Retorna el ID de la condición creada
        else:
            print(f" Error insertando en la BD: {status}")
            raise HTTPException(status_code=500, detail=f"Validating error: {status}")

    except Exception as e:
        print(f" ERROR en POST /condition: {str(e)}")  # Si algo falla, muestra el error exacto
        raise HTTPException(status_code=500, detail=f"Error desconocido: {str(e)}")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
