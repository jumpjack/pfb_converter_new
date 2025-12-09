# PFB converter

<img width="370" height="203" alt="image" src="https://github.com/user-attachments/assets/fb16edb8-1bc7-4d60-a305-45d283f94d5e" />

Spirit rover at Troy

----------------


Tool to convert PFB(*) files to a 3d format that can be read by modern software.

Bugs fixed
- PF_MAX_TEXTURES_19 = 4 (not 19)
- N_LOD is not a node of type "group"
- Added one "appearance" field to the end of geoset reading (don't know why, decided by AI...)


Se also this repo for related stuff: https://github.com/jumpjack/VST-converter/tree/main/PFB/experiments

Original OpenGL Performer source code: https://github.com/jumpjack/SGI-OpenGL-Performer

----------------


(*) Iris Performer Fast Binary; it also existed a Performer Fast ASCII (PFA) format. Don't confuse with modern PFB format for fonts! "Printer Font Binary" for Adobe Type 1 fonts. 

"Iris Performer" software then became "OpenGL Performer", developed by Silicon Grpahics Inc. (SGI), no more existing.

History:



- [IRIS](https://en.wikipedia.org/wiki/SGI_IRIS) GL (1982) 
- [IRIS](https://en.wikipedia.org/wiki/SGI_IRIS) Inventor (1992)
- [OpenGL](https://en.wikipedia.org/wiki/OpenGL) (1992)
- [Open Inventor](https://en.wikipedia.org/wiki/Open_Inventor) (1994) (**)
- IRIS Performer (1995) 
- [OpenGL Performer](https://en.wikipedia.org/wiki/OpenGL_Performer) (1996-97)
- Cosmo3d
- [Coin3d](https://en.wikipedia.org/wiki/Coin3D)(***) API by Systems in Motion (SIM) ([source code](https://sourceforge.net/projects/coin3d/files/Coin-3.1.3.tar.gz/download)) --> Kongsberg SIM
- [OpenGL++](https://en.wikipedia.org/wiki/OpenGL_plus_plus)
- [Fahrenheit](https://en.wikipedia.org/wiki/Fahrenheit_graphics_API)

-----

- IRIS = [Integrated Raster Imaging System](https://en.wikipedia.org/wiki/SGI_IRIS) (Hardware by SGI)
- IRIX = IRIS Operating System based on Unix
- GL = Graphics Library
- SGI = [Silicon Grpahics Inc](https://en.wikipedia.org/wiki/Silicon_Graphics)

(**) Not "open source", but "OpenGL based"!

(***) Being only a 3D rendering library, Coin needs a user interface binding to be able to open windows, handle user input etc. GUI Bindings are available for the native Microsoft Windows GUI (SoWin), Trolltech's QT (SoQt), Xt/Motif on X Windows (SoXt), and the native Mac OS X GUI (Sc21).
