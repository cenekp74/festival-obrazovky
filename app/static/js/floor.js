// funkce ktera zkontroluje ze je server online a pak reloadne stranku
function reloadIfServerOnline() {
    fetch(window.location).then((response) => {
        window.location.reload(true)
    })
}

function timeToMinutes(time) {
    [hours, minutes] = time.split(":").map(Number)
    return hours * 60 + minutes;
}

function getCurrentAndNextItem(room) {
    let dt = new Date();
    let currentTimeMinutes = dt.getHours() * 60 + dt.getMinutes()

    let items = program.filter(item => item.room === room)
    items.sort((a, b) => timeToMinutes(a["time_from"]) - timeToMinutes(b["time_from"]));

    let currentItem = null
    let nextItem = null
    let closestNextItemDistanceMinutes = Infinity
    for (let i = 0; i < items.length; i++) {
        let startTimeMinutes = timeToMinutes(items[i]["time_from"])
        let endTimeMinutes = timeToMinutes(items[i]["time_to"])

        if (currentTimeMinutes >= startTimeMinutes && currentTimeMinutes <= endTimeMinutes) {
            currentItem = items[i]
        }
        
        let itemDistance = startTimeMinutes - currentTimeMinutes;
        if (itemDistance > 0 && itemDistance < closestNextItemDistanceMinutes) {
            closestNextItemDistanceMinutes = itemDistance
            nextItem = items[i]
        }
    }
    
    return [currentItem, nextItem]
}

function adjustTextSize(maxFontSize, maxHeight, textEle, minFontSize=1) { // funkce na zmenseni text size pokud se nazev nevejde do containeru (pokud je height textu vyssi nez maxHeight)
    let fontSize = maxFontSize;
    textEle.style.fontSize = fontSize + "px";

    while (textEle.scrollHeight > maxHeight && fontSize > minFontSize) {
        console.log(textEle.scrollHeight)
        fontSize -= 1;
        textEle.style.fontSize = fontSize + "px";
    }
}

function refreshItems() {
    rooms.forEach(room => {
        let [currentItem, nextItem] = getCurrentAndNextItem(room)

        let currentEle = document.getElementById(`current-${room}`)
        let nextEle = document.getElementById(`next-${room}`)
        if (currentItem) {
            currentEle.querySelector('.name').innerHTML = currentItem["name"]
            currentEle.querySelector('.time').innerHTML = `${currentItem["time_from"]} - ${currentItem["time_to"]}`
        }
        if (nextItem) {
            nextEle.querySelector('.name').innerHTML = nextItem["name"]
            nextEle.querySelector('.time').innerHTML = `${nextItem["time_from"]} - ${nextItem["time_to"]}`
        }
    })
}

function refreshDateTime() {
    let now = new Date()
    const months = [
        "ledna", "února", "března", "dubna", "května", 
        "června", "července", "srpna", "září", 
        "října", "listopadu", "prosince"
    ];

    let day = String(now.getDate())
    let month = months[now.getMonth()]
    let hours = String(now.getHours()).padStart(2, '0')
    let minutes = String(now.getMinutes()).padStart(2, '0')
    let seconds = String(now.getSeconds()).padStart(2, '0')

    date = `${day}. ${month}`
    document.querySelector(".date").innerHTML = date

    time = `${hours}:${minutes}:${seconds}`
    document.querySelector(".time").innerHTML = time
}

function changeSlide() {
    document.querySelector(".countdown svg circle").style.animation = ""
    document.querySelector(".countdown svg circle").clientHeight // trigger dom reflow
    let currentSlide = 0
    document.querySelectorAll(".slideshow img").forEach(slideEle => {
        if (slideEle.classList.contains("active")) {
            currentSlide = Number(slideEle.id.split("-")[1])
        }
    })
    let nextSlide = currentSlide + 1
    if (nextSlide > document.querySelectorAll(".slideshow img").length) {
        nextSlide = 1
    }
    document.querySelectorAll(".slideshow img").forEach(slideEle => {
        slideEle.classList.remove("active")
    })
    document.getElementById("slide-"+nextSlide).classList.add("active")
    document.querySelector(".countdown svg circle").style.animation = `countdown ${SLIDE_INTERVAL_S}s linear infinite forwards`
}

const SLIDE_INTERVAL_S = 20
const RELOAD_TIME_S = 1800

document.addEventListener('DOMContentLoaded', (event) => {
    refreshDateTime()
    setInterval(refreshDateTime, 1000)
    changeSlide()
    setInterval(changeSlide, SLIDE_INTERVAL_S*1000)

    refreshItems()

    setInterval(function() {
        refreshItems()
        document.querySelectorAll(".current .name").forEach(ele => {
            adjustTextSize(32, 86, ele, 20)
        })
        document.querySelectorAll(".next .name").forEach(ele => {
            adjustTextSize(25.6, 64, ele, 15)
        })
    }, 5000)

    setInterval(reloadIfServerOnline, RELOAD_TIME_S * 1000)
});