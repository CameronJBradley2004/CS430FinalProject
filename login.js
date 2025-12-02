const form = document.getElementById("loginForm");

form.addEventListener("submit", (e) => {
  e.preventDefault();
  //Set web server url for fetch request

//Pull username and password
const usernameElement = document.getElementById("username");
const passwordElement = document.getElementById("password");

//Set the values
username = usernameElement.value;
password = passwordElement.value;

//Create the json
loginData = {
	username: username,
	password: password,
 };
 
//Set the url
url = "/api/login"

//Set the options 
fetchOptions = {
	method: 'POST',
	headers: {'Content-Type': 'application/json'},
	credentials: "include",
	body: JSON.stringify(loginData)
};

//Do the fetch
//fetch(url, options)
//	.then(res => {if(res.redirected){window.location.href = res.url;}});

fetch(url, fetchOptions)
	.then(r => r.json())
	.then(() => {window.location.href = "/CS430Dashboard.html";});
});
