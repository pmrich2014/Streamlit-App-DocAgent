from fastapi import Header, HTTPException, Depends
from starlette.status import HTTP_403_FORBIDDEN
import os

# Read API key from environment variable
API_KEY_APP = API_KEY_APP 
API_KEY_NAME = "X-API-Key"  # Custom header name

def verify_api_key(x_api_key: str = Header(..., alias=API_KEY_NAME)):
    if x_api_key != API_KEY_APP:        
        raise HTTPException(            
            status_code=HTTP_403_FORBIDDEN, detail="Invalid or missing API Key"
        )
