from fastapi import Header, HTTPException
import firebase_admin.auth as fb_auth

async def get_current_user(authorization: str = Header(...)):
    try:
        token = authorization.replace("Bearer ", "")
        decoded = fb_auth.verify_id_token(token)
        return decoded  # dict chứa uid, email, ...
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
