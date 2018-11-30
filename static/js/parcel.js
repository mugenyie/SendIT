function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function createOrder(){
    event.preventDefault();

    let placedby = getCookie("id");
    let from = document.getElementById('start').value;
    let to = document.getElementById('end').value;
    let weight = document.getElementById('weight').value;
    let weightmetric = document.getElementById('weightmetric').value;

    document.getElementById("spinner").style.display = 'flex'
    
    fetch('https://sendit-api-columbus.herokuapp.com/api/v1/parcels', {
        method: 'POST',
        headers : {
            "Authorization":getCookie("token")
        },
        body:JSON.stringify({
            from:from, 
            to:to,
            weight:weight,
            weightmetric:weightmetric,
            placedby:placedby
        })
    }).then((res) => res.json())
    .then(
        function (data){
            if(data.error != null){
                document.getElementById("order-error").textContent=data.error;
            }else{
                document.getElementById("order-success").textContent="Delivery Order Received";
                window.location = "orderhistory.html";
            }
            console.log(data)
            document.getElementById("spinner").style.display = 'none'
        }
        )
    .catch(function(err){
        console.log(err)
        document.getElementById("spinner").style.display = 'none'
        document.getElementById("order-error").textContent="An error occured, please try again"
    });
}

function get_user_orders(){

    let userid = getCookie("id");
    let order_list = `
    <tr>
        <th>Order No.</th><th>Date Made</th><th>from</th><th>to</th><th>Current Location</th><th>Status</th>
    </tr>
    `;
    fetch('https://sendit-api-columbus.herokuapp.com/api/v1/users/'+userid+'/parcels', {
        method: 'GET',
        headers : {
            "Authorization":getCookie("token")
        }
    }).then((res) => res.json())
    .then(function(data) {
        data.data.forEach(element => {
            // if(Boolean(element.iscanceled) == true){
            //     edit_link = "Order Canceled";
            // }
            edit_link = element.status == "DELIVERED" ? "" : `
            <a href='user_edit_order.html?order=${element.id}'>Edit Delivery Order</a>`; //if delivered show no edit
            
            order_list += `
            <tr>
                <td>${element.id}</td><td>${element.senton}</td><td>${element.from}</td>
                <td>${element.to}</td><td>${element.currentlocation}</td><td>${element.status}</td>
                <td>${edit_link}</td>
            </tr>
            `
        });
        console.log(data);
        var div = document.getElementById('orders');
        div.innerHTML = order_list;
    })
    .catch(function(error) {
        console.log(error);
    }); 
}

function get_all_orders(){

    let order_list = `
    <tr>
        <th>Order No.</th><th>Date Made</th><th>from</th><th>to</th><th>Current Location</th><th>Status</th><th></th>
    </tr>
    `;
    fetch('https://sendit-api-columbus.herokuapp.com/api/v1/parcels', {
        method: 'GET',
        headers : {
            "Authorization":getCookie("token")
        }
    }).then((res) => res.json())
    .then(function(data) {
        data.data.forEach(element => {
            edit_link = element.status == "DELIVERED" ? "" : `
            <a href='user_edit_order.html?order=${element.id}'>Edit Delivery Order</a>`; //if delivered show no edit
            
            order_list += `
            <tr>
                <td>${element.id}</td><td>${element.senton}</td><td>${element.from}</td>
                <td>${element.to}</td><td>${element.currentlocation}</td><td>${element.status}</td>
                <td>${edit_link}</td>
            </tr>
            `
        });
        console.log(data);
        var div = document.getElementById('order-management');
        div.innerHTML = order_list;
    })
    .catch(function(error) {
        console.log(error);
    }); 
}

