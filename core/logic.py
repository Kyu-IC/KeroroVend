from . import db

# --- Module-level state ---
state = {
    "current_amount": 0,
    "selected_product": None,
}

coin_stock = db.get_coin_stock()

# --- Give change ---
def give_change(amount, coin_stock_param):
    change = {}
    for coin in sorted(coin_stock_param.keys(), reverse=True):
        if amount <= 0:
            break
        if coin_stock_param[coin] > 0:
            use = min(amount // coin, coin_stock_param[coin])
            if use > 0:
                change[coin] = use
                amount -= coin * use
    if amount > 0:
        return None
    return change

# --- Insert coin ---
def insert_coin(coin):
    global state, coin_stock
    if coin not in coin_stock:
        return "Invalid coin"
    state["current_amount"] += coin
    coin_stock[coin] += 1
    db.update_coin_stock(coin, coin_stock[coin])
    return f"Inserted {coin} baht. Current amount: {state['current_amount']} baht"

# --- Purchase product ---
def purchase_product(product_id):
    global state, coin_stock
    products = db.get_products()
    product_info = next((p for p in products if p[0] == product_id), None)
    if not product_info:
        return "Invalid product"

    id, name, price, stock = product_info
    if stock <= 0:
        return f"{name} is out of stock"
    if state["current_amount"] < price:
        return f"Not enough money. Price is {price} baht"

    change_needed = state["current_amount"] - price
    change = give_change(change_needed, coin_stock)
    if change is None:
        return "Cannot give exact change"

    # Update stock & coins
    db.update_product_stocks(id, stock - 1)
    for c, cnt in change.items():
        coin_stock[c] -= cnt
        db.update_coin_stock(c, coin_stock[c])

    db.log_transaction(id, state["current_amount"], change)
    state["current_amount"] = 0
    return f"Purchased {name}! Change returned: {change}"
