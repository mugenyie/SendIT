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
            }
            console.log(data)
            document.getElementById("spinner").style.display = 'none'
        }
        )
    .catch(function(err){
        console.log(err)
        console.log(getCookie("id"))
        console.log(getCookie("token"))
        document.getElementById("spinner").style.display = 'none'
        document.getElementById("order-error").textContent="An error occured, please try again"
    });
}


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