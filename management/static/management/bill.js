console.log(products)
var addedProducts = {};
function select_product(selected_product, quantity){
    product_table = $('#product_table')
       
    if(selected_product.value != 'null'){
     product =  products[selected_product.value];
     if(!product.quantity_remains>0 || quantity>product.quantity_remains) {
        addNotification(`Oops! We have ${products[selected_product.value].quantity_remains} left `, type='danger');
        return;
     }
     total = Number(product.price) * Number(quantity) 
     product_table.append(`<tr> <td>${product.name}</td><td>${product.price} </td>
     <td>${quantity} </td> <td>${total} </td>`);
     addedProducts[product.id] = {
         'total': total,
         'quantity':quantity,
     }
     products[selected_product.value].quantity_remains--;
     addNotification('Product Added Sucessfully');
    }
    else {
        addNotification('Please  Select and Item','danger');
    }
    
}

function addNotification(message, type='success'){
    console.log('called');
    $('.notification').hide();
    
    $('.notification').html('')
    $('.notification').append(`<h4 class="alert alert-${type}">${message}</h4>`)
    $('.notification').show();
    setTimeout(()=>{
        $('.notification').hide();
    },4000);
}


customerNames = {

}
async function find_customer(event){
    $('#names').html('')
    search_string = event.target.value;
    response = await get_names('customer', search_string);
    response.forEach(element => {
       $('#names').append(`<option value="${element.name}">`);
       customerNames[element.name] = element; 
    });
}

var selected_customer = null;

$('#customername').on('input', function(){
    try{
        customer_info = customerNames[$(this).val()]   ;
        $('#phonenumber').val(customer_info['number']);
        $('#address').val(customer_info['address']);
        selected_customer = customer_info['id'];

    }
    catch {
        console.log('Not available')
    }
    
});

$('#customer_info').submit(function(event){
    event.preventDefault();
    form_data =  $('#customer_info').serialize()
    fields = form_data.split('&').map((value)=>{
        return value.split('=')[1];
    });
    try {
        fields.push(customerNames[fields[0]]['id'])
    } catch{
        fields.push(null)
    }
    
    $.post('/add_customer/',{
        'customer_data' : JSON.stringify(fields)
    },(data)=>{
        console.log(data);
        if(data.status == 200 && data.response_text == 'new'){
            addNotification('New User Added');
        } else {
            addNotification('You are a returning customer')
        }
    });
});

async function get_names(type, string){
   response = null
   await $.get(`/get_data/${type}/${string}/`,(data)=>{
        response = data['result'];
    });
   return response
}

generated = false;
$('#generate_menu').click(()=>{
if(!Object.values(addedProducts).length){
    addNotification('Please Add an item to generate bill', 'danger');
    return;
}
    $('#grand_total').remove();  
    addedElement = Object.values(addedProducts)
    grandTotal = 0 
    
    addedElement.forEach((element)=>{
        grandTotal+=element['total']; 
    generated = true;
});
product_table.append(`<tr id="grand_total"> <td>---</td><td>---- </td>
<td>Grand Total</td> <td>${grandTotal}</td>`);
});

$('#confirm_bill').click(()=>{
    if(generated){
        console.log(addedProducts)
        $.post(location.href, {
            'customer_id' : 1,
            'items_bought' : JSON.stringify(addedProducts)
        }, (data)=>{
            console.log(data);
            if(data.status == '200'){
                addNotification('Bill has been sucessfully generated... Redirecting');
                setTimeout(()=>{
                    location_shop = location.href
                    console.log(location_shop.slice(location_shop.length-2))
                    console.log(location.host)
                    window.location.reload()        
                    
                },2000)
            }
            
        } )
    } else {
        addNotification('Please generate the bill first');
    }
})