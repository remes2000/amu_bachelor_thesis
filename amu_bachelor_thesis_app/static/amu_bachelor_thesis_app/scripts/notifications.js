const interval = 3000;
const bigNotificationDotContainer = document.querySelector('#big-notification-dot-container');
const smallNotificationDot = document.querySelector('#small-notification-dot');
const audio = new Audio('/static/amu_bachelor_thesis_app/audio/notification.mp3');
let currentNumberOfNotifications = +smallNotificationDot.innerHTML;
setupNextFetch();
async function fetchNotificationCounter() {
    try {
        const response = await fetch('/amu_bachelor_thesis/notifications_getcounter');
        const responseBody = await response.json();
        if(responseBody.unread_notifications > currentNumberOfNotifications) {
            await audio.play();
        }
        currentNumberOfNotifications = responseBody.unread_notifications;
        smallNotificationDot.innerHTML = currentNumberOfNotifications;
        bigNotificationDotContainer.querySelector('div').innerHTML = currentNumberOfNotifications;
        if(currentNumberOfNotifications === 0) {
            smallNotificationDot.classList.add('hidden');
            bigNotificationDotContainer.classList.add('hidden');
        } else {
            smallNotificationDot.classList.remove('hidden');
            bigNotificationDotContainer.classList.remove('hidden');
        }
    } catch (e) {
        console.log('Wystapił problem podczas pobierania powiadomień')
    }
    setupNextFetch();
}

function setupNextFetch() {
    setTimeout(() => {
        fetchNotificationCounter()
    }, interval);
}