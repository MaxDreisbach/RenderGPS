# RenderGPS
Synthetic glare-point shadowgraphy data generation in Blender with the LuxCore package (code) \
by Maximilian Dreisbach (Institute of Fluid Mechanics (ISTM) - Karlsruhe Institute of Technology (KIT))

This code repository contains the script for synthetic data generation through phsically-based rendering used in the research article "Spatio-temporal reconstruction of droplet impingement dynamics by means of color-coded glare points and deep learning" (https://doi.org/10.1088/1361-6501/ad8771). \
The digital twin modeled in the rendering enironment Blender mirrors the experimental setup of the glare-point shadowgraphy experiments used for the imaging of gas-liquid interfaces in two-phase flows.
The rendered synethtic glare-point shadowgraphy images can be used to train neural networks for interface reconstruction as presenetd in the aforementioned article.

If you have any questions regarding this code, please contact Maximilian (maximilian.dreisbach@kit.edu).

## Render routine
- Reads stl files of a gas-liquid interface geometry
- applies correct materials (water inside, air outside)
- applies subdivision surface modifier to smooth meshes
- renders the synethtic images with the curent .blend-file settings, i.e. light source angles and droplet rotation angles, different seeds, focus settings of objective lens
- Outputs raw and denoised images

## Requirements
- .blend file containing the modeled rendering setup (you can find it here: https://doi.org/10.35097/mmnxkbqqeye8p5tx)
- stl files of gas-liquid interfaces

## Tested for: 
- Blender 2.93 and BlendLuxCore 2.6

## Getting Started
- Run this script out of Blender install dir with the command: "blender -b --python "P3_drop_large_rotation.py"
