function getOrderIdFromUrl() {
    var params = new URLSearchParams(window.location.search);
    return params.get('order_id');
}

function formatDate(raw) {
    var d = new Date(raw);
    if (isNaN(d.getTime())) return raw;
    return d.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' }) +
        ' ' + d.toLocaleTimeString(undefined, { hour: '2-digit', minute: '2-digit' });
}

$(function () {
    var orderId = getOrderIdFromUrl();
    var sheet = $("#receiptSheet");

    if (!orderId) {
        sheet.html('<p class="receipt-loading">No order specified.</p>');
        return;
    }

    $.get(orderReceiptApiUrl, { order_id: orderId }).done(function (order) {
        var rowsHtml = '';
        var grandTotal = 0;

        $.each(order.items, function (index, item) {
            var qty = parseFloat(item.quantity);
            var actPrice = parseFloat(item.act_price);
            var totalPrice = parseFloat(item.total_price);
            var appliedPrice = qty > 0 ? (totalPrice / qty) : 0;
            grandTotal += totalPrice;

            rowsHtml += '<tr>' +
                '<td>' + item.product_name + '</td>' +
                '<td class="num">' + qty + '</td>' +
                '<td class="num">' + actPrice.toFixed(2) + '</td>' +
                '<td class="num">' + appliedPrice.toFixed(2) + '</td>' +
                '<td class="num">' + totalPrice.toFixed(2) + '</td>' +
                '</tr>';
        });

        var html =
            '<div class="receipt-header">' +
                '<div class="receipt-brand">GSMS</div>' +
                '<div class="receipt-meta">' +
                    '<div>Order #' + orderId + '</div>' +
                '</div>' +
            '</div>' +
            '<div class="receipt-field"><strong>Customer name:</strong> ' + order.customer_name + '</div>' +
            '<div class="receipt-field"><strong>Date of bill:</strong> ' + formatDate(order.datetime) + '</div>' +
            '<table class="receipt-table">' +
                '<thead><tr>' +
                    '<th>Item</th>' +
                    '<th class="num">Net qty</th>' +
                    '<th class="num">Act. price</th>' +
                    '<th class="num">Applied price</th>' +
                    '<th class="num">Total</th>' +
                '</tr></thead>' +
                '<tbody>' + rowsHtml + '</tbody>' +
                '<tfoot><tr class="receipt-total-row">' +
                    '<td colspan="4">Total bill</td>' +
                    '<td class="num">Rs ' + grandTotal.toFixed(2) + '</td>' +
                '</tr></tfoot>' +
            '</table>' +
            '<p class="receipt-footer">Thank you for your business.</p>';

        sheet.html(html);
    }).fail(function () {
        sheet.html('<p class="receipt-loading">Could not load this order.</p>');
    });
});

$("#printButton").on("click", function () {
    window.print();
});