from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
from matcher import TrialMatcher
from eligibility import EligibilityCriteria

app = FastAPI(title="Clinical Trial Matcher API")

class PatientProfile(BaseModel):
    age: int
    gender: str
    conditions: List[str]
    symptoms: List[str]
    location: str
    previous_treatments: Optional[List[str]] = []

class TrialMatch(BaseModel):
    nct_id: str
    title: str
    similarity_score: float
    match_reasons: List[str]
    eligibility_status: str

matcher = TrialMatcher()
eligibility_checker = EligibilityCriteria()

import os

@app.on_event("startup")
def startup_event():
    base_dir = os.path.dirname(__file__)
    csv_path = os.path.join(base_dir, "data", "clinical_trials.csv")
    df = pd.read_csv(csv_path)
    matcher.load_trials(df)


@app.post("/match-trials", response_model=List[TrialMatch])
def match_trials(patient: PatientProfile):
    try:
        matches = matcher.match_patient(patient.dict())
        results = []
        for match in matches:
            trial = match['trial']
            eligibility_status = "Eligible" if eligibility_checker.check_eligibility(
                patient.dict(), trial.get('eligibility', '')
            ) else "Needs Review"
            result = TrialMatch(
                nct_id=trial['nct_id'],
                title=trial['title'],
                similarity_score=match['similarity_score'],
                match_reasons=match['match_reasons'],
                eligibility_status=eligibility_status
            )
            results.append(result)
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy"}
