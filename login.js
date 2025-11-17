//Set web server url for fetch request

//Pull username and password
const usernameElement = document.getElementById("username");
const passwordElement = document.getElementById("password");

username = usernameElement.value;
password = passwordElement.value;

//SHA256 hash the password

//sign-in-data = {
//	username: $username,
//	password: $password,
// };

//fetch-options = {
//	method: 'POST',
//	headers: {'Content-Type': 'application/json'},
//	credentials: "include",
//	body: JSON.stringify(data)
//};

//fetch(url, options)
//	.then(res => {if(res.redirected){window.location.href = res.url;}});
