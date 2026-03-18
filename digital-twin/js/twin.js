
let solarPower = 280
let batteryLevel = 78
let temperature = 34

// update dashboard + twin box

document.querySelectorAll("#solar, #solar2").forEach(el=>{
el.innerText = solarPower + " W"
})

document.querySelectorAll("#battery, #battery2").forEach(el=>{
el.innerText = batteryLevel + "%"
})

document.querySelectorAll("#esp, #esp2").forEach(el=>{
el.innerText = "Online"
})

document.querySelectorAll("#temp, #temp2").forEach(el=>{
el.innerText = temperature + " °C"
})


// ----------------------------
// BATTERY INDICATOR BAR
// ----------------------------

let batteryBar = document.getElementById("battery-level")

if(batteryBar){

batteryBar.style.width = batteryLevel + "%"

if(batteryLevel > 60){
batteryBar.style.background = "lime"
}
else if(batteryLevel > 30){
batteryBar.style.background = "yellow"
}
else{
batteryBar.style.background = "red"
}

}


// ----------------------------
// SYSTEM STATUS
// ----------------------------

let status = document.getElementById("status")

if(status){

if(batteryLevel > 20){

status.innerText = "System Status: Healthy"
status.style.color = "lightgreen"

}
else{

status.innerText = "Battery Fault ⚠"
status.style.color = "red"

}

}


// ----------------------------
// STATUS BADGE
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
// ENERGY GRAPH
// ----------------------------

const ctx = document.getElementById("energyChart")

if(ctx){

const energyChart = new Chart(ctx,{

type:"line",

data:{
labels:["1","2","3","4","5"],

datasets:[

{
label:"Solar Power",
data:[220,240,260,280,300],
borderColor:"cyan",
fill:false
},

{
label:"Battery Level",
data:[70,72,75,78,80],
borderColor:"lime",
fill:false
}

]
},

options:{
plugins:{
legend:{
labels:{color:"white"}
}
},
scales:{
x:{ticks:{color:"white"}},
y:{ticks:{color:"white"}}
}
}

})

}