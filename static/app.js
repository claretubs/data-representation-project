function fetchProducts() {
    fetch('/shoes')
        .then(response => response.json())
        .then(data => {
            const productList = document.getElementById('product-list');
            productList.innerHTML = '<h2>Products</h2>';
            data.shoes.forEach(product => {
                productList.innerHTML += `
                    <p>ID: ${product.id}, Name: ${product.Product}, Model: ${product.Model}, Price: ${product.Price}</p>
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
});