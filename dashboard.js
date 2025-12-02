const profilePic = document.getElementById("profilePic");
const dropdown = document.getElementById("dropdownMenu");

function hasCookie(name) {
    return document.cookie.split("; ").some(row => row.startsWith(name + "="));
}
//if (!hasCookie("sharktowels_auth_token")) {
//    window.location.href = "/Login.html";
//}

profilePic.addEventListener("click", () => {
    dropdown.style.display = dropdown.style.display === "block" ? "none" : "block";
});

document.addEventListener("click", (e) => {
    if (!profilePic.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.style.display = "none";
    }
});

url = "/api/tables"

const token = "sharktowels_auth_token";

fetchOptions = {
	method: 'POST',
	headers: {'Content-Type': 'application/json'},
	credentials: "include",
	body: JSON.stringify("some data")
}

fetch(url, fetchOptions)
	.then(res => res.json())
	.then(figs => {
		const fig1 = JSON.parse(figs.plot1);
		const fig2 = JSON.parse(figs.plot2); 
		const fig3 = JSON.parse(figs.plot3);
		const fig4 = JSON.parse(figs.plot4);

		Plotly.newPlot("graphDiv1", fig1.data, fig1.layout);
		Plotly.newPlot("graphDiv2", fig2.data, fig2.layout);
		Plotly.newPlot("graphDiv3", fig3.data, fig3.layout);
		Plotly.newPlot("graphDiv4", fig4.data, fig4.layout);
	});

