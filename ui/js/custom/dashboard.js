$(function () {
    //Json data by api call for order table
    $.get(orderListApiUrl, function (response) {
        if(response) {
            var table = '';
            var totalCost = 0;
            $.each(response, function(index, order) {
            var orderTotal = parseFloat(order.total);
            totalCost += orderTotal;
            table += '<tr>' +
                '<td>'+ order.datetime +'</td>'+
                '<td>'+ order.order_id +'</td>'+
                '<td>'+ order.customer_name +'</td>'+
                '<td>'+ orderTotal.toFixed(2) +' Rs</td>'+
                '<td><span class="btn btn-xs btn-primary view-order" data-id="'+ order.order_id +'">View</span></td>'+
                '<span class="btn btn-xs btn-secondary print-order" data-id="'+ order.order_id +'">Print</span>'+
                '</tr>';
        });
            table += '<tr><td colspan="3" style="text-align: end"><b>Total</b></td><td><b>'+ totalCost.toFixed(2) +' Rs</b></td><td></td></tr>';
            $("table").find('tbody').empty().html(table);
        }
    });
});

// View order details: fetch the individual line items for this order and render them in the modal.
$(document).on("click", ".view-order", function () {
    var orderId = $(this).data('id');
    var modalBody = $("#orderDetailsModalBody");

    modalBody.html('<img src="https://demo.test.cloint.com/assets/images/spinner.gif" width="40" style="margin: 60px auto;" alt="">');
    $("#myModal").modal('show');

    $(document).on("click", ".print-order", function () {
        var orderId = $(this).data('id');
        window.open('receipt.html?order_id=' + orderId, '_blank');
    });
    
    $.get(orderDetailsApiUrl, { order_id: orderId }, function (response) {
        var table = '<table class="table table-bordered text-left">' +
            '<thead><th>Product</th><th>Quantity</th><th>Total Price</th></thead><tbody>';
        var grandTotal = 0;
        $.each(response, function (index, item) {
            var totalPrice = parseFloat(item.total_price);
            grandTotal += totalPrice;
            table += '<tr>' +
                '<td>'+ item.product_name +'</td>'+
                '<td>'+ item.quantity +'</td>'+
                '<td>'+ totalPrice.toFixed(2) +' Rs</td></tr>';
        });
        table += '<tr><td colspan="2" style="text-align: end"><b>Total</b></td><td><b>'+ grandTotal.toFixed(2) +' Rs</b></td></tr>';
        table += '</tbody></table>';
        modalBody.html(table);
    });
});