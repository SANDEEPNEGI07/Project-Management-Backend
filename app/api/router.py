from fastapi import APIRouter

from app.api.routes import auth, users, tasks, organizations, projects, user_profiles

router = APIRouter()

router.include_router(auth.router, prefix="/auth")
router.include_router(users.router, prefix="/users")
router.include_router(tasks.router, prefix="/tasks")
router.include_router(organizations.router, prefix="/organizations")
router.include_router(projects.router, prefix="/projects")
router.include_router(user_profiles.router, prefix="/user-profiles")
