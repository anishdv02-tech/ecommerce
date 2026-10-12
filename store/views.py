import json
import uuid
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from store.models import Category, Product, Review, Order, OrderItem


def index_view(request):
    return render(request, 'store/index.html')


def product_to_dict(product):
    return {
        "id": product.id,
        "name": product.name,
        "slug": product.slug,
        "category_id": product.category.id if product.category else None,
        "category_name": product.category.name if product.category else "",
        "category_slug": product.category.slug if product.category else "",
        "price": float(product.price),
        "old_price": float(product.old_price) if product.old_price else None,
        "description": product.description,
        "short_specs": product.short_specs or [],
        "image": product.image,
        "rating": float(product.rating),
        "review_count": product.review_count,
        "stock": product.stock,
        "badge": product.badge,
        "tags": [t.strip() for t in product.tags.split(',') if t.strip()] if product.tags else [],
        "is_featured": product.is_featured,
        "created_at": product.created_at.isoformat()
    }

def category_to_dict(category):
    return {
        "id": category.id,
        "name": category.name,
        "slug": category.slug,
        "description": category.description,
        "icon": category.icon,
        "product_count": category.products.count()
    }

def review_to_dict(review):
    return {
        "id": review.id,
        "author": review.author,
        "rating": review.rating,
        "comment": review.comment,
        "created_at": review.created_at.strftime("%Y-%m-%d %H:%M")
    }

# ---------------- API ENDPOINTS ----------------

@require_http_methods(["GET"])
def get_products(request):
    queryset = Product.objects.select_related('category').all()

    # Category filter
    category_slug = request.GET.get('category')
    if category_slug and category_slug != 'all':
        queryset = queryset.filter(category__slug=category_slug)

    # Search filter
    search_query = request.GET.get('search')
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(tags__icontains=search_query)
        )

    # Price range filter
    min_price = request.GET.get('min_price')
    if min_price:
        try:
            queryset = queryset.filter(price__gte=float(min_price))
        except ValueError:
            pass

    max_price = request.GET.get('max_price')
    if max_price:
        try:
            queryset = queryset.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # Badge filter
    badge = request.GET.get('badge')
    if badge:
        queryset = queryset.filter(badge__iexact=badge)

    # Featured filter
    featured = request.GET.get('featured')
    if featured in ['true', '1']:
        queryset = queryset.filter(is_featured=True)

    # Sorting
    sort = request.GET.get('sort', 'featured')
    if sort == 'price_asc':
        queryset = queryset.order_by('price')
    elif sort == 'price_desc':
        queryset = queryset.order_by('-price')
    elif sort == 'rating':
        queryset = queryset.order_by('-rating', '-review_count')
    elif sort == 'newest':
        queryset = queryset.order_by('-created_at')
    else: # default featured or bestsellers
        queryset = queryset.order_by('-is_featured', '-rating', 'id')

    products = [product_to_dict(p) for p in queryset]
    return JsonResponse({"status": "success", "count": len(products), "products": products})

@require_http_methods(["GET"])
def get_product_detail(request, pk):
    try:
        product = Product.objects.select_related('category').get(pk=pk)
        reviews = [review_to_dict(r) for r in product.reviews.all().order_by('-created_at')]
        data = product_to_dict(product)
        data["reviews_list"] = reviews

        # Related products in same category
        related = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
        data["related_products"] = [product_to_dict(r) for r in related]

        return JsonResponse({"status": "success", "product": data})
    except Product.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Product not found"}, status=404)

@csrf_exempt
@require_http_methods(["POST"])
def create_product(request):
    """Insert a new product into the database"""
    try:
        body = json.loads(request.body)
        name = body.get('name', '').strip()
        if not name:
            return JsonResponse({"status": "error", "message": "'name' is required"}, status=400)

        price = float(body.get('price', 0))
        description = body.get('description', '')
        category_id = body.get('category_id') or body.get('category')
        
        category = None
        if category_id:
            category = Category.objects.filter(id=category_id).first() or Category.objects.filter(slug=category_id).first()
        if not category:
            category = Category.objects.first()

        from django.utils.text import slugify
        base_slug = slugify(name)
        slug = base_slug
        counter = 1
        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        product = Product.objects.create(
            name=name,
            slug=slug,
            category=category,
            price=price,
            old_price=float(body['old_price']) if body.get('old_price') is not None else None,
            description=description,
            short_specs=body.get('short_specs', []),
            image=body.get('image', 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80'),
            stock=int(body.get('stock', 10)),
            badge=body.get('badge', None),
            tags=body.get('tags', ''),
            is_featured=bool(body.get('is_featured', False)),
            rating=float(body.get('rating', 5.0)),
            review_count=int(body.get('review_count', 0))
        )
        return JsonResponse({"status": "success", "message": "Product created successfully", "product": product_to_dict(product)}, status=201)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST", "PUT"])
def update_product(request, pk):
    """Update an existing product by ID"""
    try:
        product = Product.objects.get(pk=pk)
        body = json.loads(request.body)

        if 'name' in body:
            product.name = body['name'].strip()
        if 'price' in body:
            product.price = float(body['price'])
        if 'old_price' in body:
            product.old_price = float(body['old_price']) if body['old_price'] is not None else None
        if 'description' in body:
            product.description = body['description']
        if 'stock' in body:
            product.stock = int(body['stock'])
        if 'badge' in body:
            product.badge = body['badge']
        if 'image' in body:
            product.image = body['image']
        if 'short_specs' in body:
            product.short_specs = body['short_specs']
        if 'tags' in body:
            product.tags = body['tags']
        if 'is_featured' in body:
            product.is_featured = bool(body['is_featured'])
        if 'category_id' in body:
            cat = Category.objects.filter(id=body['category_id']).first()
            if cat:
                product.category = cat

        product.save()
        return JsonResponse({"status": "success", "message": "Product updated successfully", "product": product_to_dict(product)})
    except Product.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Product not found"}, status=404)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST", "DELETE"])
def delete_product(request, pk):
    """Delete a product by ID"""
    try:
        product = Product.objects.get(pk=pk)
        product_name = product.name
        product.delete()
        return JsonResponse({"status": "success", "message": f"Product '{product_name}' deleted successfully"})
    except Product.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Product not found"}, status=404)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)


@require_http_methods(["GET"])
def get_categories(request):
    categories = [category_to_dict(c) for c in Category.objects.all()]
    return JsonResponse({"status": "success", "categories": categories})

@csrf_exempt
@require_http_methods(["GET", "POST"])
def product_reviews(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Product.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Product not found"}, status=404)

    if request.method == "GET":
        reviews = [review_to_dict(r) for r in product.reviews.all().order_by('-created_at')]
        return JsonResponse({"status": "success", "reviews": reviews})

    elif request.method == "POST":
        try:
            body = json.loads(request.body)
            author = body.get('author', 'Anonymous')
            rating = int(body.get('rating', 5))
            comment = body.get('comment', '')

            if not comment.strip():
                return JsonResponse({"status": "error", "message": "Comment cannot be empty"}, status=400)

            review = Review.objects.create(
                product=product,
                author=author,
                rating=max(1, min(5, rating)),
                comment=comment
            )

            # Update product rating stats
            all_reviews = product.reviews.all()
            total_stars = sum(r.rating for r in all_reviews)
            product.review_count = all_reviews.count()
            product.rating = round(total_stars / product.review_count, 1)
            product.save()

            return JsonResponse({"status": "success", "review": review_to_dict(review), "new_rating": product.rating, "new_count": product.review_count})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def validate_coupon(request):
    try:
        body = json.loads(request.body)
        code = body.get('code', '').strip().upper()
        subtotal = float(body.get('subtotal', 0.0))

        coupons = {
            "LUMINA20": {"type": "percent", "value": 20, "desc": "20% Off Storewide"},
            "AURA10": {"type": "fixed", "value": 10.00, "desc": "$10 Off Your Order"},
            "FREESHIP": {"type": "shipping", "value": 0, "desc": "Free Express Shipping"},
            "WELCOME10": {"type": "percent", "value": 10, "desc": "10% Welcome Discount"},
        }

        if code in coupons:
            c = coupons[code]
            discount_amount = 0.0
            if c["type"] == "percent":
                discount_amount = round(subtotal * (c["value"] / 100.0), 2)
            elif c["type"] == "fixed":
                discount_amount = min(subtotal, c["value"])
            elif c["type"] == "shipping":
                discount_amount = 15.00 # standard shipping saved

            return JsonResponse({
                "status": "success",
                "valid": True,
                "code": code,
                "description": c["desc"],
                "discount_amount": discount_amount
            })
        else:
            return JsonResponse({
                "status": "error",
                "valid": False,
                "message": "Invalid coupon code. Try 'LUMINA20' for 20% off!"
            }, status=400)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def checkout(request):
    try:
        body = json.loads(request.body)
        customer_name = body.get('name', '').strip()
        customer_email = body.get('email', '').strip()
        shipping_address = body.get('address', '').strip()
        payment_method = body.get('payment_method', 'Credit Card')
        items_data = body.get('items', [])
        coupon_code = body.get('coupon_code', '').upper()

        if not customer_name or not customer_email or not shipping_address:
            return JsonResponse({"status": "error", "message": "Missing required customer details"}, status=400)

        if not items_data:
            return JsonResponse({"status": "error", "message": "Cart is empty"}, status=400)

        subtotal = 0.0
        order_items_to_create = []

        # Validate items & calculate subtotal
        for item in items_data:
            product_id = item.get('product_id')
            qty = int(item.get('quantity', 1))
            try:
                prod = Product.objects.get(pk=product_id)
                if prod.stock < qty:
                    return JsonResponse({"status": "error", "message": f"Insufficient stock for {prod.name}. Available: {prod.stock}"}, status=400)
                item_price = float(prod.price)
                subtotal += item_price * qty
                order_items_to_create.append((prod, qty, item_price))
            except Product.DoesNotExist:
                return JsonResponse({"status": "error", "message": f"Product ID {product_id} not found"}, status=400)

        # Discount calculation
        discount = 0.0
        if coupon_code == "LUMINA20":
            discount = round(subtotal * 0.20, 2)
        elif coupon_code == "AURA10":
            discount = min(subtotal, 10.00)
        elif coupon_code == "WELCOME10":
            discount = round(subtotal * 0.10, 2)

        # Tax calculation (8%)
        taxable = max(0.0, subtotal - discount)
        tax = round(taxable * 0.08, 2)
        shipping_fee = 0.0 if (subtotal >= 150.0 or coupon_code == "FREESHIP") else 15.00
        total = round(taxable + tax + shipping_fee, 2)

        # Generate unique readable order number e.g. LUM-892410
        order_number = f"LUM-{str(uuid.uuid4().hex[:6]).upper()}"

        order = Order.objects.create(
            order_number=order_number,
            customer_name=customer_name,
            customer_email=customer_email,
            shipping_address=shipping_address,
            payment_method=payment_method,
            subtotal=subtotal,
            discount=discount,
            tax=tax,
            total=total,
            status='Processing'
        )

        for prod, qty, price in order_items_to_create:
            OrderItem.objects.create(
                order=order,
                product=prod,
                quantity=qty,
                price=price
            )
            # Deduct stock
            prod.stock = max(0, prod.stock - qty)
            prod.save()

        return JsonResponse({
            "status": "success",
            "message": "Order placed successfully!",
            "order": {
                "order_number": order.order_number,
                "customer_name": order.customer_name,
                "customer_email": order.customer_email,
                "shipping_address": order.shipping_address,
                "payment_method": order.payment_method,
                "subtotal": float(order.subtotal),
                "discount": float(order.discount),
                "tax": float(order.tax),
                "shipping_fee": shipping_fee,
                "total": float(order.total),
                "status": order.status,
                "created_at": order.created_at.strftime("%B %d, %Y - %H:%M")
            }     
        })

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

@require_http_methods(["GET"])
def get_order_tracking(request, order_number):
    try:
        order = Order.objects.get(order_number__iexact=order_number)
        items = [{
            "product_name": item.product.name,
            "image": item.product.image,
            "quantity": item.quantity,
            "price": float(item.price),
            "total": float(item.price * item.quantity)
        } for item in order.items.all()]

        return JsonResponse({
            "status": "success",
            "order": {
                "order_number": order.order_number,
                "customer_name": order.customer_name,
                "customer_email": order.customer_email,
                "shipping_address": order.shipping_address,
                "payment_method": order.payment_method,
                "subtotal": float(order.subtotal),
                "discount": float(order.discount),
                "tax": float(order.tax),
                "total": float(order.total),
                "status": order.status,
                "created_at": order.created_at.strftime("%B %d, %Y - %H:%M"),
                "items": items
            }
        })
    except Order.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Order number not found"}, status=404)
