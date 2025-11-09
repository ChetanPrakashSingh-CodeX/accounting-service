from pydantic import Field
from pydantic import BaseModel as BaseModelV2
from pydantic.v1 import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

    # account_id	customer_id	account_number	account_type	balance	currency	status	created_at

class Accounts(BaseModelV2):
    account_id: int
    customer_id: str
    account_number: int
    account_type: str
    balance: Decimal
    currency: str
    status: str
    created_at: datetime

class CreateAccountRequest(BaseModel):
    customer_id: str
    account_type: str
    balance: Decimal
    currency: str
    correlation_id: str

    class Config:
        json_schema_extra = {
            "example": {
                "customer_id": "1",
                "account_type": "SALARY",
                "balance": 5000.00,
                "currency": "INR",
                "correlation_id": "corr-12345-1101"
            }
        }

class AccountResponse(BaseModel):
    account_number: int
    account_type: str
    status: str
    currency: str
    balance: Decimal
    correlation_id: Optional[str]  = None
    message: Optional[str] = None


class AccountOpsRequest(BaseModel):
    #account_number: int
    status: Optional[str]
    balance: Optional[Decimal]
    correlation_id: str
    
    class Config:
        json_schema_extra = {
            "example": {
                # "account_number": 45123456789015,
                "status": "ACTIVE",
                "balance": 6000.00,
                "correlation_id": "corr-12345-1101"
            }
        }

class AccountOpsResponse(BaseModel):
    account_number: Optional[int]
    status: Optional[str]
    balance: Optional[Decimal]
    correlation_id: Optional[str]
    message: Optional[str] = None

    class Config:
        from_attributes = True

class FetchBalanceResponse(BaseModel):
    account_number: int
    account_type: str
    balance: Decimal

    class Config:
        from_attributes = True

class ChangeStatusResponse(BaseModel):
    account_number: int
    account_type: str
    status: str

    class Config:
        from_attributes = True

class AppLog(BaseModel):
    notification_id: str
    customer_id: str
    customer_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    notification_type: str
    channel: str
    subject: Optional[str] = None
    message: str
    status: str
    transaction_id: Optional[str] = None
    account_id: Optional[str] = None
    amount: Optional[Decimal] = None
    correlation_id: Optional[str] = None
    error_message: Optional[str] = None
    sent_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True

class HealthResponse(BaseModel):
    status: str
    service: str
    timestamp: str