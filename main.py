from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import get_db
from models import User
from plaid_client import client
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.country_code import CountryCode
from plaid.model.products import Products
from datetime import datetime, timedelta
import uuid

app = FastAPI()

# ✅ Request model for creating a link token
class LinkTokenRequest(BaseModel):
    user_email: str = Field(..., example="test_user_12345")

# ✅ Request model for exchanging a public token
class PublicTokenRequest(BaseModel):
    public_token: str = Field(..., example="public-sandbox-12345")

# ✅ Request model for retrieving transactions
class TransactionsRequest(BaseModel):
    user_email: str = Field(..., example="user@example.com")
    plaid_access_token: str = Field(..., example="access-sandbox-12345")

# ✅ Endpoint to create a Plaid Link Token
@app.post("/create_link_token/")
def create_link_token(request: LinkTokenRequest, db: Session = Depends(get_db)):
    try:
        request_data = LinkTokenCreateRequest(
            user={"client_user_id": str(uuid.uuid4())},
            client_name="VCC Finance",
            products=[Products.TRANSACTIONS],
            country_codes=[CountryCode.US],
            language="en"
        )
        response = client.link_token_create(request_data)
        return response.to_dict()
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Endpoint to exchange public token for access token
@app.post("/exchange_public_token/")
def exchange_public_token(request: PublicTokenRequest, db: Session = Depends(get_db)):
    try:
        exchange_request = ItemPublicTokenExchangeRequest(public_token=request.public_token)
        response = client.item_public_token_exchange(exchange_request)
        access_token = response["access_token"]
        
        # ✅ Store access token in DB
        user = db.query(User).filter(User.email == request.public_token).first()
        if not user:
            user = User(email=request.public_token, plaid_access_token=access_token)
            db.add(user)
        else:
            user.plaid_access_token = access_token
        
        db.commit()
        return {"message": "Token exchanged successfully!", "access_token": access_token}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Endpoint to get transactions (Fixed `start_date` and `end_date`)
@app.get("/transactions/")
def get_transactions(user_email: str, db: Session = Depends(get_db)):
    try:
        # Retrieve access token for user
        user = db.query(User).filter(User.email == user_email).first()
        if not user or not user.plaid_access_token:
            raise HTTPException(status_code=404, detail="User not found or no Plaid access token")

        # ✅ Fix `start_date` and `end_date` type
        request_data = TransactionsGetRequest(
            access_token=user.plaid_access_token,
            start_date=(datetime.utcnow() - timedelta(days=30)).date(),  # ✅ Explicitly convert to `date`
            end_date=datetime.utcnow().date(),  # ✅ Explicitly convert to `date`
        )

        response = client.transactions_get(request_data)
        return response.to_dict()
    except Exception as e:
        print(f"Error: {e}")  # Debugging print
        raise HTTPException(status_code=500, detail=str(e))
