from datetime import datetime, timezone
from typing import Any, Dict

from services.common.compat import BaseModel, FastAPI, Field, HTTPException

from contracts.validator import validate_message
from services.common.queue import InMemoryQueue
from services.upload.utils import is_supported_content_type

app = FastAPI(title="upload-service")
message_bus = InMemoryQueue()


class UploadRequest(BaseModel):
    filename: str = Field(..., description="Original filename")
    content_type: str = Field(..., description="MIME type of the upload")
    account_id: str = Field(..., description="Tenant/account identifier")
    object_path: str = Field(..., description="Path where object is stored")


class UploadResponse(BaseModel):
    upload_id: str
    status: str


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/uploads", response_model=UploadResponse, status_code=202)
def create_upload(request: UploadRequest) -> UploadResponse:
    if not is_supported_content_type(request.content_type):
        raise HTTPException(status_code=400, detail="Unsupported content type")

    upload_id = f"upl_{int(datetime.now(tz=timezone.utc).timestamp())}"
    message: Dict[str, Any] = {
        "upload_id": upload_id,
        "filename": request.filename,
        "content_type": request.content_type,
        "account_id": request.account_id,
        "object_path": request.object_path,
        "received_at": datetime.now(tz=timezone.utc).isoformat(),
    }
    validate_message("upload.received", message)
    message_bus.publish(message)
    return UploadResponse(upload_id=upload_id, status="accepted")


@app.get("/queue/size")
def queue_size() -> Dict[str, int]:
    return {"items": len(message_bus)}
