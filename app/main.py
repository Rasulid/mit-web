from fastapi import FastAPI

from api.v1.endpoints.course.course_endpoint import router as course_router

app = FastAPI()

app.include_router(course_router)
