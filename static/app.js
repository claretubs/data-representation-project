document.addEventListener('DOMContentLoaded', function () {
    // Global Variable to store products
    let products = [];

    // Fetch and display products on page load
    function fetchProducts() {
        fetch('/shoes')
            .then(response => response.json())
            .then(data => {
                products = data.shoes;  // Store the fetched products in the global variable
                const productList = document.getElementById('product-list');
                productList.innerHTML = '<h2>Products</h2>';
                data.shoes.forEach(product => {
                    productList.innerHTML += `
                    <div class="product-item">
                        <p>ID: ${product.id}, Name: ${product.Product}, Model: ${product.Model}, Price: ${product.Price}</p>
                        <button class="order-btn" data-id="${product.id}">Order</button>
                        <input type="number" class="quantity-input" id="quantity_${product.id}" placeholder="Quantity" min="1">
                    </div>
                    `;
                });
            })
            .catch(error => console.error('Error fetching products:', error));
    }

    // Fetch and display products on page load
    fetchProducts();

    // Add Product Form Submission
    document.getElementById('add-product-form').addEventListener('submit', function (event) {
        event.preventDefault();

        const productName = document.getElementById('product-name').value;
        const productModel = document.getElementById('product-model').value;
        const productPrice = document.getElementById('product-price').value;

        fetch('/shoes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'Product': productName,
                'Model': productModel,
                'Price': productPrice,
            }),
        })
            .then(response => response.json())
            .then(data => {
                console.log('Product added:', data.shoe);
                fetchProducts(); // Refresh the product list
            })
            .catch(error => console.error('Error adding product:', error));
    });

    // Update Product Form Submission
    document.getElementById('update-product-form').addEventListener('submit', function (event) {
        event.preventDefault();

        const productId = document.getElementById('update-product-id').value;
        const productName = document.getElementById('update-product-name').value;
        const productModel = document.getElementById('update-product-model').value;
        const productPrice = document.getElementById('update-product-price').value;

        fetch(`/shoes/${productId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'Product': productName,
                'Model': productModel,
                'Price': productPrice,
            }),
        })
            .then(response => response.json())
            .then(data => {
                console.log('Product updated:', data.shoe);
                fetchProducts(); // Refresh the product list
            })
            .catch(error => console.error('Error updating product:', error));
    });

    // Delete Product Form Submission
    document.getElementById('delete-product-form').addEventListener('submit', function (event) {
        event.preventDefault();

        const productId = document.getElementById('delete-product-id').value;

        fetch(`/shoes/${productId}`, {
            method: 'DELETE',
        })
            .then(response => response.json())
            .then(data => {
                console.log('Product deleted:', data);
                fetchProducts(); // Refresh the product list
            })
            .catch(error => console.error('Error deleting product:', error));
    });

    // Add event listener for order buttons
    document.getElementById('product-list').addEventListener('click', function (event) {
        if (event.target.classList.contains('order-btn')) {
        // Get product details using the stored product data
        const productId = event.target.getAttribute('data-id');
        const product = products.find(product => product.id === parseInt(productId));
        const productName = product.Product;
        const productPrice = product.Price;

        // Get quantity input value
        const quantityInput = document.getElementById(`quantity_${productId}`);
        const quantity = quantityInput.value ? parseInt(quantityInput.value) : 1;

        // Calculate total price
        const totalPrice = productPrice * quantity;

        // Display total price
        alert(`Product: ${productName}\nQuantity: ${quantity}\nTotal Price: €${totalPrice}`);

        // Send order request to server
        sendOrderRequest(productId, quantity, totalPrice);
    }
  });
});
// Function to send order request
function sendOrderRequest(productId, quantity, totalPrice) {
    // Prepare order data
    const orderData = {
        productId: productId,
        quantity: quantity,
        totalPrice: totalPrice
    };

    // Send order request to the server
    fetch('/orders', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(orderData),
    })
        .then(response => response.json())
        .then(data => {
            console.log('Order Placed:', data.order);
        })
        .catch(error => console.error('Error placing order:', error));
}