// Mimic Me!
// Fun game where you need to express emojis being displayed

// --- Affectiva setup ---

// The affdex SDK Needs to create video and canvas elements in the DOM
var divRoot = $("#camera")[0];  // div node where we want to add these elements
var width = 640, height = 480;  // camera image size
var faceMode = affdex.FaceDetectorMode.LARGE_FACES;  // face mode parameter
var timeStampCurrent = 0; // will be used for timing on reset button

// Initialize an Affectiva CameraDetector object
var detector = new affdex.CameraDetector(divRoot, width, height, faceMode);

// Enable detection of all Expressions, Emotions and Emojis classifiers.
detector.detectAllEmotions();
detector.detectAllExpressions();
detector.detectAllEmojis();
detector.detectAllAppearance();

// --- Utility values and functions ---

// Unicode values for all emojis Affectiva can detect
var emojis = [ 128528, 9786, 128515, 128524, 128527, 128521, 128535, 128539, 128540, 128542, 128545, 128563, 128561 ];

// Update target emoji being displayed by supplying a unicode value
function setTargetEmoji(code) {
  $("#target").html("&#" + code + ";");
}

// Convert a special character to its unicode value (can be 1 or 2 units long)
function toUnicode(c) {
  if(c.length == 1)
    return c.charCodeAt(0);
  return ((((c.charCodeAt(0) - 0xD800) * 0x400) + (c.charCodeAt(1) - 0xDC00) + 0x10000));
}

// Update score being displayed
function setScore(correct, total) {
  $("#score").html("Score: " + correct + " / " + total);
}

// Display log messages and tracking results
function log(node_name, msg) {
  $(node_name).append("<span>" + msg + "</span><br />")
}

// --- Callback functions ---

// Start button
function onStart() {
  if (detector && !detector.isRunning) {
    $("#logs").html("");  // clear out previous log
    detector.start();  // start detector
  }
  log('#logs', "Start button pressed");
  timeStampInit = 0; // set initial time stamp to 0
}

// Stop button
function onStop() {
  $("#logs").html("");  // clear out previous log
  log('#logs', "Stop button pressed");
  if (detector && detector.isRunning) {
    detector.removeEventListener();
    detector.stop();  // stop detector
  $("#target").html("?"); // set the target Emoji to ? 
  setScore(0, 0); // reset scores
  }
};

// Reset button
function onReset() {
  log('#logs', "Reset button pressed");
  if (detector && detector.isRunning) {
    detector.reset();
  }
  $('#results').html("");  // clear out results
  $("#logs").html("");  // clear out previous log

  // TODO(optional): You can restart the game as well
  detector.start();  // start detector
  gameInit(); // reinitialize scores  
  timeStampInit = timeStampCurrent; // set initial time stamp after reset target Emoji 
};

// Add a callback to notify when camera access is allowed
detector.addEventListener("onWebcamConnectSuccess", function() {
  log('#logs', "Webcam access allowed");
});

// Add a callback to notify when camera access is denied
detector.addEventListener("onWebcamConnectFailure", function() {
  log('#logs', "webcam denied");
  console.log("Webcam access denied");
});

// Add a callback to notify when detector is stopped
detector.addEventListener("onStopSuccess", function() {
  log('#logs', "The detector reports stopped");
  $("#results").html("");
});

// Add a callback to notify when the detector is initialized and ready for running
detector.addEventListener("onInitializeSuccess", function() {
  log('#logs', "The detector reports initialized");
  //Display canvas instead of video feed because we want to draw the feature points on it
  $("#face_video_canvas").css("display", "block");
  $("#face_video").css("display", "none");

  // TODO(optional): Call a function to initialize the game, if needed
  gameInit();
});

// Add a callback to receive the results from processing an image
// NOTE: The faces object contains a list of the faces detected in the image,
//   probabilities for different expressions, emotions and appearance metrics
detector.addEventListener("onImageResultsSuccess", function(faces, image, timestamp) {
  var canvas = $('#face_video_canvas')[0];
  if (!canvas)
    return;

  // Report how many faces were found
  $('#results').html("");
  timeStampCurrent = Math.round(timestamp) // use it to play game and refresh the target Emoji 
  log('#results', "Timestamp: " + timestamp.toFixed(2));
  log('#results', "Number of faces found: " + faces.length);
  if (faces.length > 0) {
    // Report desired metrics
    log('#results', "Appearance: " + JSON.stringify(faces[0].appearance));
    log('#results', "Emotions: " + JSON.stringify(faces[0].emotions, function(key, val) {
      return val.toFixed ? Number(val.toFixed(0)) : val;
    }));
    log('#results', "Expressions: " + JSON.stringify(faces[0].expressions, function(key, val) {
      return val.toFixed ? Number(val.toFixed(0)) : val;
    }));
    log('#results', "Emoji: " + faces[0].emojis.dominantEmoji);
    // Call functions to draw feature points and dominant emoji (for the first face only)
    drawFeaturePoints(canvas, image, faces[0]);
    drawEmoji(canvas, image, faces[0]);      
    // TODO: Call your function to run the game (define it first!)
    // <your code here>
    // function mimicMeMain();  
    mimicMeMain()
  }
});

// --- Custom functions ---

// Draw the detected facial feature points on the image
function drawFeaturePoints(canvas, img, face) {
  // Obtain a 2D context object to draw on the canvas
  var ctx = canvas.getContext('2d');

  // TODO: Set the stroke and/or fill style you want for each feature point marker
  // See: https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D#Fill_and_stroke_styles
  ctx.strokeStyle = 'white';
  
  // Loop over each feature point in the face
  for (var id in face.featurePoints) {
    var featurePoint = face.featurePoints[id];

    // TODO: Draw feature point, e.g. as a circle using ctx.arc()
    // See: https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/arc
    ctx.beginPath();
    ctx.arc(featurePoint.x, featurePoint.y, 2, 0, 2 * Math.PI);
    ctx.stroke();
  }
}

// Draw the dominant emoji on the image
function drawEmoji(canvas, img, face) {
  // Obtain a 2D context object to draw on the canvas
  var ctx = canvas.getContext('2d');

  // TODO: Set the font and style you want for the emoji
  ctx.font = '80px serif';
  // TODO: Draw it using ctx.strokeText() or fillText()
  // See: https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/fillText
  // TIP: Pick a particular feature point as an anchor so that the emoji sticks to your face
  var anchor = face.featurePoints[10];
  dominantEmoji = face.emojis.dominantEmoji; // use this dominant Emoji to compare with targer Emoji in the game
  ctx.fillText(dominantEmoji, anchor.x+25, anchor.y-50);
}

// TODO: Define any variables and functions to implement the Mimic Me! game mechanics

// NOTE:
// - Remember to call your update function from the "onImageResultsSuccess" event handler above
// - You can use setTargetEmoji() and setScore() functions to update the respective elements
// - You will have to pass in emojis as unicode values, e.g. setTargetEmoji(128578) for a simple smiley
// - Unicode values for all emojis recognized by Affectiva are provided above in the list 'emojis'
// - To check for a match, you can convert the dominant emoji to unicode using the toUnicode() function

// Optional:
// - Define an initialization/reset function, and call it from the "onInitializeSuccess" event handler above
// - Define a game reset function (same as init?), and call it from the onReset() function above

// initialization-reset function will set all scores to 0 and restart target Emoji with 1 seconds delay
function gameInit(){
    score = 0; // initialize correctly mimicked emoji score
    scoreTotal = 0; // total attempts to mimic
    setScore(score, scoreTotal); // update scores
    wait(1000) // call wait for 1000ms before show the target Emoji
    showEmoji(); // displays a target emoji to mimic
}

// this function will stop code execution for a ms time in milliseconds
function wait(ms){ 
   var start = new Date().getTime();
   var end = start;
   while(end < start + ms) {
     end = new Date().getTime();
  }
}

// this functions displays a target Emoji 
function showEmoji(){
    var idTargetEmoji = Math.floor(Math.random() * emojis.length); // randomly pick up an index for traget Emoji
    targetEmoji = emojis[idTargetEmoji]
    setTargetEmoji(targetEmoji); // Display the target Emoji  
}

// this function will update scores and displays new target Emoji
function updateScoreEmoji() {
    setScore(score, scoreTotal); // udate game scores 
    wait(2000); // wait for 2000 ms before showing the next tagret Emoji
    timeStampInit = timeStampCurrent++;
    showEmoji (); // update target emoji
}
    
// main function is continuously monitoring if the dominant Emoji matching, the target Emoji.
// if they match within 7 seconds the scores are increased by 1 target Emoji updates
// otherwise it updates only total score and tagret Emoji
function mimicMeMain(){
    if (toUnicode(dominantEmoji) == targetEmoji) {
        scoreTotal++; // Score total plus one
        score++; // Score plus one if the dominant Emoji matched the target Emoji
        $("#logs").html("Good job! You did it! ");
        log('#logs', "Your dominant Emoji was: "+dominantEmoji);
        updateScoreEmoji(); // Updates scores and target Emoji
    }
    if (((timeStampCurrent - timeStampInit + 1) % 8) === 0){
        scoreTotal++; // Score total plus one
        
       /* log('#logs', "Time stamp " + timeStampCurrent);
        log('#logs', "Time stamp modulo of 7 " + ((timeStampCurrent - timeStampInit) % 7));
        log('#logs', "Time stamp initial " + timeStampInit);  */     
        $("#logs").html("You run out of time! Try again! ");
        log('#logs', "Your dominant Emoji was: "+dominantEmoji);
        updateScoreEmoji(); // Updates scores and tagret Emoji
    }
}
