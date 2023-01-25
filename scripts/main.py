import os
from fastapi import FastAPI
from datetime import datetime
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import joblib
import api_tools

END_TRAIN = datetime(2021, 12, 1)
PREDICTED_YEARS = 60

app = FastAPI()

# Handle CORS

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/{region}/{province}/{type_of_exercise}/{tourist_residence}")
def forecast(region: str, province: str, type_of_exercise: str, tourist_residence: str):

    path = f"./data/{region}/models/{province}/{type_of_exercise}/{tourist_residence}"
    with open(f"{path}/presences_model.pkl", "rb") as model:
        forecaster = joblib.load(model)
        prediction = forecaster.forecast(PREDICTED_YEARS)

    values = list(prediction.array)

    #Model may display negative values sometime
    values = [0 if x < 0 else x for x in values]
    indexes = list(prediction.index)
    assert len(values) == len(indexes)

    region_val = api_tools.get_key(region, api_tools.TUSCANY_PROV)
    province_val = api_tools.get_key(province, api_tools.TUSCANY_PROV)
    exercise_val = api_tools.get_key(type_of_exercise, api_tools.TUSCANY_EXERCISES)

    data = [{"date": indexes[i].strftime("%Y-%m"),  "npeople": values[i], "region":region_val, "province": province_val, "typeOfExercise": exercise_val} for i in range(len(values))]

    return {"prediction": data}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=os.getenv("PORT", default=5000), log_level="info")