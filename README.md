# PFB converter

<img width="370" height="203" alt="image" src="https://github.com/user-attachments/assets/fb16edb8-1bc7-4d60-a305-45d283f94d5e" />

Spirit rover at Troy. See it [here](https://sketchfab.com/3d-models/troy-final-resting-position-of-spirit-rover-bd2535ef9cdd468abb213d7a27f42bb0) in immersive 3d with your Meta Quest or any VR viewer.

----------------


Tool to convert PFB(*) files to a 3d format that can be read by modern software.

## Usage
```
pfb2obj.py [-h] [-t {NASA,other}] [-i INPUT] [-o OUTPUT] [-of OUTPUT_FOLDER] [-tf TEXTURES_FOLDER]
                  [-bf BASE_FOLDER] [-l LOD] [-tse TEXTURE_SOURCE_EXTENSION] [-tde TEXTURE_DESTINATION_EXTENSION]
                  [-ot ONLY_TEXTURES] [-r REFERENCE] [-v VERBOSE]

```

### Basic example

`python pfb2obj.py -t NASA --base-folder C:\Downloads\ --LOD 0 --input C:\Downloads\PFB\inputfile.pfb`

Converts **inputfile.pfb** to **inputfile.obj** using NASA standard for textures, maximum level of detail; .obj file is saved into  C:\Downloads\ , textures are saved into C:\Downloads\textures

### Options

```
  -t, --texture {NASA,other}
                        Options: NASA, other . Specify if texture are standard or for NASA rovers
  -i, --input INPUT     Input PFB file
  -o, --output OUTPUT   Output OBJ file (optional; if not specified, input file will be used as base for the name).
                        Default: "input.OBJ"
  -of, --output-folder OUTPUT_FOLDER
                        Folder for output files (.obj+.mtl) and textures folder. Must be already present. Default:
                        "mymodels\"
  -tf, --textures-folder TEXTURES_FOLDER
                        Folder to store downloaded textures, also referenced in MTL file. Default: "textures\"
  -bf, --base-folder BASE_FOLDER
                        Root folder for output folder Default: ".\"
  -l, --LOD LOD         Level Of Detail (LOD); 0 = higher definition, 6 = minimum definition. Default: "6"
  -tse, --texture-source-extension TEXTURE_SOURCE_EXTENSION
                        Original extension of texture, to be changed into argument of --texture-destination-extension.
                        Default: "rgb"
  -tde, --texture-destination-extension TEXTURE_DESTINATION_EXTENSION
                        Final extension of texture, from original specified in --texture-source-extension. Default:
                        "img.jpg"
  -ot, --only-textures ONLY_TEXTURES
                        Parses PFB file to extract only terxtures names. Default: "False"
  -r, --reference REFERENCE
                        Reference system: x_zy, xzy, xyz Default: "x_zy"
  -v, --verbose VERBOSE
                        Amount of debug messages shown


```

## Bugs fixed from original source
-  PF_MAX_TEXTURES_19 = 4 (not 19)
-  N_LOD is not a node of type "group"
-  Added one "appearance" field to geoset reading (don't know why...)
-  Added 1 position increment while reading geostate in case of statemode == STATE_ENTEXTURE
-  aniso_degree was read but not stored


------------

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
