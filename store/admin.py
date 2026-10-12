from django.contrib import admin
from store.models import Category, Product, Review, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'icon')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'old_price', 'stock', 'rating', 'badge', 'is_featured')
    list_filter = ('category', 'badge', 'is_featured')
    search_fields = ('name', 'description', 'tags')
    list_editable = ('price', 'stock', 'badge', 'is_featured')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'author', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('author', 'comment', 'product__name')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer_name', 'customer_email', 'total', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'customer_name', 'customer_email')
    list_editable = ('status',)
    inlines = [OrderItemInline]
