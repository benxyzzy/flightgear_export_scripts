import operator

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
                # Possible block of verts found
                this_numvert = int(line.split()[1])
                if this_numvert > 0:
                    numvert = this_numvert
                    verts_stored = 0

    return verts


def reverse_scale_factor(scale_factor_verts_dict):
    """
    If you apply different scale factors to a list of verts,
    and store them in a dict with the scale factor as the key,
    then this function returns a dict with the scaling undone.

    :param scale_factor_verts_dict: takes the format of e.g.
        {'0.001': [[6496.5029, 5234.999199999999, 48231.433899999996],
                   [6496.5029, 53.703, 48231.433899999996],
                   [-6503.4981, 53.704, 48231.433899999996]],
         '0.01': [[649.65029, 523.49992, 4823.14339],
                  [649.65029, 5.3703, 4823.14339],
                  [-650.3498099999999, 5.3704, 4823.14339]],
         '0.05': [[129.930058, 104.69998399999999, 964.6286779999999],
                  [129.930058, 1.07406, 964.6286779999999],
                  [-130.06996199999998, 1.07408, 964.6286779999999]]}
    :returns: a dict with the same format and keys, but where the scaling on each element has been reversed.
    """
    orig_verts = {}
    for scale_factor, verts_list in scale_factor_verts_dict.items():
        sf = float(scale_factor)

        try:
            orig_verts[scale_factor] = [
                [v/sf for v in verts]
                for verts in verts_list
            ]
        except TypeError as ex:  # 'float' object is not iterable
            # Now we can reverse lists of scalars as well as lists of verts
            orig_verts[scale_factor] = [v/sf for v in verts_list]

    return orig_verts
