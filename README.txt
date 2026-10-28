Physical AI Final Project - Python 3.15 (Windows)

No external libraries are needed.

Run in PowerShell from this folder:
  py -3.15 main.py

Press START / RESTART. The robot performs:
1. Move forward toward obstacle A, AI k-NN predicts GO or STOP
2. Stop at obstacle A (5 seconds)
3. Reverse (8 seconds)
4. Turn left (6 seconds)
5. Move toward obstacle B, AI k-NN predicts GO or STOP
6. Stop at obstacle B and display the result (12 seconds)

Record 1-3 minutes of screen video. If the actual run is shorter than one minute,
show an introductory title and a short explanation of the results in the video.

Technical limitations:
- This is a custom 2D kinematic demo, not a physics simulator or real robot.
- k-NN inference is used for the two obstacle stop decisions.
- Reverse and turning are programmed control steps, not AI decisions.
- The model uses manually labeled training distances; no real sensor.
- events.csv is generated when the program runs.

Submission: Public GitHub repository, 1-3 minute YouTube video, PDF report via OmniCampus.
Do not publish personal information.
