function postLoginData(){
    event.preventDefault();

    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;

    document.getElementById("spinner").style.display = 'flex'

    fetch('https://sendit-api-columbus.herokuapp.com/api/v1/auth/login', {
        method: 'POST',
        headers : new Headers(),
        body:JSON.stringify({
            username:username, 
            password:password
        })
    }).then((res) => res.json())
    .then(
        function (data){
            setCookie('token', data.data[0].token, 30)
            setCookie('username', data.data[0].user.username, 30),
            setCookie('email', data.data[0].user.email, 30),
            setCookie('firstname', data.data[0].user.firstname, 30),
            setCookie('lastname', data.data[0].user.lastname, 30),
            setCookie('othernames', data.data[0].user.othernames, 30),
            setCookie('isadmin', data.data[0].user.isadmin, 30)
            document.getElementById("spinner").style.display = 'none'
            window.location.href = "home.html"
        }
        )
    .catch(function(err){
        console.log(err)
        document.getElementById("spinner").style.display = 'none'
        document.getElementById("login-notice").textContent="Wrong username or password !!"
    });
}

function postRegisterData(event){
    event.preventDefault();

    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;

    fetch('https://sendit-api-columbus.herokuapp.com/api/v1/auth/login', {
        method: 'POST',
        headers : new Headers(),
        body:JSON.stringify({
            username:username, 
            password:password
        })
    }).then((res) => res.json())
    .then(
        // setCookie('user', data.),
        (data) =>  console.log(data)
        )
    .catch((err)=>console.log(err))
}


function setCookie(cname,cvalue,exmins) {
    var d = new Date();
    d.setTime(d.getTime() + (exmins*60*1000));
    var expires = "expires=" + d.toGMTString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
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

function checkToken() {
    var token=getCookie("token");
    if (token == "") {
        alert("Login to continue")
        window.location.replace('index.html');
    }
}

function logOut()
{   
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++)
    {   
        var spcook =  cookies[i].split("=");
        deleteCookie(spcook[0]);
    }
    function deleteCookie(cookiename)
    {
        var d = new Date();
        d.setDate(d.getDate() - 1);
        var expires = ";expires="+d;
        var name=cookiename;
        //alert(name);
        var value="";
        document.cookie = name + "=" + value + expires + "; path=/acc/html";                    
    }
    window.location = "index.html"; 
}
