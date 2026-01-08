# Fixed bugs to support NASA files:
# PF_MAX_TEXTURES_19 = 4 (not 19)
# N_LOD is not a node of type "group"
# Added one "appearance" field to geoset reading (don't know why...)

import traceback
import sys, struct
from pfb_constants import *

ENDIAN_FLAG = '>'

PF_MAX_TEXTURES_19 = 4  # fixed to 4, not 19

# making a logical assumption for the values of PF_OFF & PF_ON - doublecheck this, then move this stuff to pfb_constants
PF_OFF = 0
PF_ON = 1
OnOff_table = [ 2, PF_OFF, PF_ON ]



def readInt32(f):
    data = f.read(4)
    if data == "":
        raise Exception("end of file")
    return struct.unpack(ENDIAN_FLAG+'i', data)[0]

def readUInt32(f):
    data = f.read(4)
    if data == "":
        raise Exception("end of file")
    return struct.unpack(ENDIAN_FLAG+'I', data)[0]

def readUInt16(f):
    data = f.read(2)
    if data == "":
        raise Exception("end of file")
    return struct.unpack(ENDIAN_FLAG+'H', data)[0]

def readFloat32(f):
    data = f.read(4)
    if data == "":
        raise Exception("end of file")
    return struct.unpack(ENDIAN_FLAG+'f', data)[0]

def readInt32Array(f,num):
    return [readInt32(f) for i in range(num)]

def readUInt32Array(f,num):
    return [readUInt32(f) for i in range(num)]

def readUInt16Array(f,num):
    return [readUInt16(f) for i in range(num)]

def readFloat32Array(f,num):
    return [readFloat32(f) for i in range(num)]

def readPfVec4(f):
    return readFloat32Array(f,4)

def readPfVec3(f):
    return readFloat32Array(f,3)

def readPfVec2(f):
    return readFloat32Array(f,2)

def readPfVec4Array(f,num):
    return [readPfVec4(f) for i in range(num)]

def readPfVec3Array(f,num):
    return [readPfVec3(f) for i in range(num)]

def readPfVec2Array(f,num):
    return [readPfVec2(f) for i in range(num)]



class Tex0T:
    def __init__(self,f):
        self.format = readInt32Array(f,5)
        self.filter = readUInt32Array(f,4)
        self.wrap = readInt32Array(f,3)
        self.bcolor = readPfVec4(f)
        self.btype = readInt32(f)
        self.ssp = readPfVec2Array(f,4)
        self.ssc = readFloat32(f)
        self.dsp = readPfVec2Array(f,4)
        self.dsc = readFloat32(f)
        self.tdetail = readInt32Array(f,2)
        self.lmode = readInt32Array(f,3)
        self.losource = readInt32Array(f,2)
        self.lodest = readInt32Array(f,2)
        self.lsize = readInt32Array(f,2)
        self.image = readInt32(f)
        self.comp = readInt32(f)
        self.xsize = readInt32(f)
        self.ysize = readInt32(f)
        self.zsize = readInt32(f)
        self.load_image = readInt32(f)
        self.list_size = readInt32(f)
        self.frame = readFloat32(f)
        self.num_levels = readInt32(f)
        self.udata = readInt32(f)
        self.type = 0
        self.aniso_degree = 0


SIZEOF_CLIPTEX_T = 15*4
SIZEOF_CLIPLEVEL_T = 7*4

def readTex(version,f):
    size = readInt32(f)
    if size == -1:
        pass
    else:
        name = f.read(size).decode('ascii')
    if version >= PFBV_ANISOTROPY:
        # read tex_t (232 bytes)
        t = Tex0T(f)
        t.type = readInt32(f)
        readInt32(f)
    elif version >= PFBV_CLIPTEXTURE:
        # read tex_1_t (228 bytes)
        t = Tex0T(f)
        t.type = readInt32(f)
    else:
        t = Tex0T(f)
    if t.list_size > 0:
        for i in range(t.list_size):
            readInt32(f)
    if t.type == TEXTYPE_TEXTURE:
        if t.num_levels > 0:
            for i in range(t.num_levels):
                readInt32(f)
    else:
        f.read(SIZEOF_CLIPTEX_T)
        if t.num_levels > 0:
            f.read(t.num_levels * SIZEOF_CLIPLEVEL_T)
    t.filename = name
    return t


def isGroupClassType(t):
# remved N_LOD
    return t in [N_GROUP, N_SCS, N_DCS, N_PARTITION, N_SCENE, N_SWITCH, N_SEQUENCE, N_LAYER, N_MORPH, N_ASD, N_FCS, N_DOUBLE_DCS, N_DOUBLE_FCS, N_DOUBLE_SCS ]


class Node_data:
    def __init__(self,node_type):
        self.type = node_type
        self.name = ""

def int32_to_float32(x, little=True):
    """
    Reinterpreta un intero a 32 bit come float32.

    Args:
        x (int): valore intero da reinterpretare (con segno o senza)
        little (bool): True per little-endian, False per big-endian

    Returns:
        float: valore float32 corrispondente
    """
    # Maschera per trattare x come unsigned a 32 bit
    x_uint = x & 0xFFFFFFFF
    # Scegli il formato struct in base all'endianness
    fmt = '<I' if little else '>I'
    packed = struct.pack(fmt, x_uint)
    # Reinterpretare come float32 (stesso endian)
    float_fmt = '<f' if little else '>f'
    return struct.unpack(float_fmt, packed)[0]


def readNode(version, f, counter):
    try:
        buf_size = readInt32(f)
        buf = readInt32Array(f, buf_size) # Read chunk of words containing whole node data
        node = Node_data(buf.pop(0)) # Store node type into node item "type"
        if isGroupClassType(node.type):
            print(f"   Node {counter}: Group class")
            count = buf.pop(0)
            if node.type == N_GROUP:
                print(f"      Processing Group: storing {count} children.")
                try:
                    for i in range(count):
                        val = buf.pop(0)
                        print(f"      Letto {val} per children")
                        node.children = val
                    #node.children = [buf.pop(0) for i in range(count)]
                except Exception as e:
                    traceback.print_exc()
            else:
                node_name = node_type_dict.get(node.type, f"UNKNOWN_NODE_{node.type}")
                print(f'      Unsupported group type {node.type} ({node_name})')
        elif node.type == N_LOD:  # added, for NASA files
            print(f"   Node {counter}:  LOD")
            try:
                rangesCount = buf.pop(0)

                print (f"      Extracting  {rangesCount + 1} ranges.")
                # Ciclo 1: leggi (rangesCount + 1) valori float per 'ranges'
                ranges = []
                for i in range(rangesCount + 1):
                    val = int32_to_float32(buf.pop(0), False)
                    print(f"        {val}")
                    ranges.append(val)
                node.ranges = ranges

                print (f"      Extracting  {rangesCount + 1} transitions.")
                # Ciclo 2: leggi (rangesCount + 1) valori float per 'trans'
                trans = []
                for i in range(rangesCount + 1):
                    val = int32_to_float32(buf.pop(0), False)
                    print(f"        {val}")
                    trans.append(val)
                node.transitions = trans

                # Ciclo 3: leggi 3 valori float per le coordinate (sempre 3, non dipendono da rangesCount)
                print (f"      Extracting  3 coordinates for center.")
                coords = []
                for i in range(3):
                    val = int32_to_float32(buf.pop(0), False)
                    print(f"        {val}")
                    coords.append(val)
                node.centerCoords = coords

                # Leggi lodState e lodStateIndex
                lodState = buf.pop(0)
                lodStateIndex = buf.pop(0)

                # Leggi il numero di figli
                numChildren = buf.pop(0)
                print(f"      LOD has {numChildren} children")
                # Ciclo 4: leggi gli indici dei figli (solo se numChildren != -1)
                children = []
                if numChildren != -1:
                    for i in range(numChildren):
                        childIndex = buf.pop(0)
                        print(f"        child node: n. {childIndex}")
                        children.append(childIndex)

                node.lodState = lodState
                node.lodStateIndex = lodStateIndex
                node.numChildren = numChildren
                node.children = children

            except Exception as e:
                print ("Non ha funzionato :-(")
                traceback.print_exc()

        elif node.type == N_GEODE:
            count = buf.pop(0)
            print(f"   Node {counter}: Geode")
            try:
                print(f"      Extracting {count} geosets.")
                node.gsets = [buf.pop(0) for i in range(count)]
            except Exception as e:
                traceback.print_exc()
        else:
            node_name = node_type_dict.get(node.type, f"UNKNOWN_NODE_{node.type}")
            print(f'      No group, no geode, unsupported node type {node.type} ({node_name})')

        node.isect_travmask = buf.pop(0)
        node.app_travmask = buf.pop(0)
        node.cull_travmask = buf.pop(0)
        node.draw_travmask = buf.pop(0)
        name_size = readInt32(f)
        if name_size != -1:
            node.name = f.read(name_size).decode('ascii')
            print(f"      Found name for this node: {node.name}")
        return node
    except Exception as e:
        print(f"   ======== NODE PARSING EXCEPTION ==========")
        traceback.print_exc()


# def readNode(version,f,counter):
#     try:
#         buf_size = readInt32(f)
#         buf = readInt32Array(f,buf_size)
#         node = Node_data(buf.pop(0))
#         if isGroupClassType(node.type):
#             print(f"   Node {counter}: Group class")
#             count = buf.pop(0)
#             if node.type == N_GROUP:
#                 print(f"      Processing Group: storing {count} children.")
#                 try:
#                     node.children = [buf.pop(0) for i in range(count)]
#                 except Exception as e:
#                     traceback.print_exc()
#             elif node.type == N_LOD: #added, for NASA files
#                 # --- Struttura dati per memorizzare i geoset ---
#                 geosets_list = []  # Lista globale per raccogliere tutti i geoset
#
#                 print(f"      Processing LOD: storing {count} ranges.")
#                 try:
#                     node.ranges = [buf.pop(0) for i in range(count)]
#
#
#
# #                 print(f"      Processing LOD: storing {count} ranges.")
# #                 try:
# #                     node.ranges = [buf.pop(0) for i in range(count)]
# #                     for r in node.ranges:
# #                         print(f"      Extracting range")
#
#
#
#                 except Exception as e:
#                     traceback.print_exc()
#             else:
#                 node_name = node_type_dict.get(node.type, f"UNKNOWN_NODE_{node.type}")
#                 print(f'      Unsupported group type {node.type} ({node_name})')
#         elif node.type == N_GEODE:
#             count = buf.pop(0)
#             print(f"   Node {counter}: Geode")
#             try:
#                 print(f"      Extractring {count} geosets.")
#                 node.gsets = [buf.pop(0) for i in range(count)]
#             except Exception as e:
#                 traceback.print_exc()
#         else:
#             node_name = node_type_dict.get(node.type, f"UNKNOWN_NODE_{node.type}")
#             print(f'      No group, no geode, unsupported node type {node.type} ({node_name})')
#
#         node.isect_travmask = buf.pop(0)
#         node.app_travmask = buf.pop(0)
#         node.cull_travmask = buf.pop(0)
#         node.draw_travmask = buf.pop(0)
#         name_size = readInt32(f)
#         if name_size != -1:
#             node.name = f.read(name_size).decode('ascii')
#             print(f"      Found name for this node: {node.name}")
#         return node
#     except Exception as e:
#         print(f"   ======== NODE PARSING EXCEPTION ==========")
#         traceback.print_exc()



class Mtl_data:
    def __init__(self,version,f):
        self.side = readInt32(f)
        self.alpha = readFloat32(f)
        self.shininess = readFloat32(f)
        self.ambient = readPfVec3(f)
        self.diffuse = readPfVec3(f)
        self.specular = readPfVec3(f)
        self.emission = readPfVec3(f)
        self.cmode = readInt32Array(f,2)
        self.udata = readInt32(f)

class Gset_data:
    def __init__(self, version, f, debug=False):
        self.debug = debug
        pos = f.tell()  # Ottieni la posizione corrente nel file

        primitiveType = readInt32(f)
        if debug:
            print(f"        {pos:08x}h: primitiveType = {primitiveType:08x}h ({primitiveType}, {gspt_table_strings[primitiveType]}, in node memorizzo {primitiveType})")
        else:
            pass
            #print(f"Looking for primitive type {primitiveType:08x}h in lookup table")
        #self.ptype = gspt_table[primitiveType]
        self.ptype = primitiveType #debug memorizzo valore grezzo letto da file
        if not debug:
            pass
            #print(f"  Result: {gspt_table[primitiveType]} = {gspt_table_strings[primitiveType]}")

        pos = f.tell()
        self.pcount = readInt32(f)
        if debug: print(f"        {pos:08x}h: pcount = {self.pcount:08x}h ({self.pcount})")

        pos = f.tell()
        self.llist = readInt32(f)
        if debug: print(f"        {pos:08x}h: llist = {self.llist:08x}h ({self.llist})")

        pos = f.tell()
        self.vlist = readInt32Array(f, 3)

        pos = f.tell()
        self.clist = readInt32Array(f, 3)

        pos = f.tell()
        self.nlist = readInt32Array(f, 3)

        pos = f.tell()
        self.tlist = readInt32Array(f, 3)

        pos = f.tell()
        self.draw_mode = readInt32Array(f, 3)

        pos = f.tell()
        self.gstate = readInt32Array(f, 2)

        pos = f.tell()
        self.line_width = readFloat32(f)

        pos = f.tell()
        self.point_size = readFloat32(f)

        pos = f.tell()
        self.draw_bin = readInt32(f)

        pos = f.tell()
        self.isect_mask = readUInt32(f)

        pos = f.tell()
        self.hlight = readInt32(f)

        pos = f.tell()
        self.bbox_mode = readInt32(f)

        pos = f.tell()
        self.bbox = readFloat32Array(f, 6)

        pos = f.tell()
        self.udata = readInt32(f)

        if version >= PFBV_GSET_DO_DP:
            pos = f.tell()
            self.draw_order = readUInt32(f)

            pos = f.tell()
            self.decal_plane = readInt32(f)

            pos = f.tell()
            self.dplane_normal = readFloat32Array(f, 3)

            pos = f.tell()
            self.dplane_offset = readFloat32(f)


        if version >= PFBV_GSET_BBOX_FLUX:
            pos = f.tell()
            self.bbox_flux = readInt32(f)

        if version >= PFBV_MULTITEXTURE:
            pos = f.tell()
            self.multi_tlist = readInt32Array(f, 3 * (PF_MAX_TEXTURES_19 - 1))


            dummy = readInt32(f) #debug ?!?!? "appearance"?


def readGset(version, f, debug=False):
    if debug:
        print("      Calling Gset_data in DEBUG mode.")
        gset = Gset_data(version, f, debug)
        print("      Returned from Gset_data.")
        return gset
    else:
        gset = Gset_data(version, f)
        return gset


def readMtl(version,f):
    mtl = Mtl_data(version,f)
    return mtl


class Gstate_data:
    def __init__(self):
        self.enlighting = False
        self.entexture = False
        self.frontmtl = -1
        self.texture = -1
    def read(self,version,f):
        buf_size = readInt32(f)
#NOTE: not all of the data in buf is actually Int32's - some of it can be 32-bit floats (for alpharef and for texture matrices); the original PFB code would use pointer casting to convert those parts to floats; may be able to do the same thing with Python's struct functions, but it could be messy
        buf = readInt32Array(f,buf_size)
        pos = 0
        endpos = buf_size - 1
        while pos < endpos:
            statemode = buf[pos]
            pos += 1
            if statemode == STATE_ENLIGHTING:
                self.enlighting = (OnOff_table[buf[pos]] == PF_ON)
                pos += 1
            elif statemode == STATE_ENTEXTURE:
                if version >= PFBV_MULTITEXTURE:
                    # would need to replace add a multitex alternative to "entexture"
                    pos += PF_MAX_TEXTURES_19-1
                else:
                    self.entexture = (OnOff_table[buf[pos]] == PF_ON)
                    pos += 1
            elif statemode == STATE_FRONTMTL:
                #NOTE: this is an index into the list 'data.mtl'; in original PFB code it assumed the mtl info came first, so it was looked up at this point to set the material number with pfGStateAttr
                self.frontmtl = buf[pos]
                pos += 1
            elif statemode == STATE_TEXTURE:
                #NOTE: this is an index into the list 'data.tex'
                self.texture = buf[pos]
                pos += 1
            else:
                print('#WARNING: unsupported geostate attribute; this geostate may be messed up as a result')

def readGstate(version,f):
    gstate = Gstate_data()
    gstate.read(version,f)
    return gstate


def readLlist(version,f):
    buf = readInt32Array(f,3)
    size = buf[0]
    llist = readInt32Array(f,size)
    return llist

def readVlist(version,f):
    buf = readInt32Array(f,3)
    size = buf[0]
    vlist = readPfVec3Array(f,size)
    return vlist

def readClist(version,f):
    buf = readInt32Array(f,3)
    size = buf[0]
    clist = readPfVec4Array(f,size)
    return clist

def readNlist(version,f):
    buf = readInt32Array(f,3)
    size = buf[0]
    nlist = readPfVec3Array(f,size)
    return nlist

def readTlist(version,f):
    buf = readInt32Array(f,3)
    size = buf[0]
    tlist = readPfVec2Array(f,size)
    return tlist

def readIlist(version,f):
    buf = readInt32Array(f,3)
    size = buf[0]
    ilist = readUInt16Array(f,size)
    return ilist


class modelData:
    def __init__(self):
        self.node = []
        self.mtl = []
        self.gset = []
        self.gstate = []
        self.llist = []
        self.vlist = []
        self.clist = []
        self.nlist = []
        self.tlist = []
        self.ilist = []
        self.tex = []



f = open(sys.argv[1],'rb')

magicnum = readUInt32(f)
print('#magic number = ' + hex(magicnum))
if magicnum == PFB_MAGIC_NUMBER_LE:
    ENDIAN_FLAG = '<'
version = readUInt32(f)
print(f'#pfb version {version}')
dummy = readInt32(f)
byteoffset = readInt32(f)
f.seek(byteoffset,0)

data = modelData()

while True:
    try:
        listtype = readInt32(f)
        numobjects = readInt32(f)
        numbytes = readInt32(f)
        print(f'#list type {l_name[listtype]}, {numobjects} objects, {numbytes} bytes')
        if listtype == L_TEX:
            for i in range(numobjects):
                data.tex.append(readTex(version,f))
        elif listtype == L_NODE:
            for i in range(numobjects):
                data.node.append(readNode(version,f,i))
        elif listtype == L_MTL:
            for i in range(numobjects):
                data.mtl.append(readMtl(version,f))
        elif listtype == L_GSET:
            print(f"GSET list found of {numobjects} geosets.")
            for i in range(numobjects): #debug
                print(f"   ========== Reading gset n. {i}")
                try:
                    # Chiamata con parametro "debug" - usa un valore booleano invece della stringa
                    # Per attivare la modalità debug, chiama readGset(version, f, True)
                    data.gset.append(readGset(version, f, True))  # Cambia False in True per debug
                    print(f"   Done n. {i}")
                except Exception as e:
                    #print(f"**** Error reading gset n. {i}: '{e}'")
                    traceback.print_exc()
        elif listtype == L_GSTATE:
            for i in range(numobjects):
                data.gstate.append(readGstate(version,f))
        elif listtype == L_LLIST:
            for i in range(numobjects):
                data.llist.append(readLlist(version,f))
        elif listtype == L_VLIST:
            for i in range(numobjects):
                data.vlist.append(readVlist(version,f))
        elif listtype == L_CLIST:
            for i in range(numobjects):
                data.clist.append(readClist(version,f))
        elif listtype == L_NLIST:
            for i in range(numobjects):
                data.nlist.append(readNlist(version,f))
        elif listtype == L_TLIST:
            for i in range(numobjects):
                data.tlist.append(readTlist(version,f))
        elif listtype == L_ILIST:
            for i in range(numobjects):
                data.ilist.append(readIlist(version,f))
        else:
            print(f'#  currently unsupported list type "{listtype}"- skipping {numbytes} bytes')
            f.read(numbytes)
    except Exception as error:
        break

f.close()




obj_filename = sys.argv[2]
if obj_filename[-4:] == '.obj':
    mtl_filename = obj_filename[:-4] + '.mtl'
else:
    mtl_filename = obj_filename + '.mtl'

mtl_file = open(mtl_filename,'w')

i=0
for gstate in data.gstate:
    mtl_file.write(f'newmtl gstate{i}\n')
    if gstate.frontmtl > -1:
        mtl = data.mtl[gstate.frontmtl]
        mtl_file.write(f'Ka {mtl.ambient[0]} {mtl.ambient[1]} {mtl.ambient[2]}\n')
        mtl_file.write(f'Kd {mtl.diffuse[0]} {mtl.diffuse[1]} {mtl.diffuse[2]}\n')
        mtl_file.write(f'Ks {mtl.specular[0]} {mtl.specular[1]} {mtl.specular[2]}\n')
        mtl_file.write(f'Ns {mtl.shininess}\n')
    if gstate.texture > -1:
        tex = data.tex[gstate.texture]
        pngfile = tex.filename.replace('.sgi','.png')
        mtl_file.write(f'map_Kd {pngfile}\n')
    mtl_file.write('\n')
    i += 1

mtl_file.close()

print("\n ====== Creating OBJ file =======")

obj_file = open(obj_filename,'w')
obj_file.write(f'mtllib {mtl_filename}\n')

def write_flat_tristrips_to_obj(lengths, vertices, vertex_offset=0, ccw=True):
# NOT WORKING!!  DEBUG
    """
    Write PFGS_FLAT_TRISTRIPS geometry into OBJ file

    Args:
        lengths: number of vertices per polygon
        vertices: {'x', 'y', 'z'} list
        vertex_offset: offset to add to indexes (perché OBJ è 1-based e accumulativo)
        ccw: True s= front face
    """


    # Consistency check
    expected_total = sum(lengths)
    if len(vertices) != expected_total:
        raise ValueError(f"Numero di vertici ({len(vertices)}) non corrisponde a somma di lengths ({expected_total})")

    current_index = 0
    for poly_idx, num_verts in enumerate(lengths):
        if num_verts < 3:
            continue  # skip degenerated polygons

        # Extract vertices for this poly
        poly_vertices = vertices[current_index : current_index + num_verts]


        # Create indexes lst (1-based, with offset)
        indices = [str(vertex_offset + current_index + i + 1) for i in range(num_verts)]

        if not ccw:
            # Inverti l'ordine (mantenendo il primo fisso per strip? No, per faccia basta invertire)
            indices = [indices[0]] + indices[:0:-1]  # oppure semplicemente indices[::-1]
            # Ma per una faccia chiusa, invertire tutta la lista è sufficiente:
            indices = indices[::-1]

        # Write face: f v1 v2 v3 ...
        face_line = "f " + " ".join(indices) + "\n"
        obj_file.write(face_line)

        current_index += num_verts


def print_tristrip_triangle(firstindex, normal_mode, texc_mode, ccw):
    if ccw:
        if texc_mode == PFGS_OFF:
            obj_file.write(f'f {firstindex+1}//{firstindex+1} {firstindex+2}//{firstindex+2} {firstindex+3}//{firstindex+3}\n')
        else:
            obj_file.write(f'f {firstindex+1}/{firstindex+1}/{firstindex+1} {firstindex+2}/{firstindex+2}/{firstindex+2} {firstindex+3}/{firstindex+3}/{firstindex+3}\n')
    else:
        if texc_mode == PFGS_OFF:
            obj_file.write(f'f {firstindex+1}//{firstindex+1} {firstindex+3}//{firstindex+3} {firstindex+2}//{firstindex+2}\n')
        else:
            obj_file.write(f'f {firstindex+1}/{firstindex+1}/{firstindex+1} {firstindex+3}/{firstindex+3}/{firstindex+3} {firstindex+2}/{firstindex+2}/{firstindex+2}\n')



numverts = 0

nodeCounter = -1
for n in data.node:
    nodeCounter = nodeCounter + 1
    print(f"\n=================")
    print(f"Processing node n. {nodeCounter}")
    if n.type == N_GEODE:
        print(f"   Geode detected: creating {len(n.gsets)} meshes from  {len(n.gsets)} geosets")
        geosetsCount = -1
        for g in n.gsets:
            geosetsCount = geosetsCount + 1;
            print(f"      Geoset n. {geosetsCount}")
            coords = []
            norms = []
            texc = []
            lens = []
            gset = data.gset[g]
            print(f"        Geoset is made of {gset.pcount} primitives of type {gset.ptype} ({gspt_table_strings[gset.ptype]})")
            obj_file.write(f'#gset type {gset.ptype}   numprims {gset.pcount}   gstate {gset.gstate}\n')

            if gset.llist != -1:
                print("        Writing lengths")
                lens = data.llist[gset.llist]
                obj_file.write(f'#  lenlist: {lens}\n')
            if gset.vlist[1] != -1:
               print("        Writing vertices")
               coords = data.vlist[gset.vlist[1]]
            else:
               print("        (no data, skipping geoset)")
               continue    # i.e. if there's no list of vertices, just skip this geoset
            if gset.vlist[2] != -1:
                print("        Writing indices")
                indices = data.ilist[gset.vlist[2]]
                coords = [coords[i] for i in indices]
            vstart = numverts
            for v in coords:
                obj_file.write(f'v {v[0]} {v[1]} {v[2]}\n')
                numverts += 1
#NOTE: this code assumes that normals & texcoords are per-vertex.  Support for PFGS_OVERALL and PFGS_PER_PRIM will need to be added.

            print("        Processing normals...")
            normal_mode = gsb_table[gset.nlist[0]]
            if normal_mode != PFGS_PER_VERTEX:
                obj_file.write('          ####WARNING: unsupported normal mode !!!!\n')
            if gset.nlist[1] != -1:
                print("           Extracting normals")
                norms = data.nlist[gset.nlist[1]]
                if gset.nlist[2] != -1:
                    print("           Extracting indices")
                    indices = data.ilist[gset.nlist[2]]
                    norms = [norms[i] for i in indices]
                print("           Writing to file")
                for n in norms:
                    obj_file.write(f'vn {n[0]} {n[1]} {n[2]}\n')

            print("        Processing colors...")
            texc_mode = gsb_table[gset.tlist[0]]
            if (texc_mode != PFGS_PER_VERTEX) and (texc_mode != PFGS_OFF):
                obj_file.write('          #WARNING: unsupported texture coordinate mode !!!!\n')
            if gset.tlist[1] != -1:
                print("           Extracting colors... ")
                texc = data.tlist[gset.tlist[1]]
                if gset.tlist[2] != -1:
                    print("           Extracting indices...")
                    indices = data.ilist[gset.tlist[2]]
                    texc = [texc[i] for i in indices]
                print("           Writing to file")
                for t in texc:
                    obj_file.write(f'vt {t[0]} {t[1]}\n')

            if (len(coords) != len(norms)):
                obj_file.write('#ERROR: coords <> normals - only per-vertex is supported !!!!\n')
                print('#ERROR: coords <> normals - only per-vertex is supported !!!!\n')
            if (len(coords) != len(texc)):

                obj_file.write('#ERROR: coords <> texc - only per-vertex is supported !!!!\n')
                print('#ERROR: coords <> texc - only per-vertex is supported !!!!\n')

#NOTE: should look up how pfGSetGStateIndex() works (if gstate[1] is not -1); probably none of our models use that feature, however
            if gset.gstate[0] != -1:
                obj_file.write(f'usemtl gstate{gset.gstate[0]}\n')
            if gspt_table_strings[gset.ptype] == "PFGS_TRISTRIPS":
                print(f"        Primitive of type {gspt_table_strings[gset.ptype]} is supported! Creating faces...")
                stripstart = vstart
                for striplen in lens:
                    vertindex = stripstart
                    ccw = True
                    for tri in range(striplen-2):
                        print("          Writing faces to file")
                        print_tristrip_triangle(vertindex, normal_mode, texc_mode, ccw)
                        vertindex += 1
                        ccw = not ccw
                    stripstart += striplen
            elif gspt_table_strings[gset.ptype] == "PFGS_FLAT_TRISTRIPS": ######################################################################
                print("        :-( PFGS_FLAT_TRISTRIPS to be implemented, attempting...")
                write_flat_tristrips_to_obj(lens, coords)
            else:
                print("=== WARNING! Only PFGS_TRISTRIPS supported, no mesh drawn or this geoset, only pointcloud will be shown")
        print ("   Geosets finised")
    elif n.type == N_LOD:
        print(f"   LOD")
        for r in n.ranges:
            print(f"      Range")
    else:
        node_name = node_type_dict.get(n.type, f"UNKNOWN_NODE_{n.type}")
        print (f"--------- (non-Geode, skipping node of type {n.type} ({node_name}))")
        print (" ")
print("Nodes finished, OBJ file ready.")

obj_file.close()

