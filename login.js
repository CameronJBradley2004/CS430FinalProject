//Set web server url for fetch request

//Pull username and password
const usernameElement = document.getElementById("username");
const passwordElement = document.getElementById("password");

//Set the values
username = usernameElement.value;
password = passwordElement.value;

//Create the json
loginData = {
	username: $username,
	password: $password,
 };
 
//Set the url
url = "/api/process"

//Set the options 
fetch-options = {
	method: 'POST',
	headers: {'Content-Type': 'application/json'},
	credentials: "include",
	body: JSON.stringify(loginData)
};

//Do the fetch
//fetch(url, options)
//	.then(res => {if(res.redirected){window.location.href = res.url;}});

fetch(url, options)
	.then(r => r.json())
	.then(data => console.log(data))
