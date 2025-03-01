from plaid.api import plaid_api
import plaid
import os
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Retrieve Plaid credentials from .env
PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_SECRET = os.getenv("PLAID_SECRET")
PLAID_ENV = os.getenv("PLAID_ENV", "sandbox")  # Default to 'sandbox'

# ✅ Set Plaid API Environment
configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox if PLAID_ENV == "sandbox" else
         plaid.Environment.Development if PLAID_ENV == "development" else
         plaid.Environment.Production
)

# ✅ Set API Credentials
configuration.api_key['clientId'] = PLAID_CLIENT_ID
configuration.api_key['secret'] = PLAID_SECRET

# ✅ Initialize the Plaid API Client
api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)  # ✅ Correct way to initialize the API

