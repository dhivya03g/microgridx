// =====================================================
// 🚀 MICROGRIDX FINAL REALISTIC DIGITAL TWIN (UPGRADED)
// =====================================================

document.addEventListener("DOMContentLoaded", () => {
    const old = document.querySelector(".twin-cube")
    if (old) old.style.display = "none"
})

const script = document.createElement("script")
script.src = "https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"
document.head.appendChild(script)

script.onload = () => {

const ctrl = document.createElement("script")
ctrl.src = "https://cdn.jsdelivr.net/npm/three@0.128/examples/js/controls/OrbitControls.js"
document.head.appendChild(ctrl)

// 🔥 ADD GLTF LOADER
const gltfScript = document.createElement("script")
gltfScript.src = "https://cdn.jsdelivr.net/npm/three@0.128/examples/js/loaders/GLTFLoader.js"
document.head.appendChild(gltfScript)

ctrl.onload = () => {

const container = document.querySelector(".cube-wrapper")

// ================= SCENE =================
const scene = new THREE.Scene()

const camera = new THREE.PerspectiveCamera(60,1,0.1,1000)
camera.position.set(6,5,8)

const renderer = new THREE.WebGLRenderer({ antialias:true, alpha:true })
renderer.setSize(360,360)
renderer.physicallyCorrectLights = true
renderer.outputEncoding = THREE.sRGBEncoding
container.appendChild(renderer.domElement)

const controls = new THREE.OrbitControls(camera, renderer.domElement)



// ================= LIGHT =================
scene.add(new THREE.AmbientLight(0xffffff,0.6))

const light = new THREE.PointLight(0x00ffff,2)
light.position.set(5,5,5)
scene.add(light)

// 🔥 EXTRA REALISTIC LIGHT
const strongLight = new THREE.DirectionalLight(0xffffff,3)
strongLight.position.set(10,10,10)
scene.add(strongLight)

// 🔥 GLOW
const glowLight = new THREE.PointLight(0x00ffff,5,20)
scene.add(glowLight)

// ================= GLASS CUBE =================
const cube = new THREE.Mesh(
    new THREE.BoxGeometry(5,5,5),
    new THREE.MeshPhysicalMaterial({
        color:0x00ffff,
        transparent:true,
        opacity:0.15,
        transmission:1,
        roughness:0,
        clearcoat:1
    })
)
scene.add(cube)

// 🔥 ENHANCED GLASS
cube.material.envMapIntensity = 2
cube.material.reflectivity = 1
cube.material.ior = 1.5

// edges
const edges = new THREE.LineSegments(
    new THREE.EdgesGeometry(cube.geometry),
    new THREE.LineBasicMaterial({color:0x00ffff})
)
scene.add(edges)

// ================= COMPONENT FUNCTION =================
function board(color,w,h,d){
    return new THREE.Mesh(
        new THREE.BoxGeometry(w,h,d),
        new THREE.MeshStandardMaterial({
            color,
            emissive:color,
            emissiveIntensity:0.3,
            roughness:0.3,
            metalness:0.2
        })
    )
}

// ================= COMPONENTS =================
const esp32 = board(0x00e5ff,2.2,0.15,1.2)
const battery = board(0x22c55e,0.8,1.6,0.8)
const ina219 = board(0xffaa00,0.8,0.2,0.6)
const dht22 = board(0xff4d4d,0.6,1.4,0.6)
const solar = board(0xfacc15,3,0.15,2)

// ================= POSITION =================
esp32.position.set(0,0,0)
battery.position.set(1.5,-1,0)
ina219.position.set(0.5,1,0)
dht22.position.set(-1.5,0,0)

// OUTSIDE
solar.position.set(0,3.2,0)

scene.add(esp32,battery,ina219,dht22,solar)

// ================= WIRES =================
function wire(a,b){
    const pts=[new THREE.Vector3(...a),new THREE.Vector3(...b)]
    return new THREE.Line(
        new THREE.BufferGeometry().setFromPoints(pts),
        new THREE.LineBasicMaterial({color:0x00ffff})
    )
}

scene.add(
    wire([0,0,0],[1.5,-1,0]),
    wire([0,0,0],[0.5,1,0]),
    wire([0,0,0],[-1.5,0,0]),
    wire([0,0,0],[0,3.2,0])
)

// ================= GLB MODEL SUPPORT =================
function loadModel(path, scale, x, y, z){
    const loader = new THREE.GLTFLoader()
    loader.load(path, (gltf)=>{
        const model = gltf.scene
        model.scale.set(scale,scale,scale)
        model.position.set(x,y,z)
        scene.add(model)
    })
}

// Example usage (future)
// loadModel("/models/esp32.glb", 0.5, 0, 0, 0)

// ================= LABELS =================
function label(text){
    const div = document.createElement("div")
    div.innerHTML = text
    div.style.position = "absolute"
    div.style.color = "#00ffff"
    div.style.fontSize = "12px"
    div.style.background = "rgba(0,0,0,0.6)"
    div.style.padding = "3px 6px"
    div.style.borderRadius = "5px"
    container.appendChild(div)
    return div
}

const labels = [
    {el:label("ESP32"), obj:esp32},
    {el:label("Battery"), obj:battery},
    {el:label("INA219"), obj:ina219},
    {el:label("DHT22"), obj:dht22},
    {el:label("Solar"), obj:solar}
]

// ================= ANIMATION =================
function animate(){
    requestAnimationFrame(animate)

    cube.rotation.y += 0.005
    edges.rotation.y += 0.005

    esp32.lookAt(camera.position)
    battery.lookAt(camera.position)
    ina219.lookAt(camera.position)
    dht22.lookAt(camera.position)

    // label positioning
    labels.forEach(l=>{
        const vector = l.obj.position.clone().project(camera)
        const x = (vector.x * 0.5 + 0.5) * renderer.domElement.clientWidth
        const y = (-vector.y * 0.5 + 0.5) * renderer.domElement.clientHeight

        l.el.style.left = x + "px"
        l.el.style.top = y + "px"
    })

    controls.update()
    renderer.render(scene,camera)
}

animate()

}
}