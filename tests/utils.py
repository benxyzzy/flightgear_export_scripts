def parse_verts_from_ac(f):
    """
    Take an opened AC file (or contents as a list of lines) and return all the verts.
    They are returned in the same order as they appear in the file, so can be used to compare files by their verts.
    """
    verts = []

    numvert = None
    verts_stored = None
    for line in f:
        if numvert is not None:
            # We're in a block of verts
            verts.append([float(el) for el in line.split()])
            verts_stored += 1
            if verts_stored == numvert:
                # end of block of verts
                numvert = None
                verts_stored = None
        else:
            # We're not in a block of verts
            if line.startswith("numvert"):
                # block of verts found
                numvert = int(line.split()[1])
                verts_stored = 0

    return verts
