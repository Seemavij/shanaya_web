from django.shortcuts import (
    render,
    redirect,
    reverse,
    HttpResponse,
    get_object_or_404,
)
from django.contrib import messages
from products.models import Product


def view_bag(request):
    """A view to render the bag contents page"""

    return render(request, "bag/bag.html")


def add_to_bag(request, item_id):
    """Add  item to bag"""

    # item = get_object_or_404(product, pk=item_id)
    item = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get("quantity"))

    redirect_url = request.POST.get("redirect_url")
    bag = request.session.get("bag", {})
    if item_id in list(bag.keys()):
        messages.error(request, f"The requested quantity is not available")
    else:
        bag[item_id] = quantity
        messages.success(request, f"Added {item.name} to your bag")

    request.session["bag"] = bag
    return redirect(redirect_url)


def remove_from_bag(request, item_id):
    """Remove item from bag"""

    item = get_object_or_404(Product, pk=item_id)
    # Corrected model reference to Product
    bag = request.session.get("bag", {})

    if bag_item_id in bag:
        bag.pop(item_id)
        messages.success(request, f"{item.name} has been successfully removed")
    else:
        messages.error(request, "Item was not found in the bag.")

    request.session["bag"] = bag
    return redirect(reverse("view_bag"))


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get("quantity"))
    size = None
    if "product_size" in request.POST:
        size = request.POST["product_size"]
    bag = request.session.get("bag", {})

    if size:
        if quantity > 0:
            bag[item_id]["items_by_size"][size] = quantity
            messages.success(
                request,
                f'Updated size {size.upper()} {product.name} quantity'
                f' to {bag[item_id]["items_by_size"][size]}',
            )
        else:
            del bag[item_id]["items_by_size"][size]
            if not bag[item_id]["items_by_size"]:
                bag.pop(item_id)
            messages.success(
                request,
                f"Removed size {size.upper()} {product.name} from your bag",
            )
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(
                request, f"Updated {product.name} quantity to {bag[item_id]}"
            )
        else:
            bag.pop(item_id)
            messages.success(request, f"Removed {product.name} from your bag")

    request.session["bag"] = bag
    return redirect(reverse("view_bag"))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if "product_size" in request.POST:
            size = request.POST["product_size"]
        bag = request.session.get("bag", {})

        if size:
            del bag[item_id]["items_by_size"][size]
            if not bag[item_id]["items_by_size"]:
                bag.pop(item_id)
            messages.success(
                request,
                f"Removed size {size.upper()} {product.name} from your bag",
            )
        else:
            bag.pop(item_id)
            messages.success(request, f"Removed {product.name} from your bag")

        request.session["bag"] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f"Error removing item: {e}")
        return HttpResponse(status=500)
