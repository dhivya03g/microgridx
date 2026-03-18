// ------------------------------------
// BACKEND API INTEGRATION (COMMUNITY LAYER)
// ------------------------------------

async function loadBackendData() {

    try {

        // Solar Prediction
        const solarRes = await fetch("http://127.0.0.1:5000/predict-solar")
        const solarData = await solarRes.json()

        // Battery Status
        const batteryRes = await fetch("http://127.0.0.1:5000/battery-status")
        const batteryData = await batteryRes.json()

        // Energy Matching
        const energyRes = await fetch("http://127.0.0.1:5000/energy-match")
        const energyData = await energyRes.json()

        // Update UI (override demo values)

        document.querySelectorAll("#solar").forEach(el=>{
            el.innerText = solarData.predicted + " W"
        })

        document.querySelectorAll("#battery").forEach(el=>{
            el.innerText = batteryData.level + "%"
        })

        // Update system status based on real battery
        let status = document.getElementById("status")
        if(status){
            if (batteryData.level > 20) {
                status.innerText = "System Status: Healthy"
                status.style.color = "lightgreen"
            } else {
                status.innerText = "Battery Fault ⚠"
                status.style.color = "red"
            }
        }

        console.log("Energy Transfers:", energyData)

    } catch (error) {

        console.log("Backend not connected yet")

    }

}


// ------------------------------------
// AUTO REFRESH BACKEND DATA
// ------------------------------------

setInterval(()=>{
    loadBackendData()
},3000)

// First call
loadBackendData()

// ----------------------------
// LOAD HOUSES (FIXED)
// ----------------------------

async function loadHouses(){

    try{

        const res = await fetch("http://127.0.0.1:5000/houses")
        const data = await res.json()

        let container = document.getElementById("houses")

        if(container){

            container.innerHTML = ""

            data.forEach(h => {
                container.innerHTML += `
                <div class="box">${h.house_id}</div>
                `
            })
        }

    }catch(err){
        console.log("Error loading houses")
    }

}

// ----------------------------
// ADD HOUSE (FIXED)
// ----------------------------

async function addHouse(){

    try{

        await fetch("http://127.0.0.1:5000/add-house",{
            method:"POST"
        })

        loadHouses() // refresh after adding

    }catch(err){
        console.log("Error adding house")
    }

}

// ----------------------------
// LOAD TRANSFERS
// ----------------------------

async function loadTransfers(){

    try{

        const res = await fetch("http://127.0.0.1:5000/energy-match")
        const data = await res.json()

        let box = document.getElementById("transfers")

        if(box){

            box.innerHTML = ""

            data.forEach(t=>{
                box.innerHTML += `<li>⚡ ${t.from} → ${t.to} : ${t.energy} W</li>`
            })

        }

    }catch(err){
        console.log("Transfer error")
    }

}

// AUTO LOAD
setInterval(()=>{
    loadHouses()
    loadTransfers()
},3000)

loadHouses()
loadTransfers()