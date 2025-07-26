// Profile Popup Functions
function toggleProfilePopup() {
    const popup = document.getElementById('userProfilePopup');
    const overlay = document.getElementById('popupOverlay');
    
    popup.classList.toggle('open');
    overlay.classList.toggle('open');
    
    document.body.style.overflow = popup.classList.contains('open') ? 'hidden' : 'auto';
}

function closeProfilePopup() {
    const popup = document.getElementById('userProfilePopup');
    const overlay = document.getElementById('popupOverlay');
    
    popup.classList.remove('open');
    overlay.classList.remove('open');
    document.body.style.overflow = 'auto';
}

// Close popup when pressing Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeProfilePopup();
    }
});

// buyerDashboard
// Profile Popup Functions
function toggleProfilePopup() {
    const popup = document.getElementById('userProfilePopup');
    const overlay = document.getElementById('popupOverlay');
    
    if (popup && overlay) {
        popup.classList.toggle('open');
        overlay.classList.toggle('open');
        
        // Prevent body scroll when popup is open
        document.body.style.overflow = popup.classList.contains('open') ? 'hidden' : 'auto';
    }
}

function closeProfilePopup() {
    const popup = document.getElementById('userProfilePopup');
    const overlay = document.getElementById('popupOverlay');
    
    if (popup && overlay) {
        popup.classList.remove('open');
        overlay.classList.remove('open');
        document.body.style.overflow = 'auto';
    }
}

// Profile Action Functions
function editProfile() {
    alert('Edit Profile functionality will be implemented here');
    closeProfilePopup();
}

function viewOrders() {
    alert('Order History functionality will be implemented here');
    closeProfilePopup();
}

function viewFavorites() {
    alert('Favorites functionality will be implemented here');
    closeProfilePopup();
}

function settings() {
    alert('Settings functionality will be implemented here');
    closeProfilePopup();
}

function logout() {
    if (confirm('Are you sure you want to logout?')) {
        // Clear any stored data (but remember: no localStorage in Claude artifacts)
        // In your actual app, you can use localStorage here
        try {
            localStorage.removeItem('cart');
            localStorage.removeItem('selectedFoodType');
            localStorage.removeItem('selectedVendor');
            localStorage.removeItem('isLoggedIn');
            localStorage.removeItem('userPhone');
        } catch (e) {
            console.log('localStorage not available');
        }
        
        // Redirect to login page
        window.location.href = 'login.html';
    }
}

// Load user data (in a real app, this would come from backend)
function loadUserData() {
    // Simulate loading user data
    const userData = {
        name: 'Foodie',
        type: 'Premium Buyer',
        location: 'Mumbai, Maharashtra',
        orders: 12,
        spent: '₹8,450',
        rating: 4.8,
        sellers: 15
    };
    
    // Update profile info if elements exist
    const profileNameElement = document.querySelector('.profile-info h3');
    if (profileNameElement) {
        profileNameElement.textContent = `Welcome, ${userData.name}!`;
    }
    
    // Update stats if elements exist
    const statNumbers = document.querySelectorAll('.stat-number');
    if (statNumbers.length >= 4) {
        statNumbers[0].textContent = userData.orders;
        statNumbers[1].textContent = userData.spent;
        statNumbers[2].textContent = userData.rating;
        statNumbers[3].textContent = userData.sellers;
    }
}

// Set active navigation link
function setActiveNavLink() {
    const currentPage = window.location.pathname.split('/').pop() || 'buyerDashboard.html';
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        const href = link.getAttribute('href');
        if (href === currentPage || 
            (currentPage === '' && href === 'buyerDashboard.html') ||
            (currentPage === '/' && href === 'buyerDashboard.html')) {
            link.classList.add('active');
        }
    });
}

// Action card click handlers
function handleActionCardClicks() {
    const actionCards = document.querySelectorAll('.action-card');
    
    actionCards.forEach(card => {
        card.addEventListener('click', function() {
            const onclick = this.getAttribute('onclick');
            if (onclick) {
                // Execute the onclick function
                eval(onclick);
            }
        });
    });
}

// Initialize dashboard
function initializeDashboard() {
    loadUserData();
    setActiveNavLink();
    handleActionCardClicks();
    
    // Add profile popup click handler
    const profileIcon = document.querySelector('.user-profile-icon');
    if (profileIcon) {
        profileIcon.addEventListener('click', toggleProfilePopup);
    }
    
    // Add profile action click handlers
    const profileActions = document.querySelectorAll('.profile-action');
    profileActions.forEach((action, index) => {
        action.addEventListener('click', function() {
            switch(index) {
                case 0: editProfile(); break;
                case 1: viewOrders(); break;
                case 2: viewFavorites(); break;
                case 3: settings(); break;
                case 4: logout(); break;
            }
        });
    });
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
});

// Close popup when pressing Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeProfilePopup();
    }
});

// Close popup when clicking outside
document.addEventListener('click', function(event) {
    const popup = document.getElementById('userProfilePopup');
    const profileIcon = document.querySelector('.user-profile-icon');
    
    if (popup && profileIcon && 
        !popup.contains(event.target) && 
        !profileIcon.contains(event.target) && 
        popup.classList.contains('open')) {
        closeProfilePopup();
    }
});

// Navigation functions for action cards
function navigateToSellers() {
    window.location.href = 'productSellers.html';
}

function navigateToProducts() {
    window.location.href = 'products.html';
}

function navigateToCart() {
    window.location.href = 'cart.html';
}

function navigateToOrders() {
    window.location.href = 'orders.html';
}

// Add smooth scroll behavior for better UX
document.documentElement.style.scrollBehavior = 'smooth';

// Add loading animation
function showLoading() {
    document.body.style.cursor = 'wait';
}

function hideLoading() {
    document.body.style.cursor = 'default';
}

// Error handling for missing elements
function safeElementOperation(selector, operation) {
    const element = document.querySelector(selector);
    if (element) {
        operation(element);
    } else {
        console.warn(`Element not found: ${selector}`);
    }
}

// Utility function to handle page transitions
function navigateTo(url) {
    showLoading();
    setTimeout(() => {
        window.location.href = url;
    }, 100);
}

// cart
// Profile Popup Functions
        // Profile Popup Functions
function toggleProfilePopup() {
    const popup = document.getElementById('userProfilePopup');
    const overlay = document.getElementById('popupOverlay');
    
    if (!popup || !overlay) return;
    
    popup.classList.toggle('open');
    overlay.classList.toggle('open');
    
    document.body.style.overflow = popup.classList.contains('open') ? 'hidden' : 'auto';
}

function closeProfilePopup() {
    const popup = document.getElementById('userProfilePopup');
    const overlay = document.getElementById('popupOverlay');
    
    if (!popup || !overlay) return;
    
    popup.classList.remove('open');
    overlay.classList.remove('open');
    document.body.style.overflow = 'auto';
}

// Profile Action Functions
function editProfile() {
    alert('Edit Profile functionality will be implemented here');
    closeProfilePopup();
}

function viewOrders() {
    alert('Order History functionality will be implemented here');
    closeProfilePopup();
}

function viewFavorites() {
    alert('Favorites functionality will be implemented here');
    closeProfilePopup();
}

function settings() {
    alert('Settings functionality will be implemented here');
    closeProfilePopup();
}

function logout() {
    if (confirm('Are you sure you want to logout?')) {
        // Clear localStorage
        localStorage.removeItem('cart');
        localStorage.removeItem('selectedFoodType');
        localStorage.removeItem('selectedVendor');
        localStorage.removeItem('isLoggedIn');
        localStorage.removeItem('userPhone');
        
        // Redirect to Django logout URL
        window.location.href = '/accounts/logout/';
    }
}

// Close popup when pressing Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeProfilePopup();
    }
});

// Cart functionality
let cart = typeof djangoCart !== 'undefined' ? djangoCart : [];

function updateCartQuantity(itemId, change) {
    const input = document.getElementById(`qty-${itemId}`);
    if (!input) return;
    
    let newQuantity;
    
    if (change === 0) {
        // Direct input change
        newQuantity = parseInt(input.value) || 1;
    } else {
        // Button click
        const currentQuantity = parseInt(input.value) || 1;
        newQuantity = Math.max(1, currentQuantity + change);
    }
    
    // Update the input value
    input.value = newQuantity;
    
    // Send AJAX request to Django backend
    updateCartItemQuantity(itemId, newQuantity);
}

function updateCartItemQuantity(itemId, quantity) {
    // Create a form and submit it
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/cart/update/${itemId}/`; // Adjust URL pattern as needed
    
    // Add CSRF token
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfToken) {
        const csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = csrfToken.value;
        form.appendChild(csrfInput);
    }
    
    // Add quantity input
    const quantityInput = document.createElement('input');
    quantityInput.type = 'hidden';
    quantityInput.name = 'quantity';
    quantityInput.value = quantity;
    form.appendChild(quantityInput);
    
    document.body.appendChild(form);
    form.submit();
}

function removeFromCart(itemId) {
    if (confirm('Are you sure you want to remove this item from your cart?')) {
        // Redirect to remove URL
        window.location.href = `/cart/remove/${itemId}/`; // Adjust URL pattern as needed
    }
}

function updateSummary() {
    // Update summary using Django data
    if (typeof cartTotals !== 'undefined') {
        const subtotalElement = document.getElementById('subtotal');
        const deliveryFeeElement = document.getElementById('deliveryFee');
        const discountElement = document.getElementById('discount');
        const totalElement = document.getElementById('total');
        
        if (subtotalElement) subtotalElement.textContent = `₹${cartTotals.subtotal}`;
        if (deliveryFeeElement) deliveryFeeElement.textContent = `₹${cartTotals.deliveryFee}`;
        if (discountElement) discountElement.textContent = `-₹${cartTotals.discount}`;
        if (totalElement) totalElement.textContent = `₹${cartTotals.total}`;
    }
}

function proceedToCheckout() {
    if (cart.length === 0) {
        alert('Your cart is empty!');
        return;
    }
    // Redirect to Django checkout URL
    window.location.href = '/checkout/'; // Adjust URL pattern as needed
}

function continueShopping() {
    // Redirect to Django products URL
    window.location.href = '/products/'; // Adjust URL pattern as needed
}

// Initialize cart functionality
document.addEventListener('DOMContentLoaded', function() {
    updateSummary();
    setActiveNavLink();
});

// Set active navigation link
function setActiveNavLink() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        const href = link.getAttribute('href');
        if (href && currentPath.includes('cart')) {
            if (href.includes('cart')) {
                link.classList.add('active');
            }
        }
    });
}

// Use Django data if available, otherwise fallback to sample data
const products = typeof djangoProducts !== 'undefined' && djangoProducts.length > 0 
    ? djangoProducts 
    : [
        // Fallback sample data
        {
            id: 1,
            name: "Fresh Tomatoes",
            description: "Organic red tomatoes, perfect for cooking and salads",
            price: 45,
            unit: "per kg",
            category: "vegetables",
            stock: "In Stock",
            image: "🍅",
            badge: "Fresh"
        },
        {
            id: 2,
            name: "Onions",
            description: "Fresh white onions, essential for Indian cooking",
            price: 30,
            unit: "per kg",
            category: "vegetables",
            stock: "In Stock",
            image: "🧅",
            badge: "Popular"
        },
        // Add more sample products as needed...
    ];

// Profile Popup Functions
function toggleProfilePopup() {
    const popup = document.getElementById('userProfilePopup');
    const overlay = document.getElementById('popupOverlay');
    
    if (!popup || !overlay) return;
    
    popup.classList.toggle('open');
    overlay.classList.toggle('open');
    
    document.body.style.overflow = popup.classList.contains('open') ? 'hidden' : 'auto';
}

function closeProfilePopup() {
    const popup = document.getElementById('userProfilePopup');
    const overlay = document.getElementById('popupOverlay');
    
    if (!popup || !overlay) return;
    
    popup.classList.remove('open');
    overlay.classList.remove('open');
    document.body.style.overflow = 'auto';
}

// Close popup when pressing Escape key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        closeProfilePopup();
    }
});

// Sample vendor data
const Sellers = {
    1: { name: "Fresh Foods Co.", avatar: "🥬", rating: 4.8 },
    2: { name: "Spice Paradise", avatar: "🌶️", rating: 4.9 },
    3: { name: "Local Dairy Farm", avatar: "🥛", rating: 4.6 },
    4: { name: "Bread & Bakery", avatar: "🍞", rating: 4.7 }
};

let cart = JSON.parse(localStorage.getItem('cart')) || [];

function renderVendorInfo() {
    const selectedVendor = localStorage.getItem('selectedVendor');
    const vendorInfo = document.getElementById('vendorInfo');
    
    if (!vendorInfo) return;
    
    if (selectedVendor && Sellers[selectedVendor]) {
        const vendor = Sellers[selectedVendor];
        vendorInfo.innerHTML = `
            <div class="vendor-avatar">${vendor.avatar}</div>
            <div class="vendor-details">
                <h3>${vendor.name}</h3>
                <div class="vendor-rating">⭐ ${vendor.rating} Rating</div>
            </div>
        `;
    }
}

function renderCategoryTabs() {
    const categories = ['all', 'vegetables', 'fruits', 'dairy', 'spices', 'grains'];
    const tabsContainer = document.getElementById('categoryTabs');
    
    if (!tabsContainer) return;
    
    tabsContainer.innerHTML = categories.map(category => `
        <div class="category-tab ${category === 'all' ? 'active' : ''}" 
             onclick="filterByCategory('${category}')">
            ${category.charAt(0).toUpperCase() + category.slice(1)}
        </div>
    `).join('');
}

function renderProducts(productsToRender) {
    const grid = document.getElementById('productsGrid');
    const resultsCount = document.getElementById('resultsCount');
    
    if (!grid || !resultsCount) return;
    
    resultsCount.textContent = `Showing ${productsToRender.length} products`;
    
    if (productsToRender.length === 0) {
        grid.innerHTML = `
            <div class="empty-products">
                <div class="empty-icon">📦</div>
                <h3>No products found</h3>
                <p>Try adjusting your filters or search terms.</p>
            </div>
        `;
        return;
    }
    
    grid.innerHTML = productsToRender.map(product => `
        <div class="product-card">
            <div class="product-badge">${product.badge}</div>
            <div class="product-image">${product.image}</div>
            <div class="product-title">${product.name}</div>
            <div class="product-description">${product.description}</div>
            <div class="product-meta">
                <div>
                    <div class="product-price">₹${product.price}</div>
                    <div class="product-unit">${product.unit}</div>
                </div>
                <div class="product-stock">${product.stock}</div>
            </div>
            <div class="product-actions">
                <div class="quantity-controls">
                    <button class="quantity-btn" onclick="updateQuantity(${product.id}, -1)">-</button>
                    <input type="number" class="quantity-input" value="0" min="0" 
                           id="qty-${product.id}" onchange="updateQuantity(${product.id}, 0)">
                    <button class="quantity-btn" onclick="updateQuantity(${product.id}, 1)">+</button>
                </div>
                <button class="btn" onclick="addToCart(${product.id})">Add to Cart</button>
            </div>
        </div>
    `).join('');
}

function filterProducts() {
    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');
    const sortSelect = document.getElementById('sortSelect');
    const priceFilter = document.getElementById('priceFilter');
    
    if (!searchInput || !categoryFilter || !sortSelect || !priceFilter) return;
    
    const searchTerm = searchInput.value.toLowerCase();
    const categoryValue = categoryFilter.value;
    const sortBy = sortSelect.value;
    const priceValue = priceFilter.value;
    
    let filtered = products.filter(product => {
        const matchesSearch = product.name.toLowerCase().includes(searchTerm) || 
                            product.description.toLowerCase().includes(searchTerm);
        
        const matchesCategory = categoryValue === 'all' || product.category === categoryValue;
        
        let matchesPrice = true;
        if (priceValue !== 'all') {
            const [min, max] = priceValue.split('-').map(Number);
            if (max) {
                matchesPrice = product.price >= min && product.price <= max;
            } else {
                matchesPrice = product.price >= min;
            }
        }
        
        return matchesSearch && matchesCategory && matchesPrice;
    });

    filtered.sort((a, b) => {
        switch(sortBy) {
            case 'name':
                return a.name.localeCompare(b.name);
            case 'price-low':
                return a.price - b.price;
            case 'price-high':
                return b.price - a.price;
            case 'popular':
                return Math.random() - 0.5; 
            default:
                return 0;
        }
    });
    
    renderProducts(filtered);
}

function filterByCategory(category) {
    // Update active tab
    document.querySelectorAll('.category-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    const clickedTab = event.target;
    if (clickedTab) {
        clickedTab.classList.add('active');
    }
    
    // Update category filter
    const categoryFilter = document.getElementById('categoryFilter');
    if (categoryFilter) {
        categoryFilter.value = category;
        filterProducts();
    }
}

function updateQuantity(productId, change) {
    const input = document.getElementById(`qty-${productId}`);
    if (!input) return;
    
    let currentQty = parseInt(input.value) || 0;
    
    if (change === 0) {
        // Direct input change
        currentQty = parseInt(input.value) || 0;
    } else {
        // Button click
        currentQty = Math.max(0, currentQty + change);
    }
    
    input.value = currentQty;
}

function addToCart(productId) {
    const input = document.getElementById(`qty-${productId}`);
    if (!input) return;
    
    const quantity = parseInt(input.value) || 0;
    
    if (quantity <= 0) {
        alert('Please select a quantity');
        return;
    }
    
    const product = products.find(p => p.id === productId);
    if (!product) return;
    
    const existingItem = cart.find(item => item.id === productId);
    
    if (existingItem) {
        existingItem.quantity += quantity;
    } else {
        cart.push({
            id: product.id,
            name: product.name,
            price: product.price,
            unit: product.unit,
            image: product.image,
            quantity: quantity
        });
    }
    
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
    input.value = 0;
    
    alert(`${quantity} ${product.name} added to cart!`);
}

function updateCartCount() {
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    const cartCountElement = document.getElementById('cartCount');
    if (cartCountElement) {
        cartCountElement.textContent = totalItems;
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Only render if we have products
    if (products && products.length > 0) {
        renderVendorInfo();
        renderCategoryTabs();
        renderProducts(products);
        updateCartCount();
        
        // Add filter event listeners
        const searchInput = document.getElementById('searchInput');
        const categoryFilter = document.getElementById('categoryFilter');
        const sortSelect = document.getElementById('sortSelect');
        const priceFilter = document.getElementById('priceFilter');
        
        if (searchInput) searchInput.addEventListener('input', filterProducts);
        if (categoryFilter) categoryFilter.addEventListener('change', filterProducts);
        if (sortSelect) sortSelect.addEventListener('change', filterProducts);
        if (priceFilter) priceFilter.addEventListener('change', filterProducts);
    }
    
    // Initialize products page
    setActiveNavLink();
});

// Set active navigation link
function setActiveNavLink() {
    const currentPage = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') && currentPage.includes(link.getAttribute('href'))) {
            link.classList.add('active');
        }
    });
}

let selectedCategory = null;

function selectCategory(category) {
    document.querySelectorAll('.food-category').forEach(cat => {
        cat.classList.remove('selected');
    });

    event.currentTarget.classList.add('selected');
    selectedCategory = category;

    document.getElementById('continueBtn').disabled = false;

    localStorage.setItem('selectedFoodType', category);
}

function continueToSellers() {
    if (!selectedCategory) {
        alert('Please select a food category first');
        return;
    }

    localStorage.setItem('selectedFoodType', selectedCategory);
    window.location.href = '/listings/sellers/';  // adjust if needed
}

function skipSelection() {
    localStorage.removeItem('selectedFoodType');
    window.location.href = '/buyer/dashboard/'; // adjust if needed
}

document.addEventListener('DOMContentLoaded', function () {
    const existingSelection = localStorage.getItem('selectedFoodType');
    if (existingSelection) {
        const categoryElement = document.querySelector(`[onclick="selectCategory('${existingSelection}')"]`);
        if (categoryElement) {
            categoryElement.classList.add('selected');
            selectedCategory = existingSelection;
            document.getElementById('continueBtn').disabled = false;
        }
    }
});

document.addEventListener('keydown', function (event) {
    if (event.key === 'Enter' && selectedCategory) {
        continueToSellers();
    }
});
function selectCategory(element, cuisineId) {
    // Remove 'selected' style from all other categories
    document.querySelectorAll('.food-category').forEach(cat => {
        cat.classList.remove('selected');
    });

    // Add 'selected' style to the clicked category
    element.classList.add('selected');

    // Set the value of the hidden input field
    document.getElementById('selectedCuisineId').value = cuisineId;

    // Enable the 'Continue' button
    document.getElementById('continueBtn').disabled = false;
}

function submitSelection() {
    // Check if a category has been selected
    const selectedId = document.getElementById('selectedCuisineId').value;
    if (selectedId) {
        // Submit the form to the Django view
        document.getElementById('categoryForm').submit();
    } else {
        alert('Please select a food category first.');
    }
}

function toggleProfilePopup() {
            const popup = document.getElementById('userProfilePopup');
            const overlay = document.getElementById('popupOverlay');
            
            popup.classList.toggle('open');
            overlay.classList.toggle('open');
            
            // Prevent body scroll when popup is open
            document.body.style.overflow = popup.classList.contains('open') ? 'hidden' : 'auto';
        }

        function closeProfilePopup() {
            const popup = document.getElementById('userProfilePopup');
            const overlay = document.getElementById('popupOverlay');
            
            popup.classList.remove('open');
            overlay.classList.remove('open');
            document.body.style.overflow = 'auto';
        }

        // Profile Action Functions
        function editProfile() {
            alert('Edit Profile functionality will be implemented here');
            closeProfilePopup();
        }

        function viewOrders() {
            alert('Order History functionality will be implemented here');
            closeProfilePopup();
        }

        function viewFavorites() {
            alert('Favorites functionality will be implemented here');
            closeProfilePopup();
        }

        function settings() {
            alert('Settings functionality will be implemented here');
            closeProfilePopup();
        }

        function logout() {
            if (confirm('Are you sure you want to logout?')) {
                // Clear any stored data
                localStorage.removeItem('cart');
                localStorage.removeItem('selectedFoodType');
                localStorage.removeItem('selectedVendor');
                localStorage.removeItem('isLoggedIn');
                localStorage.removeItem('userPhone');
                
                // Redirect to login page
                window.location.href = 'login.html';
            }
        }

        // Close popup when pressing Escape key
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Escape') {
                closeProfilePopup();
            }
        });

        // Load user data (in a real app, this would come from backend)
        function loadUserData() {
            // Simulate loading user data
            const userData = {
                name: 'Foodie',
                type: 'Premium Buyer',
                location: 'Mumbai, Maharashtra',
                orders: 12,
                spent: '₹8,450',
                rating: 4.8,
                Sellers: 15
            };
            
            // Update profile info
            document.querySelector('.profile-info h3').textContent = `Welcome, ${userData.name}!`;
        }

        let cart = JSON.parse(localStorage.getItem('cart')) || [];
        let selectedDelivery = 'standard';
        let selectedPayment = 'cod';

        function renderOrderItems() {
            const orderItemsContainer = document.getElementById('orderItems');
            
            orderItemsContainer.innerHTML = cart.map(item => `
                <div class="order-item">
                    <div class="item-info">
                        <div class="item-image">${item.image}</div>
                        <div class="item-details">
                            <h4>${item.name}</h4>
                            <p>Qty: ${item.quantity} × ₹${item.price}</p>
                        </div>
                    </div>
                    <div class="item-total">₹${item.price * item.quantity}</div>
                </div>
            `).join('');
        }

        function updateSummary() {
            const subtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
            const deliveryFee = selectedDelivery === 'express' ? 100 : 50;
            const discount = subtotal >= 500 ? 50 : 0;
            const total = subtotal + deliveryFee - discount;
            
            document.getElementById('subtotal').textContent = `₹${subtotal}`;
            document.getElementById('deliveryFee').textContent = `₹${deliveryFee}`;
            document.getElementById('discount').textContent = `-₹${discount}`;
            document.getElementById('total').textContent = `₹${total}`;
        }

        function selectDelivery(type) {
            selectedDelivery = type;
            
            // Update UI
            document.querySelectorAll('.delivery-option').forEach(option => {
                option.classList.remove('selected');
            });
            event.currentTarget.classList.add('selected');
            
            updateSummary();
        }

        function selectPayment(type) {
            selectedPayment = type;
            
            // Update UI
            document.querySelectorAll('.payment-method').forEach(method => {
                method.classList.remove('selected');
            });
            event.currentTarget.classList.add('selected');
        }

        function validateForm() {
            const requiredFields = document.querySelectorAll('input[required], select[required], textarea[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.style.borderColor = '#dc3545';
                    isValid = false;
                } else {
                    field.style.borderColor = '#ddd';
                }
            });
            
            return isValid;
        }

        function placeOrder() {
            if (!validateForm()) {
                alert('Please fill in all required fields');
                return;
            }
            
            if (cart.length === 0) {
                alert('Your cart is empty!');
                return;
            }
            
            // Collect form data
            const formData = {
                delivery: selectedDelivery,
                payment: selectedPayment,
                items: cart,
                total: document.getElementById('total').textContent,
                timestamp: new Date().toISOString()
            };
            
            // Store order in localStorage (in a real app, this would go to backend)
            localStorage.setItem('currentOrder', JSON.stringify(formData));
            
            // Clear cart
            localStorage.removeItem('cart');
            
            // Show success message
            showOrderSuccess();
        }

        function showOrderSuccess() {
            const checkoutForm = document.getElementById('checkoutForm');
            checkoutForm.innerHTML = `
                <div class="success-message">
                    <div class="success-icon">✅</div>
                    <h3>Order Placed Successfully!</h3>
                    <p>Your order has been confirmed and will be delivered soon.</p>
                    <p><strong>Order ID:</strong> #${Math.random().toString(36).substr(2, 9).toUpperCase()}</p>
                    <p><strong>Estimated Delivery:</strong> ${selectedDelivery === 'express' ? '1-2 hours' : '2-4 hours'}</p>
                    <div style="margin-top: var(--space-lg);">
                        <button class="btn" onclick="goToDashboard()">Go to Dashboard</button>
                    </div>
                </div>
            `;
        }

        function goBack() {
            window.location.href = 'cart.html';
        }

        function goToDashboard() {
            window.location.href = 'buyerDashboard.html';
        }

        // Initialize checkout
        document.addEventListener('DOMContentLoaded', function() {
            if (cart.length === 0) {
                alert('Your cart is empty! Redirecting to products page.');
                window.location.href = 'products.html';
                return;
            }
            
            renderOrderItems();
            updateSummary();
            setActiveNavLink();
            
            // Set default selections
            document.querySelector('.delivery-option').classList.add('selected');
            document.querySelector('.payment-method').classList.add('selected');
        });

        // Set active navigation link
        function setActiveNavLink() {
            const currentPage = window.location.pathname.split('/').pop() || 'checkout.html';
            const navLinks = document.querySelectorAll('.nav-links a');
            
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === currentPage) {
                    link.classList.add('active');
                }
            });
        }
 let selectedCategory = null;

        function selectCategory(category) {
            // Remove previous selection
            document.querySelectorAll('.food-category').forEach(cat => {
                cat.classList.remove('selected');
            });
            
            // Add selection to clicked category
            event.currentTarget.classList.add('selected');
            selectedCategory = category;
            
            // Enable continue button
            document.getElementById('continueBtn').disabled = false;
            
            // Store selection
            localStorage.setItem('selectedFoodType', category);
        }

        function continueToSellers() {
            if (!selectedCategory) {
                alert('Please select a food category first');
                return;
            }
            
            // Store the selection and redirect to Sellers page
            localStorage.setItem('selectedFoodType', selectedCategory);
            window.location.href = 'productSellers.html';
        }

        function skipSelection() {
            // Clear any previous selection and go to dashboard
            localStorage.removeItem('selectedFoodType');
            window.location.href = 'buyerDashboard.html';
        }

        // Check if user already has a selection
        document.addEventListener('DOMContentLoaded', function() {
            const existingSelection = localStorage.getItem('selectedFoodType');
            if (existingSelection) {
                // Pre-select the category if user has already chosen
                const categoryElement = document.querySelector(`[onclick="selectCategory('${existingSelection}')"]`);
                if (categoryElement) {
                    categoryElement.classList.add('selected');
                    selectedCategory = existingSelection;
                    document.getElementById('continueBtn').disabled = false;
                }
            }
        });

        // Add keyboard navigation
        document.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' && selectedCategory) {
                continueToSellers();
            }
        });
