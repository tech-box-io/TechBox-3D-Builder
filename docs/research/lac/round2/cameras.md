# LAC round 2: the cameras from Lee's screenshots (21 Oct 2026)

Each solved in the player at the screenshots' canvas shape (2000 x 1022: the window 1000 x 597 CSS px), by fitting the camera (direction,
target, radius) to points whose 3D positions are known (label and eye anchors, cap pin tips, lead ends at the potentiometer's pins,
lead-line ends), Nelder-Mead on the reprojection error; then the target slid along the sight line to a point inside the model (the eye
kept), and the render blended with the screenshot at full size: no visible offset in any of the four. (The silhouette solver,
camsolve.js, was thrown by parts the screenshots cut off: F4 in Step 16, the base in all of them.)

| Steps | screenshot | points | fit (px RMS) | view_dir | frame |
|---|---|---|---|---|---|
| 16 - 18 | lee_1_step16_camera.webp | j27 hole, the held cap, the two hanging switch pin tips | 0.7 | [0.4007, 0.615, -0.6792] | ([643.67, 917.68, 1281.09], 45.24) |
| 30 - 32 | lee_2_step30_camera.webp | (+) red hole, held cap tip, two lying pin tips, three lead ends at the pot | 1.6 | [-0.2332, 0.758, 0.6091] | ([697.93, 915.57, 1338.76], 41.69) |
| 33 - 34 | lee_4_step34_camera.webp | (-) blue hole, the black cap's pin tip and housing | 3.3 (3 points; the overlay confirms) | [-0.3958, 0.7598, 0.5158] | ([656.14, 910.4, 1382.06], 46.98) |
| 49 | lee_8_step49_camera.webp | the four lead-line ends, two lead ends at the pot | 2.5 | [0.4502, 0.5391, 0.7119] | ([703.91, 927.27, 1307.02], 97.1) |
