document.addEventListener("DOMContentLoaded", function(event) {

    var music = document.getElementById('music'); // id for audio element
    var duration; // Duration of audio clip
    var pButton = document.getElementById('pButton'); // play button
    var playhead = document.getElementById('playhead'); // playhead
    var timeline = document.getElementById('timeline'); // timeline
    
    // timeline width adjusted for playhead
    var timelineWidth = timeline.offsetWidth - playhead.offsetWidth;
    
    // play button event listenter
    pButton.addEventListener("click", play);
    
    // timeupdate event listener
    music.addEventListener("timeupdate", timeUpdate, false);
    
    // makes timeline clickable
    timeline.addEventListener("click", function(event) {
        moveplayhead(event);
        music.currentTime = duration * clickPercent(event);
        console.log(music.currentTime);
    }, false);
    
    // returns click as decimal (.77) of the total timelineWidth
    function clickPercent(event) {
        return (event.clientX - getPosition(timeline)) / timelineWidth;
    
    }
    
    // makes playhead draggable
    playhead.addEventListener('mousedown', mouseDown, false);
    window.addEventListener('mouseup', mouseUp, false);
    
    // Boolean value so that audio position is updated only when the playhead is released
    var onplayhead = false;
    
    // mouseDown EventListener
    function mouseDown() {
        onplayhead = true;
        window.addEventListener('mousemove', moveplayhead, true);
        music.removeEventListener('timeupdate', timeUpdate, false);
    }
    
    
    // mouseUp EventListener
    // getting input from all mouse clicks
    function mouseUp(event) {
        if (onplayhead == true) {
            moveplayhead(event);
            window.removeEventListener('mousemove', moveplayhead, true);
            // change current time
            music.currentTime = duration * clickPercent(event);
            music.addEventListener('timeupdate', timeUpdate, false);
        }
        onplayhead = false;
    }
    // mousemove EventListener
    // Moves playhead as user drags
    function moveplayhead(event) {
        var newMargLeft = event.clientX - getPosition(timeline);
    
        if (newMargLeft >= 0 && newMargLeft <= timelineWidth) {
            playhead.style.marginLeft = newMargLeft + "px";
        }
        if (newMargLeft < 0) {
            playhead.style.marginLeft = "0px";
        }
        if (newMargLeft > timelineWidth) {
            playhead.style.marginLeft = timelineWidth + "px";
        }
    }


    function sec_to_timestamp() {
        var sec_num = parseInt(this, 10);
        var hours = Math.floor(sec_num / 3600 );
        var minutes = Math.floor((sec_num - (hours * 3600)) / 60 );
        var seconds = sec_num - (hours * 3600) - (minutes * 60);

        if (hours < 10 ) { hours = "0" + hours; }
        if (minutes < 10) { minutes = "0" + minutes; }
        if (seconds < 10) { seconds = "0" + seconds; }


        if (sec_num < 3600) {
            console.log(sec_num);
            return "/" + minutes + ":" + seconds;
        } else {
            return "/" + hours + ":" + minutes + ":" + seconds;
        }

        
    }

    // timeUpdate
    // Synchronizes playhead position with current point in audio
    function timeUpdate() {
        var playPercent = timelineWidth * (music.currentTime / duration);
        playhead.style.marginLeft = playPercent + "px";

        var timeDelta = duration - music.currentTime;
        var date = new Date(null);
        var delta = new Date(null);

        delta.setSeconds(timeDelta);
        date.setSeconds(duration);

        var deltaString = delta.toISOString().substr(11, 8);
        var timeString = date.toISOString().substr(11, 8);
        document.getElementById("duration").textContent = "/" + timeString;
        document.getElementById("currenttime").textContent = deltaString;
        console.log(timeDelta)
        if (music.currentTime == duration || timeDelta <= 0) {
            pButton.className = "";
            pButton.className = "fa fa-play-circle-o fa-2x";
        }
    }
    
    //Play and Pause
    function play() {
        // start music
        if (music.paused) {
            music.play();
            // remove play, add pause
            pButton.className = "";
            pButton.className = "fa fa-pause-circle fa-2x";
        } else { // pause music
            music.pause();
            // remove pause, add play
            pButton.className = "";
            pButton.className = "fa fa-play-circle-o fa-2x";
        }
    }
    
    // Gets audio file duration
    music.addEventListener("canplaythrough", function() {
        duration = music.duration;
    }, false);
    
    
    
   
    /*music.addEventListener('loadedmetadata', function() {
        duration = music.duration;
        console.log(duration);
        var date = new Date(null);
        date.setSeconds(duration);
        var timeString = date.toISOString().substr(11, 8);
        document.getElementById("duration").textContent = timeString;
    }, false);*/
    
    

    // getPosition
    // Returns elements left position relative to top-left of viewport
    function getPosition(el) {
        return el.getBoundingClientRect().left;
    }
    
    /* DOMContentLoaded*/
    });