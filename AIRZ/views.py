from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect

posts = [
    {
        "user_id": 1,
        "name": "Alice",
        "orders": [
            {"order_id": 101, "product": "Laptop", "price": 75000, "status": "Delivered"},
            {"order_id": 102, "product": "Mouse", "price": 1200, "status": "Shipped"}
        ]
    },
    {
        "user_id": 2,
        "name": "Bob",
        "orders": [
            {"order_id": 103, "product": "Keyboard", "price": 2500, "status": "Processing"},
            {"order_id": 104, "product": "Monitor", "price": 12000, "status": "Delivered"}
        ]
    }
]

def home(request):
    html = "<div>"
    for post in posts:
        html += f'''
        <h1>{post["user_id"]} - {post["name"]}</h1>
        <ul>
        '''
        for order in post["orders"]:
            html += f'''
                <li>Order ID: {order["order_id"]}, Product: {order["product"]}, Price: {order["price"]}, Status: {order["status"]}</li>
            '''
        html += '</ul>'
    html += '</div>'

    return HttpResponse(html)
def airz_view(request, id):
    user_data = next((post for post in posts if post["user_id"] == id), None)

    if not user_data:
        return HttpResponse("<h1>User not found</h1>", status=404)

    html = f"<h1>{user_data['user_id']} - {user_data['name']}</h1><ul>"

    for order in user_data["orders"]:
        html += f'''<li>Order ID: {order["order_id"]}, Product: {order["product"]}, Price: {order["price"]}, Status: {order["status"]}</li>'''

    html += "</ul>"

    return HttpResponse(html)

