// Capture Emotion
document.getElementById("captureBtn").onclick = async function () {
    const res = await fetch("/capture");
    const data = await res.json();

    // update emotion text
    document.getElementById("emotionText").innerText =
        `${data.emotion} (${data.confidence}%)`;

    // show captured image
    document.getElementById("resultImg").src = data.image;

    // play emotion song
    const player = document.getElementById("player");
    player.src = data.track;
    player.play();
};

// Next Song
document.getElementById("nextSongBtn").onclick = function() {
    const player = document.getElementById("player");
    player.currentTime = 0;
    player.play();
};
