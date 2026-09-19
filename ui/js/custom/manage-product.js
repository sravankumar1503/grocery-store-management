var productModal = $("#productModal");
    $(function () {

        //JSON data by API call
        $.get(productListApiUrl, function (response) {
            if(response) {
                var table = '';
                $.each(response, function(index, product) {
                    table += '<tr data-id="'+ product.product_id +'" data-name="'+ product.name +'" data-unit="'+ product.uom_id +'" data-price="'+ product.price_per_unit +'">' +
                        '<td>'+ product.name +'</td>'+
                        '<td>'+ product.uom_name +'</td>'+
                        '<td>'+ product.price_per_unit +'</td>'+
                        '<td>'+
                        '<span class="btn btn-xs btn-primary edit-product">Edit</span> '+
                        '<span class="btn btn-xs btn-danger delete-product">Delete</span>'+
                        '</td></tr>';
                });
                $("table").find('tbody').empty().html(table);
            }
        });
    });

        // Save Product - handles both "Add New Product" (id == 0) and "Edit Product" (id != 0)
    $("#saveProduct").on("click", function () {
        var data = $("#productForm").serializeArray();
        var requestPayload = {
            product_id: null,
            product_name: null,
            uom_id: null,
            price_per_unit: null
        };
        for (var i=0;i<data.length;++i) {
            var element = data[i];
            switch(element.name) {
                case 'id':
                    requestPayload.product_id = element.value;
                    break;
                case 'name':
                    requestPayload.product_name = element.value;
                    break;
                case 'uoms':
                    requestPayload.uom_id = element.value;
                    break;
                case 'price':
                    requestPayload.price_per_unit = element.value;
                    break;
            }
        }

        if (requestPayload.product_id && requestPayload.product_id !== '0') {
            callApi("POST", productUpdateApiUrl, {
                'data': JSON.stringify(requestPayload)
            });
        } else {
            callApi("POST", productSaveApiUrl, {
                'data': JSON.stringify(requestPayload)
            });
        }
    });

    $(document).on("click", ".delete-product", function (){
        var tr = $(this).closest('tr');
        var data = {
            product_id : tr.data('id')
        };
        var isDelete = confirm("Are you sure to delete "+ tr.data('name') +" item?");
        if (isDelete) {
            callApi("POST", productDeleteApiUrl, data);
        }
    });

    

    productModal.on('hide.bs.modal', function(){
        $("#id").val('0');
        $("#name, #unit, #price").val('');
        productModal.find('.modal-title').text('Add New Product');
    });

        // Edit Product: populate the shared modal/form with this row's data, load the UOM list,
    // pre-select the product's current unit, then open the modal.
    $(document).on("click", ".edit-product", function (){
        var tr = $(this).closest('tr');
        var productId = tr.data('id');
        var productName = tr.data('name');
        var uomId = tr.data('unit');
        var price = tr.data('price');

        productModal.find('.modal-title').text('Edit Product');
        $("#id").val(productId);
        $("#name").val(productName);
        $("#price").val(price);

        $.get(uomListApiUrl, function (response) {
            if(response) {
                var options = '<option value="">--Select--</option>';
                $.each(response, function(index, uom) {
                    options += '<option value="'+ uom.uom_id +'">'+ uom.uom_name +'</option>';
                });
                $("#uoms").empty().html(options);
                $("#uoms").val(uomId);
            }
            productModal.modal('show');
        });
    });

    productModal.on('hide.bs.modal', function(){
        $("#id").val('0');
        $("#name, #price").val('');
        $("#uoms").val('');
        productModal.find('.modal-title').text('Add New Product');
    });

    
    var uomModal = $("#uomModal");

    // Add New UOM
    $("#saveUOM").on("click", function () {
        var uomName = $("#uom_name").val();
        if (!uomName || !uomName.trim()) {
            alert("Please enter a UOM name.");
            return;
        }
        callApi("POST", uomSaveApiUrl, {
            'data': JSON.stringify({ uom_name: uomName.trim() })
        });
    });

    uomModal.on('hide.bs.modal', function(){
        $("#uom_name").val('');
    });

    productModal.on('show.bs.modal', function(){
        // "Add New Product" opens the modal with id still 0, so load a fresh, unselected
        // UOM list here. When editing, #id is already set before .modal('show') is called
        // above, and the handler above already populated + selected the UOM list, so skip
        // reloading here to avoid wiping out the selection.
        if ($("#id").val() === '0') {
            $.get(uomListApiUrl, function (response) {
                if(response) {
                    var options = '<option value="">--Select--</option>';
                    $.each(response, function(index, uom) {
                        options += '<option value="'+ uom.uom_id +'">'+ uom.uom_name +'</option>';
                    });
                    $("#uoms").empty().html(options);
                }
            });
        }
    });