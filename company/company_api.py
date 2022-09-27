#  author = "Vũ Đức Cường"
#  date = 9/25/22, 5:32 PM
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_company_name():
    return {"name": "The example company"}


@router.get("/employees")
async def number_of_employees():
    return 200
