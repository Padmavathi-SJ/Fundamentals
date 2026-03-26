const apiKey="0419e516b631c8d506781065a34b6de7";

async function getWeather() {
    const city = document.getElementById("cityInput").value;
    const resultDiv = document.getElementById("weatherResult");

    if(city === "") {
        resultDiv.innerHTML = "Please enter a city name";
        return;
    }

    const url = `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${apiKey}&units=metric`;

    try {
        const response = await fetch(url);

        if(!response.ok) {
            throw new Error("City not found");
        }

        const data = await response.json();

        //Extract data
        const temp=data.main.temp;
        const humidity=data.main.humidity;
        const condition=data.weather[0].description;

        //update UI
        resultDiv.innerHTML =`
        <p><strong>City: </strong>${data.name}</p>
        <p><strong>Temperature: </strong>${temp} °C</p>
        <p><strong>Humidity: </strong>${humidity}%</p>
        <p><strong>Condition: </strong>${condition}</p>
        `;
    }
    catch(error) {
        resultDiv.innerHTML = "Error: " + error.message;
    }
}