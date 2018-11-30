document.getElementById("cancel-delivery").addEventListener("click", cancelOrder);
document.getElementById("change-destination").addEventListener("click", changeDestination);
let parcelId = findGetParameter("order");
let destination = document.getElementById("destination").value;

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
    
    console.log(destination);
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