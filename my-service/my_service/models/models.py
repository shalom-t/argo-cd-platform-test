from pydantic import BaseModel
from typing import Dict, List, Optional


class HealthCheckResponse(BaseModel):
    status_code: int
    message: str


class ArgoCDCreds(BaseModel):
    username: str
    password: str


class ApplicationStatus(BaseModel):
    application_name: str
    status: str


class ApplicationResponse(BaseModel):
    applications: List[ApplicationStatus]


class ProjectStatus(BaseModel):
    project_name: str
    namespace: str


class ProjectResponse(BaseModel):
    projects: List[ProjectStatus]