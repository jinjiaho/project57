function updateCart() {
  console.log('updating cart...');
  // if there's no cart object, create one
  if (localStorage.cart === undefined) {
    $('#cartModal .modal-body table').html('There are no items in the cart.');
  }
  else {
    console.log(localStorage.cart);
    // Get the current cart in array format
    var cartNow = JSON.parse(localStorage.cart);
    // find the length of the cart currently
    var qty = cartNow.length;
    if (qty > 0) {
      // show badge and quantity
      $("#cart-notif").removeClass('hide');
      $("#cart-qty").html(qty);

      var cartTable = $('#cartModal table tbody')
      cartTable.html('');
      for (item of cartNow) {
        item.qty = parseInt(item.qty);
        cartTable.append('<tr class="cart_item" id="'
            + item.iid + '"><td><img src="' 
            + item.picture + '"/></td><td>' + item.name + '</td><td><input type="number" name="' 
            + item.iid + '" value="' + item.qty + '" class="num-input" />' 
            + item.action + '<input type="hidden" name="' + item.iid + '" value="'
            + item.action +'" /></td><td style="display:none;"><input type="text" name="'
            + item.iid + '" value="'
            + item.tag + '"/></td>'
            + '<td><a onclick="deleteRow(this)" href="javascript:void(0);">&times;</a></td></tr>');
        $('#'+item.iid+' option[value="'+item.action+'"]').attr('selected', 'selected');
      }
    }
  }
  // localStorage.clear();
}

function clearCartSubmit() {
  localStorage.setItem('cart', JSON.stringify([]));
  document.getElementById('cartForm').submit();
}

function deleteRow(r) {
  // delete from table form
  var row = r.parentNode.parentNode.rowIndex;
  document.getElementById('cart-table').deleteRow(row);

  // delete from cart
  var cart = JSON.parse(localStorage.cart);
  cart.splice(row-1, 1);
  localStorage.setItem('cart', JSON.stringify(cart));

  updateCart();
}

$(function () {
  updateCart();

  // When an item is clicked, open a modal with the item information
  $(".openModal").click(function() {
      // find item iid, name and image filename
      var iid = $(this).attr('id');
      var name = $(this).find('div.name').html();
      var img = $(this).find("img").attr('src');

      // insert information into the modal
      $('#qtyForm #modal-input-iid').val(iid);
      $("#qtyForm #modal-picture img").attr('src', img);
      $("#qtyForm #modal-input-name").val(name);
      $("#qtyModal h4").text(name);
  });

  // // Function to prevent negative number input
  // $(function() {
  //     var numbers = $("#stockUpdateForm .num-input");
  //     $.each(numbers, function(index, value){
  //       numbers[index].onkeydown = function(e) {
  //         if(!((e.keyCode > 95 && e.keyCode < 106)
  //           || (e.keyCode > 47 && e.keyCode < 58) 
  //           || e.keyCode == 8)) {
  //             return false;
  //         }
  //       }
  //     })
  // })

  // When the form is submitted, handle it here instead of backend
  $("#qtyForm").on('submit', function(e) {
    e.preventDefault();
    // reset localStorage. Use if localStorage is messed up.
    // localStorage.clear();
    // Get information from modal
    var role = $(this).data('role');
    var item_id = $(this).find($('#modal-input-iid')).val();
    var item_name = $(this).find($("#modal-input-name")).val();
    var item_qty = parseInt($(this).find($('#modal-input-qty')).val());
    var item_pic = $("#modal-picture img").attr('src');
    var tag_id = window.location.pathname.split("/")[3];
    var action = $(this).find($("input[name='action']:checked")).val();
    console.log(item_id + ", " + item_name + ", " + item_qty + ", " + item_pic);
    
    // if there is no cart object, create one with the form data
    if (localStorage.cart === undefined) {
      console.log('no cart, creating new');

      // stringify the cart for HTML5 storage
      localStorage.setItem('cart', JSON.stringify([{'iid':item_id, 'name': item_name, 'qty': item_qty, 'picture': item_pic, 'action': action, 'tag': tag_id}]));
    }
    // Or add it to the current cart
    else {
      // get the cart in array format
      var thisCart = JSON.parse(localStorage.cart);
      console.log(typeof(thisCart));
      // boolean to see if item has already been added to cart
      var inCart = false; 
      var newCart = thisCart.map(function(i) {
        if (i.name === item_name && i.action === action) {
          inCart = true;
          // update quantity for the item
          i.qty = i.qty + item_qty;
          localStorage.setItem('cart', JSON.stringify(thisCart));

        }
      });
      // if item has not been added to the cart
      if (inCart === false) {
        // add to cart
        thisCart.push({'iid':item_id, 'name': item_name, 'qty': item_qty, 'picture': item_pic, 'action': action, 'tag': tag_id});
        // console.log(JSON.stringify({'iid':item_iid, 'name': item_name, 'qty': item_qty, 'picture': item_pic}));
        // stringify
        localStorage.setItem('cart', JSON.stringify(thisCart));
      }
    }

    updateCart();
    $('#qtyModal').modal('hide');

  });

});

