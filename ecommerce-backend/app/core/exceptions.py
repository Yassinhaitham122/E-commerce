from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException


#بدل ما ترفع HTTPException في كل مكان، نعمل Middleware يعيد رسائل JSON موحدة لكل الأخطاء في المشروع.

class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except StarletteHTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content={"error": exc.detail, "status_code": exc.status_code}
            )
        except RequestValidationError as exc:
            return JSONResponse(
                status_code=422,
                content={"error": "Validation error", "details": exc.errors()}
            )
        except Exception as exc:
            # أي خطأ غير متوقع
            return JSONResponse(
                status_code=500,
                content={"error": "Internal server error", "details": str(exc)}
            )
    