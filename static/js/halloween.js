function toggleTheme() {
    document.body.classList.toggle('dark-mode');
}

function getRandom(min, max) {
    return Math.random() * (max - min) + min;
}

// --- GEIST LOGIK ---
const ghost = document.getElementById('ghost');

function triggerGhost() {
    if (document.body.classList.contains('dark-mode')) {
        const duration = getRandom(5, 10);
        const direction = Math.random() < 0.5 ? 'up' : 'down';
        const randomX = getRandom(10, 80);

        ghost.style.left = randomX + 'vw';
        ghost.style.animation = `${direction === 'up' ? 'moveUp' : 'moveDown'} ${duration}s linear forwards`;
        ghost.classList.add('active');

        setTimeout(() => {
            ghost.classList.remove('active');
            ghost.style.animation = '';
        }, duration * 1000);
    }

    const nextInterval = getRandom(20000, 60000);
    setTimeout(triggerGhost, nextInterval);
}

// --- HEXEN LOGIK ---
const witch = document.getElementById('witch');

function triggerWitch() {
    if (document.body.classList.contains('dark-mode')) {
        const duration = getRandom(1, 5);
        const toLeft = Math.random() < 0.5;
        const randomY = getRandom(10, 60);

        // Holt die Bildpfade aus den data-Attributen
        if (toLeft) {
            witch.src = witch.getAttribute('data-left-src');
            witch.style.animation = `moveRightToLeft ${duration}s linear forwards`;
        } else {
            witch.src = witch.getAttribute('data-right-src');
            witch.style.animation = `moveLeftToRight ${duration}s linear forwards`;
        }

        witch.style.top = randomY + 'vh';
        witch.classList.add('active');

        setTimeout(() => {
            witch.classList.remove('active');
            witch.style.animation = '';
        }, duration * 1000);
    }

    const nextInterval = getRandom(20000, 60000);
    setTimeout(triggerWitch, nextInterval);
}

setTimeout(triggerGhost, 5000);
setTimeout(triggerWitch, 7000);