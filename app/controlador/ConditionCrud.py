from connection import connect_to_mongodb
from bson import ObjectId
from fhir.resources.condition import Condition
import json

# Conectar a la colección de condiciones en MongoDB
collection = connect_to_mongodb("SamplePatientService", "conditions")

def WriteCondition(condition_dict: dict):
    try:
        # Validar la estructura de la condición con el modelo FHIR
        cond = Condition.model_validate(condition_dict)
    except Exception as e:
        return f"errorValidating: {str(e)}", None

    # Convertir el modelo validado a JSON
    validated_condition_json = cond.model_dump()

    # Insertar la condición en la base de datos
    result = collection.insert_one(validated_condition_json)

    if result:
        inserted_id = str(result.inserted_id)
        return "success", inserted_id
    else:
        return "errorInserting", None
