from fastapi import APIRouter

from app.api.v1.endpoints import auth, tasks, opportunities, tutors

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(opportunities.router, prefix="/opportunities", tags=["opportunities"])
api_router.include_router(tutors.router, prefix="/tutors", tags=["tutors"])
