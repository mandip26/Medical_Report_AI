from typing import Optional, List
from pydantic import BaseModel

class PatientInfo(BaseModel):
    name: Optional[str]
    age: Optional[str]
    gender: Optional[str]
    referred_by: Optional[str]
    date: Optional[str]

class ReportItem(BaseModel):
    title: str
    result: str
    unit: Optional[str] = ""
    reference: Optional[str] = ""

class ExtractionResult(BaseModel):
    patient_info: PatientInfo
    report_items: List[ReportItem]

class UserData(BaseModel):
    user_id: str
    