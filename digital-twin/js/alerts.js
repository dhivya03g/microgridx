function checkAlerts(data){

if(data.energy_status.battery < 30){
showAlert("⚠ Low Battery")
}

if(data.failure === "HIGH"){
showAlert("❌ Failure Risk High")
}

if(data.loss === "Energy Loss"){
showAlert("⚡ Energy Loss Detected")
}

}

function showAlert(msg){
let div = document.createElement("div")
div.innerText = msg
div.className = "alert"
document.body.appendChild(div)

setTimeout(()=>div.remove(),3000)
}