// Define your api here
var productListApiUrl = 'https://grocery-store-management-1qh4.onrender.com/getProducts';
var uomListApiUrl = 'https://grocery-store-management-1qh4.onrender.com/getUOM';
var uomSaveApiUrl = 'https://grocery-store-management-1qh4.onrender.com/insertUOM';
var productSaveApiUrl = 'https://grocery-store-management-1qh4.onrender.com/insertProduct';
var productUpdateApiUrl = 'https://grocery-store-management-1qh4.onrender.com/updateProduct';
var productDeleteApiUrl = 'https://grocery-store-management-1qh4.onrender.com/deleteProduct';
var orderListApiUrl = 'https://grocery-store-management-1qh4.onrender.com/getAllOrders';
var orderSaveApiUrl = 'https://grocery-store-management-1qh4.onrender.com/insertOrder';
var orderDetailsApiUrl = 'https://grocery-store-management-1qh4.onrender.com/getOrderDetails';
// For product drop in order
var productsApiUrl = 'https://fakestoreapi.com/products';

function callApi(method, url, data) {
    $.ajax({
        method: method,
        url: url,
        data: data
    }).done(function( msg ) {
        window.location.reload();
    });
}

// Recalculates each line item's total (qty * price) and then refreshes the grand total.
// Used whenever qty or the selected product changes.
function calculateValue() {
    $(".product-item").each(function( index ) {
        var qty = parseFloat($(this).find('.product-qty').val());
        var price = parseFloat($(this).find('#product_price').val());
        price = price*qty;
        $(this).find('#item_total').val(price.toFixed(2));
    });
    updateGrandTotal();
}

// Sums up whatever is currently in each line item's total field (without recomputing
// them from qty/price) and writes it to the grand total. This lets a manually edited
// item total still be reflected in the grand total.
function updateGrandTotal() {
    var total = 0;
    $(".product-item").each(function( index ) {
        var itemTotal = parseFloat($(this).find('.product-total').val());
        if (!isNaN(itemTotal)) {
            total += itemTotal;
        }
    });
    $("#product_grand_total").val(total.toFixed(2));
}

function orderParser(order) {
    return {
        id : order.id,
        date : order.employee_name,
        orderNo : order.employee_name,
        customerName : order.employee_name,
        cost : parseInt(order.employee_salary)
    }
}

function productParser(product) {
    return {
        id : product.id,
        name : product.employee_name,
        unit : product.employee_name,
        price : product.employee_name
    }
}

function productDropParser(product) {
    return {
        id : product.id,
        name : product.title
    }
}

//To enable bootstrap tooltip globally
// $(function () {
//     $('[data-toggle="tooltip"]').tooltip()
// });