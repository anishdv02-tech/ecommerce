// LUMINA E-COMMERCE FULLSTACK APPLICATION LOGIC

const STATE = {
  products: [],
  categories: [],
  cart: JSON.parse(localStorage.getItem('lumina_cart') || '[]'),
  wishlist: JSON.parse(localStorage.getItem('lumina_wishlist') || '[]'),
  currentCategory: 'all',
  currentTag: 'all',
  searchQuery: '',
  sortBy: 'featured',
  currency: 'USD',
  rates: { USD: 1.0, EUR: 0.92, GBP: 0.79, INR: 83.5 },
  symbols: { USD: '$', EUR: '€', GBP: '£', INR: '₹' },
  appliedCoupon: null,
  activeQuickViewProduct: null,
};

// INITIALIZATION
document.addEventListener('DOMContentLoaded', () => {
  fetchCategories();
  fetchProducts();
  updateCartBadge();
  updateWishlistBadge();
  setupEventListeners();
  startFlashTimer();
});

// CURRENCY FORMATTER HELPER
function formatPrice(amountInUSD) {
  const rate = STATE.rates[STATE.currency] || 1.0;
  const symbol = STATE.symbols[STATE.currency] || '$';
  const converted = (amountInUSD * rate).toFixed(2);
  return `${symbol}${converted}`;
}

// FETCH CATEGORIES FROM DJANGO BACKEND API
async function fetchCategories() {
  try {
    const res = await fetch('/api/categories/');
    const data = await res.json();
    if (data.status === 'success') {
      STATE.categories = data.categories;
      renderCategories(data.categories);
    }
  } catch (err) {
    console.error('Failed to fetch categories:', err);
  }
}

// RENDER CATEGORY PILLS
function renderCategories(categories) {
  const container = document.getElementById('categoriesScroll');
  if (!container) return;

  let html = `
    <button class="category-pill ${STATE.currentCategory === 'all' ? 'active' : ''}" onclick="filterByCategory('all')">
      <i class="bi bi-grid-fill"></i> All Items
    </button>
  `;

  categories.forEach(cat => {
    html += `
      <button class="category-pill ${STATE.currentCategory === cat.slug ? 'active' : ''}" onclick="filterByCategory('${cat.slug}')">
        <i class="bi ${cat.icon || 'bi-tag'}"></i> ${cat.name} (${cat.product_count})
      </button>
    `;
  });

  container.innerHTML = html;
}

// FETCH PRODUCTS FROM DJANGO BACKEND API
async function fetchProducts() {
  const grid = document.getElementById('productsGrid');
  if (grid) {
    grid.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 60px 0; color: var(--text-muted);">
        <i class="bi bi-arrow-repeat spin-icon" style="font-size: 2.5rem; display: inline-block; animation: spin 1s linear infinite;"></i>
        <p style="margin-top: 12px; font-weight: 600;">Loading Lumina Tech Catalog...</p>
      </div>
    `;
  }

  try {
    let url = `/api/products/?category=${STATE.currentCategory}&sort=${STATE.sortBy}`;
    if (STATE.searchQuery) url += `&search=${encodeURIComponent(STATE.searchQuery)}`;
    if (STATE.currentTag !== 'all') url += `&badge=${encodeURIComponent(STATE.currentTag)}`;

    const res = await fetch(url);
    const data = await res.json();
    if (data.status === 'success') {
      STATE.products = data.products;
      renderProducts(data.products);
      const countEl = document.getElementById('resultsCount');
      if (countEl) countEl.innerText = `Showing ${data.count} items`;
    }
  } catch (err) {
    console.error('Failed to fetch products:', err);
  }
}

// RENDER PRODUCTS GRID
function renderProducts(products) {
  const grid = document.getElementById('productsGrid');
  if (!grid) return;

  if (products.length === 0) {
    grid.innerHTML = `
      <div style="grid-column: 1/-1; text-align: center; padding: 80px 20px; background: var(--bg-card); border-radius: var(--radius-lg); border: 1px solid var(--border-glass);">
        <i class="bi bi-search" style="font-size: 3rem; color: var(--text-dim);"></i>
        <h3 style="margin-top: 16px;">No products match your criteria</h3>
        <p style="color: var(--text-muted); margin-top: 6px;">Try clearing filters or changing search keywords.</p>
        <button class="btn-primary" style="margin-top: 20px;" onclick="resetFilters()">Reset All Filters</button>
      </div>
    `;
    return;
  }

  let html = '';
  products.forEach(product => {
    const isWishlisted = STATE.wishlist.includes(product.id);
    const badgeClass = product.badge ? `badge-${product.badge.toLowerCase()}` : '';

    html += `
      <div class="product-card" id="prod-card-${product.id}">
        <div class="product-image-box">
          ${product.badge ? `<span class="badge ${badgeClass} badge-position">${product.badge}</span>` : ''}
          <button class="wishlist-btn-pos ${isWishlisted ? 'active' : ''}" onclick="toggleWishlist(${product.id})" title="Wishlist">
            <i class="bi ${isWishlisted ? 'bi-heart-fill' : 'bi-heart'}"></i>
          </button>
          <img src="${product.image}" alt="${product.name}" loading="lazy" />
          <div class="quick-view-overlay">
            <button class="btn-quick-view" onclick="openQuickView(${product.id})">
              <i class="bi bi-eye"></i> Quick View
            </button>
          </div>
        </div>
        <div class="product-info">
          <div class="product-category">${product.category_name}</div>
          <h3 class="product-title" title="${product.name}">${product.name}</h3>
          <div class="product-rating">
            <span>${renderStars(product.rating)}</span>
            <span style="font-weight: 700;">${product.rating.toFixed(1)}</span>
            <span class="rating-count">(${product.review_count})</span>
          </div>
          <div class="product-bottom-row">
            <div class="price-box">
              <span class="current-price">${formatPrice(product.price)}</span>
              ${product.old_price ? `<span class="old-price">${formatPrice(product.old_price)}</span>` : ''}
            </div>
            <button class="btn-add-cart" onclick="addToCart(${product.id})">
              <i class="bi bi-bag-plus"></i> Add
            </button>
          </div>
        </div>
      </div>
    `;
  });

  grid.innerHTML = html;
}

// RENDER STAR RATING SVG / ICONS
function renderStars(rating) {
  let stars = '';
  const full = Math.floor(rating);
  const half = rating % 1 >= 0.5;

  for (let i = 1; i <= 5; i++) {
    if (i <= full) {
      stars += `<i class="bi bi-star-fill"></i>`;
    } else if (i === full + 1 && half) {
      stars += `<i class="bi bi-star-half"></i>`;
    } else {
      stars += `<i class="bi bi-star"></i>`;
    }
  }
  return stars;
}

// FILTER HANDLERS
function filterByCategory(slug) {
  STATE.currentCategory = slug;
  renderCategories(STATE.categories);
  fetchProducts();
}

function filterByTag(tag) {
  STATE.currentTag = STATE.currentTag === tag ? 'all' : tag;
  document.querySelectorAll('.tag-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.tag === STATE.currentTag);
  });
  fetchProducts();
}

function handleSortChange(val) {
  STATE.sortBy = val;
  fetchProducts();
}

function resetFilters() {
  STATE.currentCategory = 'all';
  STATE.currentTag = 'all';
  STATE.searchQuery = '';
  STATE.sortBy = 'featured';

  const searchInput = document.getElementById('searchInput');
  if (searchInput) searchInput.value = '';

  renderCategories(STATE.categories);
  fetchProducts();
}

// CART SYSTEM
function addToCart(productId, qty = 1) {
  const existing = STATE.cart.find(item => item.product_id === productId);
  if (existing) {
    existing.quantity += qty;
  } else {
    STATE.cart.push({ product_id: productId, quantity: qty });
  }

  saveCart();
  updateCartBadge();
  showToast('Item added to cart!');

  // Trigger floating cart preview animation
  const cartBtn = document.getElementById('openCartBtn');
  if (cartBtn) {
    cartBtn.style.transform = 'scale(1.25)';
    setTimeout(() => cartBtn.style.transform = 'none', 300);
  }
}

function removeFromCart(productId) {
  STATE.cart = STATE.cart.filter(item => item.product_id !== productId);
  saveCart();
  updateCartBadge();
  renderCartDrawer();
}

function updateCartQty(productId, change) {
  const item = STATE.cart.find(i => i.product_id === productId);
  if (item) {
    item.quantity += change;
    if (item.quantity <= 0) {
      removeFromCart(productId);
    } else {
      saveCart();
      updateCartBadge();
      renderCartDrawer();
    }
  }
}

function saveCart() {
  localStorage.setItem('lumina_cart', JSON.stringify(STATE.cart));
}

function updateCartBadge() {
  const badge = document.getElementById('cartBadge');
  const totalItems = STATE.cart.reduce((sum, item) => sum + item.quantity, 0);
  if (badge) badge.innerText = totalItems;
}

// CART DRAWER RENDER
async function renderCartDrawer() {
  const body = document.getElementById('cartDrawerBody');
  const footer = document.getElementById('cartDrawerFooter');

  if (!body) return;

  if (STATE.cart.length === 0) {
    body.innerHTML = `
      <div style="text-align: center; padding: 60px 0; color: var(--text-muted);">
        <i class="bi bi-cart-x" style="font-size: 3.5rem; color: var(--text-dim);"></i>
        <h4 style="margin-top: 16px; color: var(--text-main);">Your cart is currently empty</h4>
        <p style="font-size: 0.85rem; margin-top: 6px;">Explore 30+ premium tech items in our store!</p>
      </div>
    `;
    if (footer) footer.style.display = 'none';
    return;
  }

  if (footer) footer.style.display = 'block';

  // Fetch full details of products in cart
  body.innerHTML = `<div style="text-align:center; padding: 40px;"><i class="bi bi-arrow-repeat spin-icon" style="font-size:2rem;"></i></div>`;

  let subtotal = 0;
  let itemsHtml = '';

  for (const item of STATE.cart) {
    let product = STATE.products.find(p => p.id === item.product_id);

    if (!product) {
      try {
        const res = await fetch(`/api/products/${item.product_id}/`);
        const data = await res.json();
        if (data.status === 'success') product = data.product;
      } catch (e) {}
    }

    if (product) {
      const itemTotal = product.price * item.quantity;
      subtotal += itemTotal;

      itemsHtml += `
        <div class="cart-item">
          <img src="${product.image}" alt="${product.name}" />
          <div class="cart-item-details">
            <h4 class="cart-item-title">${product.name}</h4>
            <div class="cart-item-price">${formatPrice(product.price)}</div>
            <div style="display:flex; align-items:center; justify-content:space-between; margin-top:6px;">
              <div class="qty-controls">
                <button class="qty-btn" onclick="updateCartQty(${product.id}, -1)">-</button>
                <span class="qty-val">${item.quantity}</span>
                <button class="qty-btn" onclick="updateCartQty(${product.id}, 1)">+</button>
              </div>
              <button style="background:none; border:none; color:var(--accent-rose); cursor:pointer;" onclick="removeFromCart(${product.id})">
                <i class="bi bi-trash"></i>
              </button>
            </div>
          </div>
        </div>
      `;
    }
  }

  body.innerHTML = itemsHtml;

  // Calculate totals with coupon if any
  let discount = 0;
  if (STATE.appliedCoupon) {
    discount = STATE.appliedCoupon.discount_amount || 0;
  }

  const tax = Math.round((subtotal - discount) * 0.08 * 100) / 100;
  const shipping = subtotal >= 150 ? 0 : 15;
  const total = Math.max(0, subtotal - discount) + tax + shipping;

  const subtotalEl = document.getElementById('cartSubtotal');
  const discountEl = document.getElementById('cartDiscount');
  const taxEl = document.getElementById('cartTax');
  const shippingEl = document.getElementById('cartShipping');
  const totalEl = document.getElementById('cartTotal');

  if (subtotalEl) subtotalEl.innerText = formatPrice(subtotal);
  if (discountEl) discountEl.innerText = discount > 0 ? `-${formatPrice(discount)}` : '$0.00';
  if (taxEl) taxEl.innerText = formatPrice(tax);
  if (shippingEl) shippingEl.innerText = shipping === 0 ? 'FREE' : formatPrice(shipping);
  if (totalEl) totalEl.innerText = formatPrice(total);
}

// APPLY PROMO COUPON CODE
async function applyCoupon() {
  const input = document.getElementById('couponCodeInput');
  if (!input) return;
  const code = input.value.trim().toUpperCase();
  if (!code) return;

  const subtotal = STATE.cart.reduce((sum, item) => {
    const prod = STATE.products.find(p => p.id === item.product_id);
    return sum + (prod ? prod.price * item.quantity : 0);
  }, 0);

  try {
    const res = await fetch('/api/coupons/validate/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code, subtotal })
    });
    const data = await res.json();

    if (data.status === 'success') {
      STATE.appliedCoupon = data;
      showToast(`Coupon '${code}' applied! (${data.description})`);
      renderCartDrawer();
    } else {
      showToast(data.message || 'Invalid coupon code', 'error');
    }
  } catch (err) {
    showToast('Failed to validate coupon', 'error');
  }
}

// WISHLIST SYSTEM
function toggleWishlist(productId) {
  const idx = STATE.wishlist.indexOf(productId);
  if (idx > -1) {
    STATE.wishlist.splice(idx, 1);
    showToast('Removed from wishlist');
  } else {
    STATE.wishlist.push(productId);
    showToast('Added to wishlist!');
  }

  localStorage.setItem('lumina_wishlist', JSON.stringify(STATE.wishlist));
  updateWishlistBadge();

  // Re-render target product card star heart icon
  const btn = document.querySelector(`#prod-card-${productId} .wishlist-btn-pos`);
  if (btn) {
    const active = STATE.wishlist.includes(productId);
    btn.classList.toggle('active', active);
    btn.innerHTML = `<i class="bi ${active ? 'bi-heart-fill' : 'bi-heart'}"></i>`;
  }
}

function updateWishlistBadge() {
  const badge = document.getElementById('wishlistBadge');
  if (badge) badge.innerText = STATE.wishlist.length;
}

// QUICK VIEW MODAL
async function openQuickView(productId) {
  const modal = document.getElementById('quickViewModal');
  const content = document.getElementById('quickViewContent');
  if (!modal || !content) return;

  content.innerHTML = `<div style="text-align:center; padding: 60px;"><i class="bi bi-arrow-repeat spin-icon" style="font-size:2.5rem;"></i></div>`;
  modal.classList.add('active');

  try {
    const res = await fetch(`/api/products/${productId}/`);
    const data = await res.json();
    if (data.status === 'success') {
      const p = data.product;
      STATE.activeQuickViewProduct = p;

      const specsHtml = p.short_specs && p.short_specs.length
        ? `<ul style="margin: 12px 0 16px 20px; color: var(--text-muted); font-size: 0.88rem;">${p.short_specs.map(s => `<li style="margin-bottom:4px;">${s}</li>`).join('')}</ul>`
        : '';

      const reviewsHtml = p.reviews_list && p.reviews_list.length
        ? p.reviews_list.map(r => `
            <div style="background: rgba(255,255,255,0.03); border:1px solid var(--border-glass); border-radius: var(--radius-sm); padding:12px; margin-bottom:10px;">
              <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                <strong style="font-size:0.85rem;">${r.author}</strong>
                <span style="color:var(--accent-amber); font-size:0.8rem;">${renderStars(r.rating)}</span>
              </div>
              <p style="font-size:0.82rem; color:var(--text-muted);">${r.comment}</p>
            </div>
          `).join('')
        : '<p style="color:var(--text-dim); font-size:0.85rem;">No customer reviews yet. Be the first to review!</p>';

      content.innerHTML = `
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; padding: 24px;">
          <div>
            <img src="${p.image}" alt="${p.name}" style="width: 100%; border-radius: var(--radius-md); object-fit: cover; height: 320px; border:1px solid var(--border-glass);" />
          </div>
          <div>
            <span class="product-category">${p.category_name}</span>
            <h2 style="font-size: 1.6rem; margin: 4px 0 8px;">${p.name}</h2>
            <div class="product-rating" style="margin-bottom:12px;">
              ${renderStars(p.rating)} <span style="font-weight:700;">${p.rating.toFixed(1)}</span> (${p.review_count} reviews)
            </div>
            <div style="font-size: 1.6rem; font-weight: 800; color: var(--text-main); margin-bottom: 12px;">
              ${formatPrice(p.price)}
              ${p.old_price ? `<span style="font-size: 1rem; color: var(--text-dim); text-decoration: line-through; margin-left: 8px;">${formatPrice(p.old_price)}</span>` : ''}
            </div>
            <p style="color: var(--text-muted); font-size: 0.9rem; line-height: 1.5; margin-bottom: 12px;">${p.description}</p>
            ${specsHtml}
            <div style="display: flex; gap: 12px; align-items: center; margin-top: 20px;">
              <button class="btn-primary" onclick="addToCart(${p.id}); closeQuickView();">
                <i class="bi bi-bag-plus"></i> Add to Shopping Bag
              </button>
              <button class="btn-outline" onclick="toggleWishlist(${p.id})">
                <i class="bi bi-heart"></i>
              </button>
            </div>
          </div>
        </div>

        <!-- REVIEWS SECTION -->
        <div style="border-top: 1px solid var(--border-glass); padding: 24px;">
          <h4 style="margin-bottom: 16px;">Customer Reviews & Ratings</h4>
          <div style="max-height: 200px; overflow-y: auto; margin-bottom: 20px;">
            ${reviewsHtml}
          </div>

          <!-- WRITE REVIEW FORM -->
          <form onsubmit="submitReview(event, ${p.id})" style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-glass); padding: 16px; border-radius: var(--radius-md);">
            <h5 style="margin-bottom: 10px; font-size: 0.9rem;">Submit a Review</h5>
            <div style="display: flex; gap: 10px; margin-bottom: 10px;">
              <input type="text" id="reviewAuthor" placeholder="Your Name" required class="promo-input" style="flex:1;" />
              <select id="reviewRating" class="currency-select">
                <option value="5">⭐⭐⭐⭐⭐ (5/5)</option>
                <option value="4">⭐⭐⭐⭐ (4/5)</option>
                <option value="3">⭐⭐⭐ (3/5)</option>
                <option value="2">⭐⭐ (2/5)</option>
                <option value="1">⭐ (1/5)</option>
              </select>
            </div>
            <textarea id="reviewComment" placeholder="Write your honest review..." required class="promo-input" style="width:100%; height:70px; resize:none; margin-bottom:10px;"></textarea>
            <button type="submit" class="btn-primary" style="padding: 8px 18px; font-size: 0.85rem;">Submit Review</button>
          </form>
        </div>
      `;
    }
  } catch (err) {
    content.innerHTML = `<p style="padding:40px; color:var(--accent-rose);">Failed to load product details.</p>`;
  }
}

function closeQuickView() {
  const modal = document.getElementById('quickViewModal');
  if (modal) modal.classList.remove('active');
}

// SUBMIT REVIEW
async function submitReview(event, productId) {
  event.preventDefault();
  const author = document.getElementById('reviewAuthor').value.trim();
  const rating = document.getElementById('reviewRating').value;
  const comment = document.getElementById('reviewComment').value.trim();

  try {
    const res = await fetch(`/api/reviews/${productId}/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ author, rating, comment })
    });
    const data = await res.json();

    if (data.status === 'success') {
      showToast('Thank you! Your review has been published.');
      openQuickView(productId); // Refresh modal view
      fetchProducts(); // Refresh catalog rating
    } else {
      showToast(data.message || 'Failed to post review', 'error');
    }
  } catch (err) {
    showToast('Failed to post review', 'error');
  }
}

// CHECKOUT SYSTEM
function openCheckoutModal() {
  if (STATE.cart.length === 0) {
    showToast('Your cart is empty!', 'error');
    return;
  }
  closeCartDrawer();
  const modal = document.getElementById('checkoutModal');
  if (modal) {
    modal.classList.add('active');
    renderCheckoutSummary();
  }
}

function closeCheckoutModal() {
  const modal = document.getElementById('checkoutModal');
  if (modal) modal.classList.remove('active');
}

function renderCheckoutSummary() {
  const summaryBox = document.getElementById('checkoutSummaryBox');
  if (!summaryBox) return;

  let subtotal = 0;
  STATE.cart.forEach(item => {
    const prod = STATE.products.find(p => p.id === item.product_id);
    if (prod) subtotal += prod.price * item.quantity;
  });

  let discount = STATE.appliedCoupon ? STATE.appliedCoupon.discount_amount || 0 : 0;
  const tax = Math.round((subtotal - discount) * 0.08 * 100) / 100;
  const shipping = subtotal >= 150 ? 0 : 15;
  const total = Math.max(0, subtotal - discount) + tax + shipping;

  summaryBox.innerHTML = `
    <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.9rem;">
      <span>Subtotal (${STATE.cart.length} items):</span>
      <span>${formatPrice(subtotal)}</span>
    </div>
    ${discount > 0 ? `<div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.9rem; color:var(--accent-emerald);"><span>Discount:</span><span>-${formatPrice(discount)}</span></div>` : ''}
    <div style="display:flex; justify-content:space-between; margin-bottom:8px; font-size:0.9rem;">
      <span>Estimated Tax (8%):</span>
      <span>${formatPrice(tax)}</span>
    </div>
    <div style="display:flex; justify-content:space-between; margin-bottom:12px; font-size:0.9rem;">
      <span>Shipping:</span>
      <span>${shipping === 0 ? 'FREE' : formatPrice(shipping)}</span>
    </div>
    <div style="display:flex; justify-content:space-between; font-weight:800; font-size:1.2rem; border-top:1px solid var(--border-glass); padding-top:12px; color:var(--accent-cyan);">
      <span>Total Due:</span>
      <span>${formatPrice(total)}</span>
    </div>
  `;
}

// PROCESS CHECKOUT FORM SUBMISSION
async function handleCheckoutSubmit(event) {
  event.preventDefault();
  const name = document.getElementById('chkName').value.trim();
  const email = document.getElementById('chkEmail').value.trim();
  const address = document.getElementById('chkAddress').value.trim();
  const payment_method = document.getElementById('chkPayment').value;

  const btn = document.getElementById('chkSubmitBtn');
  if (btn) {
    btn.disabled = true;
    btn.innerHTML = `<i class="bi bi-arrow-repeat spin-icon"></i> Processing Payment...`;
  }

  const payload = {
    name,
    email,
    address,
    payment_method,
    items: STATE.cart,
    coupon_code: STATE.appliedCoupon ? STATE.appliedCoupon.code : ''
  };

  try {
    const res = await fetch('/api/checkout/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await res.json();

    if (data.status === 'success') {
      // Clear cart
      STATE.cart = [];
      STATE.appliedCoupon = null;
      saveCart();
      updateCartBadge();
      closeCheckoutModal();

      // Show receipt modal
      openReceiptModal(data.order);
      fetchProducts(); // Refresh stock counts in UI
    } else {
      showToast(data.message || 'Checkout failed', 'error');
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = `Complete Order`;
      }
    }
  } catch (err) {
    showToast('Order processing error. Please try again.', 'error');
    if (btn) {
      btn.disabled = false;
      btn.innerHTML = `Complete Order`;
    }
  }
}

// RECEIPT MODAL
function openReceiptModal(order) {
  const modal = document.getElementById('receiptModal');
  const box = document.getElementById('receiptContent');
  if (!modal || !box) return;

  box.innerHTML = `
    <div style="text-align: center; padding: 20px;">
      <div style="width: 70px; height: 70px; border-radius: 50%; background: rgba(16, 185, 129, 0.2); color: var(--accent-emerald); display: flex; align-items: center; justify-content: center; font-size: 2.5rem; margin: 0 auto 16px;">
        <i class="bi bi-check-circle-fill"></i>
      </div>
      <h2 style="font-size: 1.8rem; margin-bottom: 6px;">Order Confirmed!</h2>
      <p style="color: var(--text-muted); font-size: 0.9rem;">Thank you, ${order.customer_name}. A receipt has been sent to ${order.customer_email}.</p>

      <div style="background: rgba(255,255,255,0.03); border: 1px dashed var(--border-glow); padding: 16px; border-radius: var(--radius-md); margin: 24px 0; text-align: left;">
        <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
          <strong style="color:var(--accent-cyan);">Tracking Order #:</strong>
          <span style="font-family:monospace; font-weight:800; font-size:1.1rem; color:#fff;">${order.order_number}</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:0.85rem;">
          <span style="color:var(--text-muted);">Payment Method:</span>
          <span>${order.payment_method}</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:4px; font-size:0.85rem;">
          <span style="color:var(--text-muted);">Shipping Address:</span>
          <span>${order.shipping_address}</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-top:8px; font-weight:700; font-size:1.1rem; border-top:1px solid var(--border-glass); padding-top:8px;">
          <span>Total Paid:</span>
          <span style="color:var(--accent-emerald);">${formatPrice(order.total)}</span>
        </div>
      </div>

      <div style="display: flex; gap: 12px; justify-content: center;">
        <button class="btn-primary" onclick="closeReceiptModal(); trackOrder('${order.order_number}');">
          <i class="bi bi-truck"></i> Track Order Status
        </button>
        <button class="btn-outline" onclick="closeReceiptModal();">Continue Shopping</button>
      </div>
    </div>
  `;

  modal.classList.add('active');
}

function closeReceiptModal() {
  const modal = document.getElementById('receiptModal');
  if (modal) modal.classList.remove('active');
}

// ORDER TRACKING SYSTEM
async function trackOrder(orderNum = null) {
  if (!orderNum) {
    const input = document.getElementById('trackOrderInput');
    if (input) orderNum = input.value.trim();
  }

  if (!orderNum) {
    showToast('Please enter an order number', 'error');
    return;
  }

  const modal = document.getElementById('trackingModal');
  const box = document.getElementById('trackingContent');
  if (!modal || !box) return;

  box.innerHTML = `<div style="text-align:center; padding: 40px;"><i class="bi bi-arrow-repeat spin-icon" style="font-size:2rem;"></i> Loading order status...</div>`;
  modal.classList.add('active');

  try {
    const res = await fetch(`/api/orders/${encodeURIComponent(orderNum)}/`);
    const data = await res.json();

    if (data.status === 'success') {
      const o = data.order;
      const itemsList = o.items.map(i => `
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:10px; font-size:0.88rem;">
          <img src="${i.image}" style="width:40px; height:40px; border-radius:6px; object-fit:cover;" />
          <div style="flex:1;">${i.product_name} x ${i.quantity}</div>
          <div style="font-weight:700;">${formatPrice(i.total)}</div>
        </div>
      `).join('');

      box.innerHTML = `
        <h3 style="margin-bottom:6px;">Order Tracking</h3>
        <p style="color:var(--text-muted); font-size:0.85rem; margin-bottom:20px;">Order #${o.order_number} placed on ${o.created_at}</p>

        <!-- TRACKING TIMELINE -->
        <div style="display:flex; justify-content:space-between; position:relative; margin: 30px 0 40px;">
          <div style="position:absolute; top:18px; left:10%; right:10%; height:4px; background:rgba(255,255,255,0.1); z-index:1;"></div>
          <div style="position:absolute; top:18px; left:10%; width:60%; height:4px; background:var(--accent-cyan); z-index:1;"></div>

          <div style="position:relative; z-index:2; text-align:center;">
            <div style="width:36px; height:36px; border-radius:50%; background:var(--accent-cyan); color:#000; display:flex; align-items:center; justify-content:center; font-weight:800; margin:0 auto 6px;">✓</div>
            <span style="font-size:0.75rem; font-weight:700;">Order Placed</span>
          </div>
          <div style="position:relative; z-index:2; text-align:center;">
            <div style="width:36px; height:36px; border-radius:50%; background:var(--accent-cyan); color:#000; display:flex; align-items:center; justify-content:center; font-weight:800; margin:0 auto 6px;">✓</div>
            <span style="font-size:0.75rem; font-weight:700;">Processing</span>
          </div>
          <div style="position:relative; z-index:2; text-align:center;">
            <div style="width:36px; height:36px; border-radius:50%; background:var(--accent-primary); color:#fff; display:flex; align-items:center; justify-content:center; font-weight:800; margin:0 auto 6px;"><i class="bi bi-truck"></i></div>
            <span style="font-size:0.75rem; font-weight:700; color:var(--accent-primary);">In Transit</span>
          </div>
          <div style="position:relative; z-index:2; text-align:center;">
            <div style="width:36px; height:36px; border-radius:50%; background:rgba(255,255,255,0.1); color:var(--text-dim); display:flex; align-items:center; justify-content:center; font-weight:800; margin:0 auto 6px;">4</div>
            <span style="font-size:0.75rem; color:var(--text-dim);">Delivered</span>
          </div>
        </div>

        <div style="background:rgba(255,255,255,0.03); border:1px solid var(--border-glass); padding:16px; border-radius:var(--radius-md);">
          <h4 style="font-size:0.9rem; margin-bottom:12px;">Items in Package:</h4>
          ${itemsList}
        </div>
      `;
    } else {
      box.innerHTML = `<p style="color:var(--accent-rose); padding:20px;">Order number not found. Check your tracking number.</p>`;
    }
  } catch (err) {
    box.innerHTML = `<p style="color:var(--accent-rose); padding:20px;">Error retrieving order tracking info.</p>`;
  }
}

function closeTrackingModal() {
  const modal = document.getElementById('trackingModal');
  if (modal) modal.classList.remove('active');
}

// LIVE SEARCH AUTOCOMPLETE
function setupEventListeners() {
  const searchInput = document.getElementById('searchInput');
  const dropdown = document.getElementById('searchResultsDropdown');

  if (searchInput && dropdown) {
    searchInput.addEventListener('input', (e) => {
      const q = e.target.value.trim().toLowerCase();
      STATE.searchQuery = q;

      if (q.length < 2) {
        dropdown.classList.remove('active');
        fetchProducts();
        return;
      }

      const matches = STATE.products.filter(p => p.name.toLowerCase().includes(q) || p.category_name.toLowerCase().includes(q)).slice(0, 5);

      if (matches.length > 0) {
        dropdown.innerHTML = matches.map(m => `
          <div class="search-item" onclick="openQuickView(${m.id}); document.getElementById('searchResultsDropdown').classList.remove('active');">
            <img src="${m.image}" alt="${m.name}" />
            <div class="search-item-info">
              <div class="search-item-title">${m.name}</div>
              <div class="search-item-price">${formatPrice(m.price)}</div>
            </div>
          </div>
        `).join('');
        dropdown.classList.add('active');
      } else {
        dropdown.classList.remove('active');
      }

      fetchProducts();
    });

    document.addEventListener('click', (e) => {
      if (!searchInput.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.classList.remove('active');
      }
    });
  }

  // Currency select handler
  const currSelect = document.getElementById('currencySelect');
  if (currSelect) {
    currSelect.addEventListener('change', (e) => {
      STATE.currency = e.target.value;
      renderProducts(STATE.products);
      if (document.getElementById('cartDrawer').classList.contains('active')) renderCartDrawer();
    });
  }
}

// DRAWER TOGGLES
function openCartDrawer() {
  renderCartDrawer();
  const drawer = document.getElementById('cartDrawer');
  const backdrop = document.getElementById('drawerBackdrop');
  if (drawer && backdrop) {
    drawer.classList.add('active');
    backdrop.classList.add('active');
  }
}

function closeCartDrawer() {
  const drawer = document.getElementById('cartDrawer');
  const backdrop = document.getElementById('drawerBackdrop');
  if (drawer && backdrop) {
    drawer.classList.remove('active');
    backdrop.classList.remove('active');
  }
}

// FLASH TIMER
function startFlashTimer() {
  let time = 3600 * 14 + 1800 + 45; // 14h 30m 45s
  setInterval(() => {
    if (time <= 0) time = 3600 * 24;
    time--;
    const h = Math.floor(time / 3600);
    const m = Math.floor((time % 3600) / 60);
    const s = time % 60;

    const hEl = document.getElementById('timerHours');
    const mEl = document.getElementById('timerMins');
    const sEl = document.getElementById('timerSecs');

    if (hEl) hEl.innerText = String(h).padStart(2, '0');
    if (mEl) mEl.innerText = String(m).padStart(2, '0');
    if (sEl) sEl.innerText = String(s).padStart(2, '0');
  }, 1000);
}

// TOAST NOTIFICATIONS
function showToast(message, type = 'info') {
  let container = document.getElementById('toastContainer');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = 'toast-msg';
  toast.style.borderColor = type === 'error' ? 'var(--accent-rose)' : 'var(--accent-primary)';
  toast.innerHTML = `
    <i class="bi ${type === 'error' ? 'bi-exclamation-triangle-fill' : 'bi-check-circle-fill'}" style="color: ${type === 'error' ? 'var(--accent-rose)' : 'var(--accent-cyan)'}; font-size:1.2rem;"></i>
    <span>${message}</span>
  `;

  container.appendChild(toast);
  setTimeout(() => {
    toast.style.animation = 'slide-toast 0.3s ease reverse';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

// LIGHT / DARK THEME TOGGLE
function toggleTheme() {
  document.body.classList.toggle('light-theme');
  const icon = document.getElementById('themeIcon');
  if (icon) {
    const isLight = document.body.classList.contains('light-theme');
    icon.className = isLight ? 'bi bi-sun-fill' : 'bi bi-moon-stars-fill';
  }
}
