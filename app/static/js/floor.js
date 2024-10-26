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
    for (let i = 0; i < items.length; i++) {
        let startTimeMinutes = timeToMinutes(items[i]["time_from"])
        let endTimeMinutes = timeToMinutes(items[i]["time_to"])

        if (currentTimeMinutes >= startTimeMinutes && currentTimeMinutes <= endTimeMinutes) {
            currentItem = items[i]
            if (i + 1 < items.length) {
                nextItem = items[i + 1];
            }
            break
        }
    }
    
    return [currentItem, nextItem]
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
            nextEle.querySelector('.time').innerHTML = `${nextItem["time_from"]} - ${currentItem["time_to"]}`
        }
    })
}

document.addEventListener('DOMContentLoaded', (event) => {
    refreshItems()
});