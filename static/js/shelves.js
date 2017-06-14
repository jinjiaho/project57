$(function() {
  // if there's no cart object, create one
  if (localStorage.cart === undefined) {
    localStorage.setItem('cart', JSON.stringify([]));
    $('#cartModal .modal-body table').html('There are no items in the cart.');
  }
  else {
    // Get the current cart in array format
    var cartNow = JSON.parse(localStorage.cart);
    // find the length of the cart currently
    var qty = cartNow.length;
    if (qty > 0) {
      // show badge and quantity
      $("#cart-notif").removeClass('hide');
      $("#cart-qty").html(qty);
    }
    
  }

  // When an item is clicked, open a modal with the item information
  $(".openModal").click(function() {
      // find item sku, name and image filename
      var sku = $(this).attr('id');
      var name = $(this).find('div.name').html();
      var img = $(this).find("img").attr('src');

      // insert information into the modal
      $('#qtyForm #modal-input-sku').val(sku);
      $("#qtyForm #modal-picture img").attr('src', img);
      $("#qtyForm #modal-input-name").val(name);
      $("#qtyModal h4").text(name);
  });

  // When the form is submitted, handle it here instead of backend
  $("#qtyForm").on('submit', function(e) {
    e.preventDefault();
    // Get information from modal
    var item_sku = $(this).find($('#modal-input-sku')).val();
    var item_name = $(this).find($("#modal-input-name")).val();
    var item_qty = $(this).find($('#modal-input-qty')).val();
    var item_pic = $("#modal-picture img").attr('src');
    
    // if there is no cart object, create on with the form data
    if (localStorage.cart === undefined) {
      var nextItem = {'sku':item_sku, 
      'name': item_name, 
      'qty': item_qty, 
      'picture': item_pic};
      // stringify the cart for HTML5 storage
      localStorage.setItem('cart', JSON.stringify([nextItem]));
    }
    // Or add it to the current cart
    else {
      // get the cart in array format
      var thisCart = JSON.parse(localStorage.cart);
      for (i=0; i<thisCart.length; i++) {
        // boolean to see if item has already been added to cart
        var inCart; 
        if (thisCart[i].name == item_name) {
          inCart = true;
          // update quantity for the item
          thisCart[i].qty = thisCart[i].qty + item_qty;
          localStorage.setItem('cart', JSON.stringify(thisCart));
        }
      }
      // if item has not been added to the cart
      if (!inCart) {
        // add to cart
        thisCart.push(nextItem);
        // stringify
        localStorage.setItem('cart', JSON.stringify(thisCart));
      }
    }
    localStorage.clear();

    $('#cartModal table tbody').html('');
    // for (i=0; i<cart.length; i++) {
    //   var row = '';
    //   row += '<tr class="cart_item" id="'+i+'"><td><input type="hidden" name="item_' + i + '" value="' + cart[i].name + '"/><img src="' + cart[i].picture + '"/></td><td><input type="number" name="qty_' + i + '" value="' + cart[i].qty.toString() + '"/></td><td class="remove_row"><a class="remove_item" data-target="#'+i+'">&times;</a></td></tr>';
    //   $('#cartModal table tbody').append(row);
    // }

    $('#qtyModal').hide();
    location.reload();

  });
});