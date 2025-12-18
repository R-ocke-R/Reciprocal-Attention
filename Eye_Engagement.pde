import netP5.*;
import oscP5.*;

OscP5 oscP5;

// Data - Python 
float userX = 0.5;
float userY = 0.5;
int isFacing = 1; 

float pupilX = 0;
float pupilY = 0;

void setup() {
  size(800, 600);
  oscP5 = new OscP5(this, 9999);
  
  // Center pupil initially
  pupilX = width/2;
  pupilY = height/2;
}

void draw() {
  background(20); 
  
  if (isFacing == 1) {
    
    // White part of eye
    fill(255); 
    stroke(0);
    strokeWeight(4);
    ellipse(width/2, height/2, 400, 250);
    
    //  normalized data (0-1) to screen pixels
    float targetPupilX = map(userX, 0, 1, width/2 - 100, width/2 + 100);
    float targetPupilY = map(userY, 0, 1, height/2 - 80, height/2 + 80);
    
    // Smooth movement (Linear Interpolation)
    pupilX = lerp(pupilX, targetPupilX, 0.2);
    pupilY = lerp(pupilY, targetPupilY, 0.2);
    // drawing Pupil (Red) & reflection 
    fill(200, 0, 0);
    noStroke();
    ellipse(pupilX, pupilY, 90, 90);
    fill(255, 150);
    ellipse(pupilX + 20, pupilY - 20, 30, 30); 
    fill(255);
    textAlign(CENTER);
    textSize(24);
    text("I SEE YOU", width/2, height - 50);
    
  } else {
    // closed eye 
    stroke(150);
    strokeWeight(5);
    line(width/2 - 200, height/2, width/2 + 200, height/2);
    
    fill(150);
    textAlign(CENTER);
    textSize(24);
    text("IGNORING YOU", width/2, height - 50);
  }
}

// Event listener for incoming OSC data
void oscEvent(OscMessage theOscMessage) {
  if (theOscMessage.checkAddrPattern("/pose")) {
    userX = theOscMessage.get(0).floatValue();
    userY = theOscMessage.get(1).floatValue();
    isFacing = theOscMessage.get(2).intValue();
  }
}
