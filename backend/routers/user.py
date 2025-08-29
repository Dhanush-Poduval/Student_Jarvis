from fastapi import FastAPI,APIRouter

app=FastAPI()

router=APIRouter(
    tags=['User']
)

@router.get('/test')
def test():
    return{'works successfully'}