from fastapi import FastAPI, Query, HTTPException

app = FastAPI()

@app.get("/calculate")
def calculate(
    op: str = Query(..., description="Операція: +, -, *, /, square"),
    a: float = Query(..., description="Перший операнд"),
    b: float = Query(None, description="Другий операнд (опційний, потрібен для операцій крім square)")
):
    if op == "square":
       
        result = a ** 2
    else:
        
        if b is None:
            raise HTTPException(status_code=400, detail="Параметр 'b' потрібен для цієї операції")
        
        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        elif op == "/":
            if b == 0:
                raise HTTPException(status_code=400, detail="Ділення на нуль заборонено")
            result = a / b
        else:
            raise HTTPException(status_code=400, detail="Невідома операція")

    return {"operation": op, "a": a, "b": b, "result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
