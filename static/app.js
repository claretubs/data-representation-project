// Global Variable to store products
let products = [];

function fetchProducts() {
    fetch('/shoes')
        .then(response => response.json())
        .then(data => {
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

document.addEventListener('DOMContentLoaded', function () {
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
        const orderButton = event.target.closest('.order-btn');
        if (event.target.classList.contains('order-btn')) {
        // Get product details
        const productId = event.target.getAttribute('data-id');
        const productName = products.find(product => product.id === parseInt(productId)).Product;
        const productPrice = products.find(product => product.id === parseInt(productId)).Price;

        // Get quantity input value
        const quantityInput = document.getElementById(`quantity_${productId}`);
        const quantity = quantityInput.value ? parseInt(quantityInput.value) : 1;

        // Calculate total price
        const totalPrice = productPrice * quantity;

        // Display total price
        alert(`Product: ${productName}\nQuantity: ${quantity}\nTotal Price: $${totalPrice}`);

        // Send order request to server
        sendOrderRequest(productId, productName, quantity, totalPrice);
    }
  });
});