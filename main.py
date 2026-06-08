from fastapi import FastAPI
from backend.database import engine, SessionLocal
from backend.models import Base, Request
from backend.schemas import ResourceRequest
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uuid
import time

app = FastAPI()

# Static Files
app.mount(
    "/static",
    StaticFiles(directory="frontend"),
    name="static"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create Tables
Base.metadata.create_all(bind=engine)

# Home
@app.get("/")
def home():
    return {
        "status": "UP",
        "project": "Platform Engineering Portal"
    }

# Create Resource
@app.post("/create-resource")
def create_resource(payload: ResourceRequest):

    db = SessionLocal()

    request = Request(
    request_id=str(uuid.uuid4())[:8],
    resource_type=payload.resource_type,
    resource_name=payload.resource_name,
    environment=payload.environment,
    status="PENDING",
    iac_tool=payload.iac_tool
)

    db.add(request)
    db.commit()
    db.refresh(request)

    return {
        "message": "Request Created",
        "request_id": request.request_id,
        "resource_type": request.resource_type,
        "resource_name": request.resource_name,
        "environment": request.environment,
        "status": request.status,
        "iac_tool": request.iac_tool
    }




# Get All Requests
@app.post("/run/{request_id}")
def run_request(request_id: str):

    import requests

    db = SessionLocal()

    request = (
        db.query(Request)
        .filter(Request.request_id == request_id)
        .first()
    )

    if not request:
        return {
            "message": "Request Not Found"
        }

    request.status = "RUNNING"
    db.commit()

    try:

        if request.iac_tool == "Terraform":

            response = requests.post(
                "http://13.250.127.166:5000/create-s3",
                json={
                    "bucket_name": request.resource_name
                }
            )

            if response.status_code == 200:

                request.status = "SUCCESS"
                db.commit()

                return {
                    "message": "Terraform Provisioning Complete",
                    "resource": request.resource_name,
                    "status": request.status
                }

            else:

                request.status = "FAILED"
                db.commit()

                return {
                    "message": "Terraform Failed",
                    "response": response.text
                }

        else:

            request.status = "FAILED"
            db.commit()

            return {
                "message": "Only Terraform S3 supported currently"
            }

    except Exception as e:

        request.status = "FAILED"
        db.commit()

        return {
            "message": str(e)
        }

# My Requests Page
@app.get("/my-requests-page")
def my_requests_page():
    return FileResponse(
        "frontend/my-requests.html"
    )

# Create Resource Page
@app.get("/create-resource-page")
def create_page():
    return FileResponse(
        "frontend/create-resource.html"
    )

# Approvals Page
@app.get("/approvals-page")
def approvals_page():
    return FileResponse(
        "frontend/approvals.html"
    )

# Workflow Page
@app.get("/workflow-page")
def workflow_page():
    return FileResponse(
        "frontend/workflows.html"
    )

# Approve Request
@app.post("/approve/{request_id}")
def approve_request(request_id: str):

    db = SessionLocal()

    request = (
        db.query(Request)
        .filter(Request.request_id == request_id)
        .first()
    )

    if not request:
        return {
            "message": "Request Not Found"
        }

    if request.environment == "DEV":
        request.status = "APPROVED"

    elif request.environment == "QA":
        request.status = "TEAM_LEAD_APPROVED"

    elif request.environment == "UAT":
        request.status = "MANAGER_APPROVED"

    elif request.environment == "PROD":
        request.status = "SECURITY_APPROVAL"

    db.commit()

    return {
        "request_id": request.request_id,
        "environment": request.environment,
        "status": request.status
    }

# Run Workflow (GitHub Actions Simulation)
@app.post("/run/{request_id}")
def run_request(request_id: str):

    db = SessionLocal()

    request = (
        db.query(Request)
        .filter(Request.request_id == request_id)
        .first()
    )

    if not request:
        return {
            "message": "Request Not Found"
        }

    request.status = "RUNNING"
    db.commit()

    print("================================")
    print("GitHub Actions Pipeline Started")
    print("================================")

    print("Checkout Repository")
    print("Validate Templates")

    if request.iac_tool == "Terraform":

        print("terraform init")
        print("terraform plan")
        print("terraform apply -auto-approve")

    elif request.iac_tool == "CloudFormation":

        print("aws cloudformation create-stack")

    else:

        print("boto3 automation started")

    print("Deployment Successful")

    time.sleep(3)

    request.status = "SUCCESS"

    db.commit()

    return {
        "message": "Provisioning Complete",
        "request_id": request.request_id,
        "status": request.status,
        "iac_tool": request.iac_tool
    }

# Complete Workflow
@app.post("/complete/{request_id}")
def complete_request(request_id: str):

    db = SessionLocal()

    request = (
        db.query(Request)
        .filter(Request.request_id == request_id)
        .first()
    )

    if not request:
        return {
            "message": "Request Not Found"
        }

    request.status = "SUCCESS"

    db.commit()

    return {
        "message": "Provisioning Complete"
    }

@app.get("/dashboard")
def dashboard():
    return FileResponse(
        "frontend/index.html"
    )


@app.post("/api-gateway")
def api_gateway(payload: ResourceRequest):

    return {
        "message": "Request received by API Gateway",
        "resource": payload.resource_type
    }

@app.get("/logs-page")
def logs_page():
    return FileResponse(
        "frontend/logs.html"
    )


@app.get("/monitoring-page")
def monitoring_page():

    return FileResponse(
        "frontend/monitoring.html"
    )

@app.get("/inventory-page")
def inventory_page():

    return FileResponse(
        "frontend/inventory.html"
    )

@app.get("/pipeline-page")
def pipeline_page():

    return FileResponse(
        "frontend/pipeline.html"
    )

@app.get("/templates-page")
def templates_page():

    return FileResponse(
        "frontend/templates.html"
    )