

function day_changed(today, tomorrow) {
    if (today.getFullYear() == tomorrow.getFullYear() &&
        today.getMonth() == tomorrow.getMonth() &&
        today.getDate() == tomorrow.getDate()
    ) {
            return true
    } else {
        return false
    }
}

export default day_changed