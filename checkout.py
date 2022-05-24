from fastapi import FastAPI

app = FastAPI()

cart = {
    "johndoe" : [
        {
            "product" : {

            },
            "amount": 2
        },

    ]

}

@app.get("/checkout/cart")
async def getCart(username: str):
    if username not in cart {
        cart[username] = []
    }
    
    grandTotal = 0
    items = []

    for item in cart[username]:
        totalPrice = 0
        items["product"] = item
        grandTotal += item["product"]["price"] * item["amount"]
        totalPrice += item["product"]["price"] * item["amount"]
        
        items.append({
            "product": item,
            "amount": item["amount"],
            "totalPrice": totalPrice
        })


    return {"username": username, "grandTotal": grandTotal, "items": items}

@app.put("/checkout/cart")
async def putCart(username: str, product_id: str, is_add: bool):
    userCart = cart[username]
    for item in cart[username]:
        if item["product"]["id"] == product_id:
            item["amount"] += 1 if is_add else item["amount"] -= 1
            return

