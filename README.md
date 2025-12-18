# eye engagement

an interactive installation that only looks at you when you look at it.

## overview

when you make eye contact, a digital eye tracks your movement. when you look away, it ignores you completely.

this is a human-robotic interaction project built for qtrobot (www.luxai.com) to increase perceived engagement and measure attentiveness, especially with children.

## why this project

qtrobot's main selling point is engagement, but we noticed engagement levels could be improved. by creating an interactive eye that responds to your gaze, we can:

- measure what factors affect engagement
- understand when and why attention is lost
- identify ways to improve interaction rates

## how it works

1. **python tracks your face** using computer vision
2. **checks if you're making eye contact** by detecting your eyes
3. **sends the data** via osc (open sound control) to a processing visualization
4. **processing draws a digital eye** that either:
   - tracks your movement (when you're looking at it)
   - closes and ignores you (when you look away)

## tech stack

- **python 3** — face & eye detection
- **opencv** — camera input and image processing
- **yolo v8** — face detection model
- **haarcascade** — eye detection
- **osc (open sound control)** — data transmission
- **processing** — real-time visualization

## versions

**v1.0** — simple face tracking
- uses yolo for face detection
- calculates face position using geometry
- sends normalized coordinates (0-1)

**v2.0** — face + eye engagement
- adds haarcascade eye detection
- measures engagement with an eye score (0.0 to 1.0)
- only tracks movement when both eyes are visible
- more accurate engagement measurement

## setup & how to run

### 1. install dependencies

```bash
pip install -r requirements.txt
```

### 2. run python (v2.0 recommended)

open a terminal and start the face tracker:

```bash
python faceTracking2.py
```

a window will open showing your face with bounding boxes and eye detection.

### 3. run processing visualization

- open `Eye_Engagement.pde` in processing
- make sure you have the `oscP5` library installed (sketch → import library → manage libraries → search "oscP5" → install)
- click the play button to start the visualization

### 4. see it in action

- the digital eye should now respond to your movements
- when you look at the camera (both eyes visible), the eye tracks you and says "i see you"
- when you look away or close your eyes, the eye closes and says "ignoring you"

**tip:** run both python and processing at the same time for the full experience.
