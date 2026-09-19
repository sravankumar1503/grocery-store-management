var productPrices = {};

$(function () {
    //Json data by api call for order table
    $.get(productListApiUrl, function (response) {
        productPrices = {}
        if(response) {
            var options = '<option value="">--Select--</option>';
            $.each(response, function(index, product) {
                options += '<option value="'+ product.product_id +'">'+ product.name +'</option>';
                productPrices[product.product_id] = product.price_per_unit;
            });
            $(".product-box").find("select").empty().html(options);
        }
    });
});

$("#addMoreButton").click(function () {
    var row = $(".product-box").html();
    $(".product-box-extra").append(row);
    $(".product-box-extra .remove-row").last().removeClass('hideit');
    $(".product-box-extra .product-price").last().text('0.0');
    $(".product-box-extra .product-qty").last().val('1');
    $(".product-box-extra .product-total").last().text('0.0');
});

$(document).on("click", ".remove-row", function (){
    $(this).closest('.row').remove();
    updateGrandTotal();
});

$(document).on("change", ".cart-product", function (){
    var product_id = $(this).val();
    var price = productPrices[product_id];

    $(this).closest('.row').find('#product_price').val(price);
    calculateValue();
});

$(document).on("change", ".product-qty", function (e){
    calculateValue();
});

$(document).on("change", ".product-qty", function (e){
    calculateValue();
});

// Bug fix: when the item total is edited by hand, don't recompute it from qty*price -
// just re-sum all item totals into the grand total so the manual edit is reflected there too.
$(document).on("input change", ".product-total", function (e){
    updateGrandTotal();
});

$(document).on("change", ".product-qty", function (e){
    calculateValue();
});

// Validation: customer name, at least one line item, a product selected per row,
// and a positive quantity per row.
function validateOrder() {
    var errors = [];

    var customerName = $("#customerName").val();
    if (!customerName || !customerName.trim()) {
        errors.push("Customer name is required.");
    }

    var rows = $(".product-box-extra .product-item");
    if (rows.length === 0) {
        errors.push("Please add at least one item to the order.");
    }

    rows.each(function (index) {
        var row = $(this);
        var productId = row.find('.cart-product').val();
        var qty = row.find('.product-qty').val();

        if (!productId) {
            errors.push("Item " + (index + 1) + ": please select a product.");
        }
        if (qty === '' || qty === null || isNaN(parseFloat(qty)) || parseFloat(qty) <= 0) {
            errors.push("Item " + (index + 1) + ": please enter a valid quantity.");
        }
    });

    return errors;
}

function showOrderErrors(errors) {
    var errorBox = $("#orderFormErrors");
    if (errors.length === 0) {
        errorBox.hide().empty();
        return;
    }
    var html = '<ul class="mb-0">';
    $.each(errors, function (index, message) {
        html += '<li>' + message + '</li>';
    });
    html += '</ul>';
    errorBox.html(html).show();
}

$("#saveOrder").on("click", function(){
    var errors = validateOrder();
    if (errors.length > 0) {
        showOrderErrors(errors);
        return;
    }
    showOrderErrors([]);

    var formData = $("form").serializeArray();
    var requestPayload = {
        customer_name: null,
        total: null,
        order_details: []
    };
    var orderDetails = [];
    for(var i=0;i<formData.length;++i) {
        var element = formData[i];
        var lastElement = null;

        switch(element.name) {
            case 'customerName':
                requestPayload.customer_name = element.value;
                break;
            case 'product_grand_total':
                requestPayload.total = element.value;
                break;
            case 'product':
                requestPayload.order_details.push({
                    product_id: element.value,
                    quantity: null,
                    total_price: null
                });                
                break;
            case 'qty':
                lastElement = requestPayload.order_details[requestPayload.order_details.length-1];
                lastElement.quantity = element.value
                break;
            case 'item_total':
                lastElement = requestPayload.order_details[requestPayload.order_details.length-1];
                lastElement.total_price = element.value
                break;
        }

    }
    callApi("POST", orderSaveApiUrl, {
        'data': JSON.stringify(requestPayload)
    });
});