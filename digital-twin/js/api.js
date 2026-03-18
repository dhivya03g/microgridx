async function fetchData(){
const res = await fetch("http://127.0.0.1:5000/api/data")
const data = await res.json()

document.getElementById("solar").innerText = data.energy_status.solar
document.getElementById("battery").innerText = data.energy_status.battery
document.getElementById("temp").innerText = data.energy_status.temperature
document.getElementById("mode").innerText = data.mode

document.getElementById("personality").innerText = data.personality
document.getElementById("future").innerText = data.future_mode
document.getElementById("failure").innerText = data.failure
document.getElementById("carbon").innerText = data.carbon + " kg"

checkAlerts(data)

}

setInterval(fetchData,3000)