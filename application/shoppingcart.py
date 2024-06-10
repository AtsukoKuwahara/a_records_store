from .model import Order, Product

def shoppingcart(user_id):
    """
    Retrieves the shopping cart details for a given user.

    :param user_id: The ID of the user whose shopping cart is being retrieved.
    :return: A list of dictionaries containing the order and product details.
    """
    orders = Order.objects(user_id=user_id)
    results = []
    for order in orders:
        product = Product.objects(product_id=order.product_id).first()
        results.append({
            'r1': order,
            'r2': product
        })
    return results
