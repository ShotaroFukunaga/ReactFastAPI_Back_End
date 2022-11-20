from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routers import route_todo,route_auth
from schemas import SuccessMsg, CsrfSettings
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect import CsrfProtectError

app = FastAPI()
app.include_router(route_todo.router)
app.include_router(route_auth.router)
origins = ["http://localhost:3000"]
app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@CsrfProtect.load_config
def get_csrf_config():
  return CsrfSettings()

@app.exception_handler(ChildProcessError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
  return JSONResponse(
    status_code = exc.status_code,
    content={"detail": exc.message}
  )

@app.get("/",response_model=SuccessMsg)
def root():
  return {"message":"Welcome to Fast API"}

#uvicorn main:app --reload 
# "please exec cmd"
# python3 -m pip install --upgrade pip
# pip install -r requirements.txt

# "this your pip packages export to requirements.txt"
# pip freeze > requirements.txt