from connection import connect_to_mongodb
from bson import ObjectId
from fhir.resources.condition import Condition
import json

# Conectar a la colección de condiciones en MongoDB
collection = connect_to_mongodb("SamplePatientService", "conditions")

def WriteCondition(condition_dict: dict):
    try:
        # Validar con el modelo FHIR
        cond = Condition.model_validate(condition_dict)
    except Exception as e:
        print(f"❌ Error validando el artefacto condition: {e}")
        return f"errorValidating: {str(e)}", None

    # Convertir el modelo validado a JSON
    validated_condition_json = cond.model_dump()
    
    # 🛠️ DEPURACIÓN: Imprimir lo que se está intentando guardar
    print("📝 Intentando guardar la condición en MongoDB:", json.dumps(validated_condition_json, indent=2))

    # Insertar en MongoDB
    result = collection.insert_one(validated_condition_json)

    if result.inserted_id:
        print(f"✅ Condición guardada con ID: {result.inserted_id}")
        return "success", str(result.inserted_id)
    else:
        print("❌ Error al insertar en MongoDB")
        return "errorInserting", None
        
def GetConditionsByPatientReference(patient_reference):
    try:
        conditions = list(collection.find({"subject.reference": patient_reference}))
        for cond in conditions:
            cond["_id"] = str(cond["_id"])
        if conditions:
            return "success", conditions
        else:
            return "notFound", []
    except Exception as e:
        print(f"Error buscando condiciones: {e}")  # <-- Aquí imprime el error real
        return f"error: {str(e)}", []


