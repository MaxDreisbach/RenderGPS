# RenderGPS
Synthetic glare-point shadowgraphy data generation in Blender with the LuxCore package (code)

by Maximilian Dreisbach (Institute of Fluid Mechanics (ISTM) - Karlsruhe Institute of Technology (KIT))

If you have any questions regarding this code, please feel free to contact Maximilian (maximilian.dreisbach@kit.edu).

# Render routine for synthesized drop test images.
- Takes stl files of a drop, applies correct material, applies subdivision surface modifier, renders the animation with the curent timeline settings, i.e. different seeds, focus points, angles,...
- Outputs raw image and denoised image.
- Requires ,blend file (you can find it here: KITOpen) 
- Tested using Blender 2.93 and BlendLuxCore 2.6.
- Run this script out of Blender install dir with the command:
