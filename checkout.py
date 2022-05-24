from fastapi import FastAPI, Response, status

app = FastAPI()

cart = {}

def check_user(username):
    if username not in cart:
            cart[username] = []

@app.get("/checkout/cart")
async def get_cart(username: str):
    check_user(username)

    grandTotal = 0
    items = []

    for item in cart[username]:
        totalPrice = 0
        grandTotal += item["product"]["price"] * item["amount"]
        totalPrice += item["product"]["price"] * item["amount"]
        
        items.append({
            "product": item,
            "amount": item["amount"],
            "totalPrice": totalPrice
        })


    return {"username": username, "grandTotal": grandTotal, "items": items}

@app.put("/checkout/cart")
async def put_cart(product_id: int, is_add: bool, response: Response, username: str):
    check_user(username)

    for item in cart[username]:
        if item["product"]["id"] == product_id:
            item["amount"] = item["amount"] + 1 if is_add else item["amount"] - 1
            return

    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {"error": "Internal Server Error", "error_message": "Product ID not found"}

@app.delete("/checkout/cart")
async def delete_cart(product_id: int, username: str):
    cart[username] = [item for item in cart[username] if not (item["product"]["id"] == product_id)]
    return

@app.post("/checkout/cart")
async def add_cart(id: int, name: str, description: str, price: int, stock: int, image: str, video: str, created_at: str, updated_at: str, username: str):
    check_user(username)

    for item in cart[username]:
        if item["product"]["id"] == id:
            await put_cart(id, True, Response, username)
            return await get_cart(username)

    productTemp = {
        "id": id,
        "name": name,
        "description": description,
        "price": price,
        "stock": stock,
        "image": image,
        "video": video,
        "created_at": created_at,
        "updated_at": updated_at
    }
    cart[username].append(
        {
            "product": productTemp,
            "amount": 1
        }
    )

    return await get_cart(username)

@app.post("/checkout")
async def checkout_items(username: str):
    for item in cart[username]:
        # Hit endpoint kurangin stok
        cart[username] = []
    return