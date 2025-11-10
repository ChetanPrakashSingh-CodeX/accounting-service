import json
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import logging, models, schemas
from datetime import datetime
from database import engine, Base, get_db
from models import Accounts
from schemas import (
    Accounts,
    CreateAccountRequest,
    AccountResponse,
    AccountOpsRequest,
    AccountOpsResponse,
    FetchBalanceResponse,
    ChangeStatusResponse,
    AppLog,
    HealthResponse
)
from services import generate_account_number, generate_account_id


logging.basicConfig(
     level=logging.INFO,
     format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s", "service": "accounting-service"}'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    logger.info("Accounting service started successfully")
    yield
    logger.info("Shutting down accounting service")

app = FastAPI(
    # title="Accounting Service",
    # description="Microservice for accounts management",
    # version="1.0.0",
    # lifespan=lifespan
)

# --- Create Tables with the calss reference in model.py file ---
#models.Base.metadata.create_all(engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- CRUD Endpoints ---


# Create a new account
@app.post("/api/v1/accounts/create", response_model=AccountResponse, status_code=201)
def create_account(request: schemas.CreateAccountRequest, db: Session = Depends(get_db)):
    
    """Generate a new account_id"""
    account_id = generate_account_id()
    print(account_id)

    """Generate a new account_number"""
    account_number = generate_account_number()
    print(account_number) # Output: Example: 45123456789015

    # account_id	customer_id	account_number	account_type	balance	currency	status	created_at

    
    new_account = models.Accounts(
        account_id=account_id,customer_id=request.customer_id,account_number=account_number,
        account_type=request.account_type,balance=request.balance,currency=request.currency,status='ACTIVE', created_at=datetime.now()
    )
    print(new_account)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return schemas.AccountResponse(
        account_number=new_account.account_number,
        account_type=new_account.account_type,
        status=new_account.status,
        currency=new_account.currency,
        balance=new_account.balance,
        correlation_id=request.correlation_id,
        message="Account created successfully"
    )

# Update account Balance
@app.put("/api/v1/accounts/{account_number}/update_balance", response_model=AccountOpsResponse, status_code=200)
def update_account_balance(account_number: int, request: schemas.AccountOpsRequest, db: Session = Depends(get_db)):
    """Update account status and balance."""
    #account_number = request.account_number

    account = db.query(models.Accounts).filter(models.Accounts.account_number == account_number).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    # updated_account = models.Accounts(
    #     account_id=account.account_id,
    #     customer_id=account.customer_id,
    #     account_number=account_number,
    #     account_type=account.account_type,
    #     balance=request.balance,
    #     currency=account.currency,
    #     status=request.status, 
    #     created_at=datetime.now()
    # )
    
    #for key, value in updated_account.model_dump(exclude_unset=True).items():
    #for key, value in updated_account.dict().items():
        #setattr(account, key, value)

    # db.commit()
    # db.refresh(account)
    return schemas.AccountOpsResponse(
        account_number=account.account_number,
        status=account.status,
        balance=request.balance,
        correlation_id=request.correlation_id,
        message="Account updated successfully"
    )

# Close an existing account
@app.post("/api/v1/accounts/{account_number}/close",response_model=AccountOpsResponse, status_code=200)
def update_account_status(account_number: int, request: schemas.AccountOpsRequest,  db: Session = Depends(get_db)):
    """Close an existing account."""
    #account_number = request.account_number
    account = db.query(models.Accounts).filter(models.Accounts.account_number == account_number).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    if request.status == 'CLOSE' and account.balance != 0:
        raise HTTPException(status_code=400, detail="Account balance must be zero to close the account")
    #account.status = 'CLOSED'

    # db.commit()
    # db.refresh(account)
    
    return schemas.AccountOpsResponse(
        account_number=account.account_number,
        status=request.status,
        correlation_id=request.correlation_id,
        message="Account updated successfully"
    )

# Update an existing account status
@app.patch("/api/v1/accounts/{account_number}/update_status",response_model=AccountOpsResponse, status_code=200)
def update_account_status(account_number: int, request: schemas.AccountOpsRequest,  db: Session = Depends(get_db)):
    """Close an existing account."""
    #account_number = request.account_number
    account = db.query(models.Accounts).filter(models.Accounts.account_number == account_number).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # if request.status == 'CLOSE' and account.balance != 0:
    #     raise HTTPException(status_code=400, detail="Account balance must be zero to close the account")
    #account.status = 'CLOSED'

    # db.commit()
    # db.refresh(account)
    
    return schemas.AccountOpsResponse(
        account_number=account.account_number,
        status=request.status,
        correlation_id=request.correlation_id,
        message="Account updated successfully"
    )


# Fetch an account by Account Number
@app.get("/api/v1/accounts/{account_number}", response_model=AccountOpsResponse, status_code=200)
def fetch_account(account_number: int,  db: Session = Depends(get_db)):
    """Fetch an account by its Number."""
    account = db.query(models.Accounts).filter(models.Accounts.account_number == account_number).first()
    if not account:
        #print(account_number)
        raise HTTPException(status_code=404, detail="Account not found")
    return schemas.AccountOpsResponse(
        account_number=account.account_number,
        status=account.status,
        balance=account.balance,
        correlation_id="corr-12345-9876",
        message="Account fetched successfully"
    )

# Fetch all accounts belonging to a customer
@app.get("/api/v1/accounts/{customer_id}", response_model=AccountOpsResponse, status_code=200)
def fetch_account(customer_id: int,  db: Session = Depends(get_db)):
    """Fetch an account by its Number."""
    accounts = db.query(models.Accounts).filter(models.Accounts.customer_id == str(customer_id)).all()
    if not accounts:
        #print(account_number)
        raise HTTPException(status_code=404, detail="Customer not found")
    return accounts
    #         schemas.AccountOpsResponse(
    #     account_number=account.account_number,
    #     status=account.status,
    #     balance=account.balance,
    #     correlation_id="corr-12345-9876",
    #     message="Accounts fetched successfully"
    # )


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8004)