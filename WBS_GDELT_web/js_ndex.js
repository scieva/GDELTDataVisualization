function noneHandler(){
    var img = document.getElementById("mapa");
    img.src = "none.png"
    img.style.display = 'block'
    document.getElementById('dc').style.display = 'none'
    document.getElementById('fdd').style.display = 'none'
}

function allHandler(){
    var img = document.getElementById("mapa");
    img.src = "all.png"
    img.style.display = 'block'
    document.getElementById('dc').style.display = 'none'
    document.getElementById('fdd').style.display = 'none'
}

function allLHandler(){
    var img = document.getElementById("mapa");
    img.src = "all_lines.png"
    img.style.display = 'block'
    document.getElementById('dc').style.display = 'none'
    document.getElementById('fdd').style.display = 'none'
}

function chnHandler() {
    var img = document.getElementById("mapa");
    img.src = "chn.png"
    img.style.display = 'block'
    document.getElementById('dc').style.display = 'none'
    document.getElementById('fdd').style.display = 'none'
}

function rusHandler() {
    var img = document.getElementById("mapa");
    img.src = "rus.png"
    img.style.display = 'block'
    document.getElementById('dc').style.display = 'none'
    document.getElementById('fdd').style.display = 'none'
}

function usaHandler() {
    var img = document.getElementById("mapa");
    img.src = "usa.png"
    img.style.display = 'block'
    document.getElementById('dc').style.display = 'none'
    document.getElementById('fdd').style.display = 'none'
}

function hideDC() {
    var img = document.getElementById("mapa");
    img.style.display = 'none'
    document.getElementById('dc').style.display = 'block'
    document.getElementById('fdd').style.display = 'none'
}

function hideFDD() {
    var img = document.getElementById("mapa");
    img.style.display = 'none'
    document.getElementById('fdd').style.display = 'block'
    document.getElementById('dc').style.display = 'none'
}
