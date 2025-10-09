from fastapi import FastAPI, Depends, APIRouter, HTTPException, status
from my_service.dependencies import get_token
from my_service.utils.logger import setup_logger
from aiohttp import ClientSession
from my_service.config.config import settings
from my_service.models.models import (
    ApplicationStatus,
    ApplicationResponse,
    ProjectStatus,
    ProjectResponse,
)

router = APIRouter(
    prefix="/argocd",
    tags=["argocd"],
)


logger = setup_logger()
app = FastAPI()


@router.get("/application_status")
async def application_status(token: str = Depends(get_token)):
    """Fetches all ArgoCD applications statuses

    Args:
        token (str, optional): _description_. Defaults to Depends(get_token).

    Returns:
        applications: ApplicationResponse model
    """
    logger.debug("application_status hit")
    ##############################################################################
    # Please complete the fastapi route to get applications metadata from argocd #
    # Make sure to use argocd token for authentication                           #
    ##############################################################################
    try:
        async with ClientSession() as session:
            async with session.get(
                f"https://{settings.ARGOCD_URL}/api/v1/applications",
                headers={"Authorization": f"Bearer {token}"},
                verify_ssl=False,
            ) as response:
                if response.status != 200:
                    logger.error(
                        f"Error fetching applications metadata: {response.status}"
                    )
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"Error fetching applications metadata: {response.status}",
                    )

                data = await response.json()
                applications_data = []
                for application in data.get("items", []):
                    logger.debug(f"Application: {application}")

                    applications_data.append(
                        ApplicationStatus(
                            application_name=application["metadata"]["name"],
                            status=application["status"]["sync"]["status"],
                        )
                    )

                applications = ApplicationResponse(applications=applications_data)
                return applications
    except Exception as e:
        logger.error(f"Error fetching applications metadata: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching applications metadata: {e}",
        )


@router.get("/list_projects")
async def list_projects(token: str = Depends(get_token)):
    """Fetches all argocd projects names and namespaces to which they are configured

    Args:
        token (str, optional): _description_. Defaults to Depends(get_token).
    Returns:
        projects_data_conscise: concise argocd projects metadata json strucure
    """
    logger.debug("list_projects hit")

    ##########################################################################
    # Please complete the fastapi route to get projects metadata from argocd #
    # Make sure to use argocd token for authentication                       #
    ##########################################################################

    try:
        async with ClientSession() as session:
            async with session.get(
                f"https://{settings.ARGOCD_URL}/api/v1/projects",
                headers={"Authorization": f"Bearer {token}"},
                verify_ssl=False,
            ) as response:
                if response.status != 200:
                    logger.error(f"Error fetching projects metadata: {response.status}")
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"Error fetching projects metadata: {response.status}",
                    )

                data = await response.json()
                projects_data = []
                for project in data.get("items", []):
                    projects_data.append(
                        ProjectStatus(
                            project_name=project["metadata"]["name"],
                            namespace=project["metadata"]["namespace"],
                        )
                    )
                projects = ProjectResponse(projects=projects_data)
                return projects
    except Exception as e:
        logger.error(f"Error fetching projects metadata: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching projects metadata: {e}",
        )
