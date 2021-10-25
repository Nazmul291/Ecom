
//checkbox
 $('.check_box').click (function(){
    var c_id = $(this).attr("id").toString();
    $.ajax({
        type: 'POST',
        url: '/check_item',
        data:{
            'c_id': c_id,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(item_data){
            if (item_data.option == true){
                var x=document.getElementById(c_id).children[0];
                    x.setAttribute('src', 'static/img/check.svg')
                var y=document.getElementById("sub_total").children[0].children[0];
                    y.innerText = item_data.sub_total.toFixed(1);
                var z=document.getElementById("grand_total").children[0].children[0];
                    z.innerText = item_data.grand_total.toFixed(1);
                var y=document.getElementById("shipping").children[0].children[0];
                    y.innerText = item_data.shipping.toFixed(1);
            } else {
                var x=document.getElementById(c_id).children[0];
                    x.setAttribute('src', 'static/img/uncheck.svg')
                var y=document.getElementById("sub_total").children[0].children[0];
                    y.innerText = item_data.sub_total.toFixed(1);
                var z=document.getElementById("grand_total").children[0].children[0];
                    z.innerText = item_data.grand_total.toFixed(1);
                var y=document.getElementById("shipping").children[0].children[0];
                    y.innerText = item_data.shipping.toFixed(1);
            }
        },
    });
 });

// add to cart function
  $('.addcart').click (function(e){
  e.preventDefault()
    var item_id = $(this).attr("c_id").toString();
    $.ajax({
        type: 'POST',
        url: '/addcart',
        data:{
            'c_id': item_id,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(item_data){

        },
    });
 });

 // remove cart item
  $('.remove_item').click (function(e){
  e.preventDefault()
    var item_id = $(this).attr("c_id").toString();
    console.log(item_id)
    $.ajax({
        type: 'POST',
        url: '/remove_cart',
        data:{
            'c_id': item_id,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(status){
        if (status.value == "success"){
                var rem = document.getElementById(item_id).parentNode.parentNode.parentNode.remove();
                var y=document.getElementById("sub_total").children[0].children[0];
                    y.innerText = status.sub_total.toFixed(1);
                var z=document.getElementById("grand_total").children[0].children[0];
                    z.innerText = status.grand_total.toFixed(1);
                var z=document.getElementById("shipping").children[0].children[0];
                    z.innerText = status.shipping.toFixed(1);
            }
        },
    });
 });

 // increased quantity
  $('.btn-plus').click (function(e){
  e.preventDefault()
    var item_id = $(this).attr("d_id").toString();
    $.ajax({
        type: 'POST',
        url: '/btn_plus',
        data:{
            'c_id': item_id,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(plus_data){
            var x=document.getElementById(item_id).parentNode.parentNode.parentNode.children[3].children[0].children[1];
                x.value = plus_data.quantity
            var y=document.getElementById("sub_total").children[0].children[0];
                y.innerText = plus_data.sub_total.toFixed(1);
            var y=document.getElementById("shipping").children[0].children[0];
                y.innerText = plus_data.shipping.toFixed(1);
            var z=document.getElementById("grand_total").children[0].children[0];
                z.innerText = plus_data.grand_total.toFixed(1);
            var z=document.getElementById(item_id).parentNode.parentNode.parentNode.children[4].children[0];
                z.innerText = plus_data.item_total.toFixed(1);
        },
    });
 });

  // decreased quantity
  $('.btn-minus').click (function(e){
  e.preventDefault()
    var item_id = $(this).attr("m_id").toString();
    $.ajax({
        type: 'POST',
        url: '/btn_minus',
        data:{
            'c_id': item_id,
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val()
        },
        success: function(minus_data){
            var x=document.getElementById(item_id).parentNode.parentNode.parentNode.children[3].children[0].children[1];
                x.value = minus_data.quantity
            var y=document.getElementById("sub_total").children[0].children[0];
                y.innerText = minus_data.sub_total.toFixed(1);
            var z=document.getElementById("grand_total").children[0].children[0];
                z.innerText = minus_data.grand_total.toFixed(1);
            var y=document.getElementById("shipping").children[0].children[0];
                y.innerText = minus_data.shipping.toFixed(1);
            var z=document.getElementById(item_id).parentNode.parentNode.parentNode.children[4].children[0];
                z.innerText = minus_data.item_total.toFixed(1);
        },
    });
 });