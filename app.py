from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Query
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates

from wisest.price import query_price

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/query_price")
async def query_price_endpoint(
    source_amount: float = Query(None, gt=0),
    source_currency: str = Query(...),
    target_amount: float = Query(..., gt=0),
    target_currency: str = Query(...),
    pay_in_method: str = Query("GOOGLE_PAY"),
    pay_out_method: str = Query("BALANCE"),
    price_set_id: int = Query(None),
):
    try:
        price = query_price(
            source_amount=source_amount if source_amount is not None else None,
            source_currency=source_currency,
            target_amount=target_amount,
            target_currency=target_currency,
            pay_in_method=pay_in_method,
            pay_out_method=pay_out_method,
            price_set_id=price_set_id if price_set_id is not None else None,
        )
        return JSONResponse(content=price.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from None


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
