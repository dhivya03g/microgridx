// ----------------------------
// SENSOR DATA (temporary demo)
// ----------------------------

let solarPower = 280
let batteryLevel = 78
let temperature = 34

// update all matching elements (because IDs repeat in twin view)

document.querySelectorAll("#solar").forEach(el=>{
el.innerText = solarPower + " W"
})

document.querySelectorAll("#battery").forEach(el=>{
el.innerText = batteryLevel + "%"
})

document.querySelectorAll("#esp").forEach(el=>{
el.innerText = "Online"
})

document.querySelectorAll("#temp").forEach(el=>{
el.innerText = temperature + " °C"
})
// ------------------------------------
// GLOBAL VARIABLES (dynamic from backend)
// ------------------------------------

let solarPower = 0
let batteryLevel = 0
let temperature = 0


// ------------------------------------
// FETCH DATA FROM BACKEND (FLASK API)
// ------------------------------------

async function loadDecisionData() {

    try {

        const response = await fetch("http://127.0.0.1:5000/api/data")
        const data = await response.json()

        const energy = data.energy_status
        const decision = data.decision

        // UPDATE VALUES
        solarPower = energy.solar_power
        batteryLevel = energy.battery_level
        temperature = energy.temperature

        // UPDATE UI
        document.querySelectorAll("#solar").forEach(el=>{
            el.innerText = solarPower + " W"
        })

        document.querySelectorAll("#battery").forEach(el=>{
            el.innerText = batteryLevel + "%"
        })

        document.querySelectorAll("#temp").forEach(el=>{
            el.innerText = temperature + " °C"
        })

        document.querySelectorAll("#esp").forEach(el=>{
            el.innerText = "Online"
        })

        // ------------------------------------
        // BATTERY BAR
        // ------------------------------------

        let batteryBar = document.getElementById("battery-level")

        if (batteryBar) {
            batteryBar.style.width = batteryLevel + "%"

            if (batteryLevel > 60) {
                batteryBar.style.background = "lime"
            }
            else if (batteryLevel > 30) {
                batteryBar.style.background = "yellow"
            }
            else {
                batteryBar.style.background = "red"
            }
        }

        // ------------------------------------
        // SYSTEM STATUS
        // ------------------------------------

        let status = document.getElementById("status")

        if(status){
            status.innerText = "Backend Connected"
            status.style.color = "lightgreen"
        }

        // ------------------------------------
        // SYSTEM BADGE
        // ------------------------------------

        let badge = document.getElementById("system_badge")

        if(badge){
            if(batteryLevel > 20){
                badge.innerText = "✔ STATUS: HEALTHY"
                badge.style.background = "#22c55e"
            }
            else{
                badge.innerText = "⚠ STATUS: FAULT"
                badge.style.background = "red"
            }
        }

        // ------------------------------------
        // ALERTS
        // ------------------------------------

        let alerts = document.getElementById("alerts")

        if(alerts){

            alerts.innerHTML = ""

            if(batteryLevel < 20){
                alerts.innerHTML += "<li>⚠ Battery Low</li>"
            }

            alerts.innerHTML += "<li>Solar: " + solarPower + " W</li>"
            alerts.innerHTML += "<li>Temp: " + temperature + " °C</li>"
        }

        // ------------------------------------
        // DECISION DATA
        // ------------------------------------

        document.getElementById("energy_mode").innerText = decision.energy_mode
        document.getElementById("system_health").innerText = data.system_health
        document.getElementById("battery_action").innerText = decision.battery_action

        // ENERGY MODE COLOR

        const energyModeElement = document.getElementById("energy_mode")

        if (decision.energy_mode === "EMERGENCY_MODE") {
            energyModeElement.style.color = "red"
            stopEnergyFlow()
        }
        else if (decision.energy_mode === "ECO_MODE") {
            energyModeElement.style.color = "yellow"
            slowEnergyFlow()
        }
        else {
            energyModeElement.style.color = "lightgreen"
            normalEnergyFlow()
        }

    }
    catch (error) {

        let status = document.getElementById("status")

        if(status){
            status.innerText = "Backend not connected"
            status.style.color = "red"
        }

        console.log(error)
    }
}


// ------------------------------------
// ENERGY FLOW ANIMATION
// ------------------------------------

function normalEnergyFlow() {
    document.querySelectorAll(".arrow").forEach(a=>{
        a.style.animationDuration = "1s"
    })
}

function slowEnergyFlow() {
    document.querySelectorAll(".arrow").forEach(a=>{
        a.style.animationDuration = "2s"
    })
}

function stopEnergyFlow() {
    document.querySelectorAll(".arrow").forEach(a=>{
        a.style.animation = "none"
    })
}


// ------------------------------------
// COMMUNITY MICROGRID DEMO
// ------------------------------------

let houseA = 2.5
let houseB = 1.2
let houseC = 0.8

if(document.getElementById("houseA")){
    document.getElementById("houseA").innerText = houseA + " kW"
}

if(document.getElementById("houseB")){
    document.getElementById("houseB").innerText = houseB + " kW"
}

if(document.getElementById("houseC")){
    document.getElementById("houseC").innerText = houseC + " kW"
}


// ------------------------------------
// CHART.JS GRAPH
// ------------------------------------

const chartCanvas = document.getElementById("energyChart")
let energyChart

if(chartCanvas){

    const ctx = chartCanvas.getContext("2d")

    energyChart = new Chart(ctx,{
        type:"line",
        data:{
            labels:[],
            datasets:[
                {
                    label:"Solar Power (W)",
                    data:[],
                    fill:false
                },
                {
                    label:"Battery Level (%)",
                    data:[],
                    fill:false
                }
            ]
        },
        options:{
            responsive:true
        }
    })
}


// ------------------------------------
// GRAPH UPDATE
// ------------------------------------

function updateGraph(){

    if(!energyChart) return

    let time = new Date().toLocaleTimeString()

    energyChart.data.labels.push(time)
    energyChart.data.datasets[0].data.push(solarPower)
    energyChart.data.datasets[1].data.push(batteryLevel)

    if(energyChart.data.labels.length > 10){
        energyChart.data.labels.shift()
        energyChart.data.datasets[0].data.shift()
        energyChart.data.datasets[1].data.shift()
    }

    energyChart.update()
}


// ------------------------------------
// AUTO REFRESH
// ------------------------------------

setInterval(()=>{
    loadDecisionData()
    updateGraph()
},2000)

loadDecisionData()
updateGraph()

// ----------------------------
// BATTERY INDICATOR BAR
// ----------------------------

let batteryBar = document.getElementById("battery-level")

if (batteryBar) {

batteryBar.style.width = batteryLevel + "%"

if (batteryLevel > 60) {
batteryBar.style.background = "lime"
}
else if (batteryLevel > 30) {
batteryBar.style.background = "yellow"
}
else {
batteryBar.style.background = "red"
}

}


// ----------------------------
// SYSTEM STATUS
// ----------------------------

let status = document.getElementById("status")

if(status){

if (batteryLevel > 20) {

status.innerText = "System Status: Healthy"
status.style.color = "lightgreen"

}
else {

status.innerText = "Battery Fault ⚠"
status.style.color = "red"

}

}


// ----------------------------
// SYSTEM BADGE
// ----------------------------

let badge = document.getElementById("system_badge")

if(badge){

if(batteryLevel > 20){

badge.innerText = "✔ STATUS: HEALTHY"
badge.style.background = "#22c55e"

}
else{

badge.innerText = "⚠ STATUS: FAULT"
badge.style.background = "red"

}

}


// ----------------------------
// ALERTS LOG
// ----------------------------

let alerts = document.getElementById("alerts")

if(alerts){

alerts.innerHTML = ""

if(batteryLevel < 20){
alerts.innerHTML += "<li>⚠ Battery Low</li>"
}

alerts.innerHTML += "<li>Solar output: " + solarPower + " W</li>"
alerts.innerHTML += "<li>Temperature: " + temperature + " °C</li>"

}


// ------------------------------------
// DECISION LAYER DATA (JSON FILE)
// ------------------------------------

async function loadDecisionData() {

try {

const response = await fetch("../data/decision_output.json")
const data = await response.json()

document.getElementById("energy_mode").innerText = data.energy_mode
document.getElementById("system_health").innerText = data.system_health
document.getElementById("battery_action").innerText = data.battery_action
document.getElementById("load_priority").innerText = data.load_priority


// ENERGY MODE COLOR CONTROL

const energyModeElement = document.getElementById("energy_mode")

if (data.energy_mode === "EMERGENCY") {

energyModeElement.style.color = "red"
stopEnergyFlow()

}
else if (data.energy_mode === "ECO") {

energyModeElement.style.color = "yellow"
slowEnergyFlow()

}
else {

energyModeElement.style.color = "lightgreen"
normalEnergyFlow()

}

}
catch (error) {

console.log("Decision layer data not available yet")

}

}


// ------------------------------------
// ENERGY FLOW ANIMATION CONTROL
// ------------------------------------

function normalEnergyFlow() {

document.querySelectorAll(".arrow").forEach(a=>{
a.style.animationDuration = "1s"
})

}

function slowEnergyFlow() {

document.querySelectorAll(".arrow").forEach(a=>{
a.style.animationDuration = "2s"
})

}

function stopEnergyFlow() {

document.querySelectorAll(".arrow").forEach(a=>{
a.style.animation = "none"
})

}


// ------------------------------------
// COMMUNITY MICROGRID DEMO
// ------------------------------------

let houseA = 2.5
let houseB = 1.2
let houseC = 0.8

if(document.getElementById("houseA")){
document.getElementById("houseA").innerText = houseA + " kW"
}

if(document.getElementById("houseB")){
document.getElementById("houseB").innerText = houseB + " kW"
}

if(document.getElementById("houseC")){
document.getElementById("houseC").innerText = houseC + " kW"
}


// ------------------------------------
// ENERGY GRAPH (Chart.js)
// ------------------------------------

const chartCanvas = document.getElementById("energyChart")

let energyChart

if(chartCanvas){

const ctx = chartCanvas.getContext("2d")

energyChart = new Chart(ctx,{
type:"line",

data:{
labels:[],
datasets:[

{
label:"Solar Power (W)",
borderColor:"cyan",
data:[],
fill:false
},

{
label:"Battery Level (%)",
borderColor:"lime",
data:[],
fill:false
}

]
},

options:{
responsive:true,
plugins:{
legend:{
labels:{color:"white"}
}
},
scales:{
x:{
ticks:{color:"white"}
},
y:{
ticks:{color:"white"}
}
}
}

})

}


// update graph every refresh

function updateGraph(){

if(!energyChart) return

let time = new Date().toLocaleTimeString()

energyChart.data.labels.push(time)
energyChart.data.datasets[0].data.push(solarPower)
energyChart.data.datasets[1].data.push(batteryLevel)

if(energyChart.data.labels.length > 10){

energyChart.data.labels.shift()
energyChart.data.datasets[0].data.shift()
energyChart.data.datasets[1].data.shift()

}

energyChart.update()

}


// ------------------------------------
// AUTO REFRESH
// ------------------------------------

setInterval(()=>{
loadDecisionData()
updateGraph()
},2000)

loadDecisionData()
updateGraph()