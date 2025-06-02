from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

# 점수 변환용 딕셔너리
grade_to_point = {
    "A+": 4.5, "A": 4.0,
    "B+": 3.5, "B": 3.0,
    "C+": 2.5, "C": 2.0,
    "D+": 1.5, "D": 1.0,
    "F": 0.0
}

# Pydantic 모델 정의
class Course(BaseModel):
    course_code: str
    course_name: str
    credits: int
    grade: str = Field(..., regex="^(A\+?|B\+?|C\+?|D\+?|F)$")

class StudentRequest(BaseModel):
    student_id: str
    name: str
    courses: List[Course]

class StudentSummary(BaseModel):
    student_id: str
    name: str
    gpa: float
    total_credits: int

class StudentResponse(BaseModel):
    student_summary: StudentSummary


@app.post("/score", response_model=StudentResponse)
def calculate_gpa(data: StudentRequest):
    total_points = 0.0
    total_credits = 0

    for course in data.courses:
        if course.grade not in grade_to_point:
            raise HTTPException(status_code=400, detail=f"Invalid grade: {course.grade}")
        point = grade_to_point[course.grade]
        total_points += point * course.credits
        total_credits += course.credits

    if total_credits == 0:
        gpa = 0.0
    else:
        gpa = round(total_points / total_credits + 1e-8, 2)  # 소수점 셋째 자리 반올림

    return {
        "student_summary": {
            "student_id": data.student_id,
            "name": data.name,
            "gpa": round(gpa, 2),
            "total_credits": total_credits
        }
    }
