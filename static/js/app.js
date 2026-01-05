let currentTracks = [];
let currentIndex = 0;

const player = document.getElementById("player");
const audioSource = document.getElementById("audio-source");
const capturedImage = document.getElementById("captured-image");
const capturedEmotion = document.getElementById("captured-emotion");
const liveEmotion = document.getElementById("live-emotion");


// ----------------------------------------------------------
// LIVE STATUS UPDATE (emotion only)
// ----------------------------------------------------------
setInterval(() => {
    fetch("/status")
        .then(res => res.json())
        .then(data => {
            liveEmotion.textContent = "Emotion: " + data.emotion;
        });
}, 900);


// ----------------------------------------------------------
// CAPTURE BUTTON
// ----------------------------------------------------------
document.getElementById("capture-btn").addEventListener("click", () => {

    fetch("/capture")
        .then(res => res.json())
        .then(data => {

            if (!data.ok) {
                alert("No frame available!");
                return;
            }

            // Update captured image
            capturedImage.src = "/" + data.path + "?t=" + Date.now();
            capturedEmotion.textContent = "Emotion: " + data.emotion;

            // LOAD SONGS
            currentTracks = data.tracks;
            currentIndex = 0;

            if (currentTracks.length > 0) {
                playCurrentSong();
            } else {
                console.log("No tracks available for this emotion.");
            }
        });
});


// ----------------------------------------------------------
// PLAY CURRENT SONG
// ----------------------------------------------------------
function playCurrentSong() {

    if (!currentTracks || currentTracks.length === 0) {
        console.log("No songs loaded.");
        return;
    }

    let track = currentTracks[currentIndex];

    console.log("Playing:", track);

    // ALWAYS ensure proper path: add leading slash
    audioSource.src = "/" + track;

    player.load();

    player.play()
        .catch(err => {
            console.log("Autoplay blocked, waiting for user interaction.", err);
        });
}


// ----------------------------------------------------------
// NEXT SONG BUTTON
// ----------------------------------------------------------
document.getElementById("next-song-btn").addEventListener("click", () => {
    if (currentTracks.length === 0) return;

    currentIndex = (currentIndex + 1) % currentTracks.length;
    playCurrentSong();
});
