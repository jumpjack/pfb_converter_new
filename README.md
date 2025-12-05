# PFB converter

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

Iris Inventor --> Open Inventor (**) --> 

- IRIS GL (1982) 
- IRIS Inventor (1992)
- OpenGL (1992)
- Open Inventor (1994) (**)
- IRIS Performer (1995) 
- OpenGL Performer (1996-97)

(**) Not "open source", but "OpenGL based"!
