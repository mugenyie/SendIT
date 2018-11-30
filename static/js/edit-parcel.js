document.getElementById("cancel-delivery").addEventListener("click", cancelOrder);
document.getElementById("change-destination").addEventListener("click", changeDestination);
document.getElementById("change-status").addEventListener("click", changeStatus);
document.getElementById("change-currentLocation").addEventListener("click", changeCurrentLocation);

let parcelId = findGetParameter("order");

function cancelOrder(){
    document.getElementById("spinner").style.display = 'flex';

    fetch(`https://sendit-api-columbus.herokuapp.com/api/v1/parcels/${parcelId}/cancel`, {
        method: 'PATCH',
        headers : {
            "Authorization":getCookie("token")
        }
    }).then((res) => res.json())
    .then(
        function (data){
            if(data.error != null){
                document.getElementById("edit-error").textContent=data.error;
            }else{
                document.getElementById("edit-success").textContent="Delivery Order Canceled";
            }
            console.log(data)
            document.getElementById("spinner").style.display = 'none'
        }
        )
    .catch(function(err){
        console.log(err)
        document.getElementById("spinner").style.display = 'none'
        document.getElementById("edit-error").textContent="An error occured, please try again"
    });
}

function changeDestination(){
    let destination = document.getElementById("autocomplete").value;
    document.getElementById("spinner").style.display = 'flex';

    fetch(`https://sendit-api-columbus.herokuapp.com/api/v1/parcels/${parcelId}/destination`, {
        method: 'PATCH',
        headers : {
            "Authorization":getCookie("token")
        },
        body:JSON.stringify({
            to:destination
        })
    }).then((res) => res.json())
    .then(
        function (data){
            if(data.error != null){
                document.getElementById("edit-error").textContent=data.error;
            }else{
                document.getElementById("edit-success").textContent="Order: "+parcelId+" Delivery Destination Changed to "+destination;
            }
            console.log(data)
            document.getElementById("spinner").style.display = 'none'
        }
        )
    .catch(function(err){
        console.log(err)
        document.getElementById("spinner").style.display = 'none'
        document.getElementById("edit-error").textContent="An error occured, please try again"
    });
}

function changeCurrentLocation(){
    let currentlocation = document.getElementById("autocomplete").value;
    document.getElementById("spinner").style.display = 'flex';
    let userid = getCookie("id");

    fetch(`https://sendit-api-columbus.herokuapp.com/api/v1/parcels/${parcelId}/currentlocation`, {
        method: 'PATCH',
        headers : {
            "Authorization":getCookie("token")
        },
        body:JSON.stringify({
            userId: userid,
            currentlocation: currentlocation
        })
    }).then((res) => res.json())
    .then(
        function (data){
            if(data.error != null){
                document.getElementById("edit-error").textContent=data.error;
            }else{
                document.getElementById("edit-success").textContent="Order: "+parcelId+" Current Location Changed to "+currentlocation;
            }
            console.log(data)
            document.getElementById("spinner").style.display = 'none'
        }
        )
    .catch(function(err){
        console.log(err)
        document.getElementById("spinner").style.display = 'none'
        document.getElementById("edit-error").textContent="An error occured, please try again"
    });
}

function changeStatus(){
    let status = document.getElementById("status").value;
    document.getElementById("spinner").style.display = 'flex';
console.log(status);
    fetch(`https://sendit-api-columbus.herokuapp.com/api/v1/parcels/${parcelId}/status`, {
        method: 'PATCH',
        headers : {
            "Authorization":getCookie("token")
        },
        body:JSON.stringify({
            userId: getCookie("id"),
            status: status
        })
    }).then((res) => res.json())
    .then(
        function (data){
            if(data.error != null){
                document.getElementById("edit-error").textContent=data.error;
            }else{
                document.getElementById("edit-success").textContent="Order: "+parcelId+" Status Changed to "+status;
            }
            console.log(data)
            document.getElementById("spinner").style.display = 'none'
        }
        )
    .catch(function(err){
        console.log(err)
        document.getElementById("spinner").style.display = 'none'
        document.getElementById("edit-error").textContent="An error occured, please try again"
    });
}

function findGetParameter(parameterName) {
    var result = null,
        tmp = [];
    var items = location.search.substr(1).split("&");
    for (var index = 0; index < items.length; index++) {
        tmp = items[index].split("=");
        if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
    }
    return result;
}