#from flask import Flask
#

    # app.py
from flask import Flask, render_template, request   # Flask se web pages banane aur form data lene ke liye

app = Flask(__name__)  # Flask app create

# ---- MENU as a dictionary (tumne padha hua) ----
# key = item name, value = price (simple dictionary)
menu = {
    "Burger": 200,
    "Pizza": 500,
    "Fries": 100,
    "Drink": 80
}

# ---- Helper function: calculate bill from quantities ----
def calculate_bill(qty_dict):
    """
    qty_dict: {'Burger': 2, 'Pizza': 1, ...}
    returns: order_list (list of tuples), subtotal, discount, total_after_discount
    """
    order = []           # list rakhenge orders as (item, qty, cost)
    subtotal = 0
    for item, price in menu.items():               # loop through menu (tumne loop padha)
        qty = qty_dict.get(item, 0)                # get quantity (0 if not present)
        if qty > 0:                                # if/else concept
            cost = price * qty
            order.append((item, qty, cost))        # tuple use hua (item, qty, cost)
            subtotal += cost

    # simple discount rule using if/else:
    discount = 0
    if subtotal > 500:                              # agar subtotal 500 se zyada to 10% discount
        discount = int(subtotal * 0.10)
    total = subtotal - discount

    return order, subtotal, discount, total


# ---- Route: home page showing menu and quantity inputs ----
@app.route("/", methods=["GET"])
def index():
    # render_template uses templates/index.html and passes menu dictionary to it
    return render_template("index.html", menu=menu)


# ---- Route: handle form submit and show bill ----
@app.route("/bill", methods=["POST"])
def bill():
    # request.form se form ke inputs milte hain (Flask ka simple way)
    # hum har menu item ke liye quantity expect kar rahe hain (0 ya number)
    qty_dict = {}
    for item in menu.keys():
        # request.form.get(item) returns string; convert to int safely
        val = request.form.get(item)
        try:
            qty = int(val) if val and val.strip() != "" else 0
        except ValueError:
            qty = 0
        qty_dict[item] = qty

    order, subtotal, discount, total = calculate_bill(qty_dict)

    # pass data to bill.html to display nicely
    return render_template("bill.html",
                           order=order,
                           subtotal=subtotal,
                           discount=discount,
                           total=total)


if __name__ == "__main__":
    app.run(debug=True)