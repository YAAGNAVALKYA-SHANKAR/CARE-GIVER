from pydantic import BaseModel, Field
from enum import Enum

class EscalationStatus(str, Enum):
    """
    Enum for escalation status.
    """
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class EscalationPriority(str, Enum):
    """
    Enum for escalation priority.
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class EscalationModel(BaseModel):
    """
    Model for escalation data.
    """

    patient_id: str = Field(..., description="Name of the escalated patient")
    caregiver_id: str = Field(..., description="Name of the caregiver")
    visit_id: str = Field(..., description="ID of the visit")
    vitals_id: str = Field(..., description="ID of the vitals")
    escalation_reason:str = Field(..., description="Reason for the escalation")
    escalation_description: str = Field(..., description="Description of the escalation")
    # escalation_status:EscalationStatus = Field(default="pending", description="Status of the escalation")
    # escalation_created_at: str = Field(..., description="Creation timestamp of the escalation")
    # escalation_updated_at: str = Field(..., description="Last update timestamp of the escalation")
    # escalation_priority:EscalationPriority = Field(default="low", description="Priority level of the escalation")