import math

def toPrecision(x,p,sf=True):
    """
    returns a string representation of x formatted with a precision of p

    Based on the webkit javascript implementation taken from here:
    https://code.google.com/p/webkit-mirror/source/browse/JavaScriptCore/kjs/number_object.cpp
    """

    if isinstance(x,list):
        out_list = []
        for item in x:
            out_list.append(toPrecision(item,p,sf=sf))
        return str(out_list).replace("'","")

    try:
        x = float(x)
    except ValueError:
        return x
    except TypeError:
        return x

    if sf:
        try:
            x = float(x)

            if x == 0.:
                return "0." + "0"*(p-1)

            out = []

            if x < 0:
                out.append("-")
                x = -x

            e = int(math.log10(x))
            tens = math.pow(10, e - p + 1)
            n = math.floor(x/tens)

            if n < math.pow(10, p - 1):
                e = e -1
                tens = math.pow(10, e - p+1)
                n = math.floor(x / tens)

            if abs((n + 1.) * tens - x) <= abs(n * tens -x):
                n = n + 1

            if n >= math.pow(10,p):
                n = n / 10.
                e = e + 1

            m = "%.*g" % (p, n)

            if e < -2 or e >= p:
                out.append(m[0])
                if p > 1:
                    out.append(".")
                    out.extend(m[1:p])
                out.append('e')
                if e > 0:
                    out.append("+")
                out.append(str(e))
            elif e == (p -1):
                out.append(m)
            elif e >= 0:
                out.append(m[:e+1])
                if e+1 < len(m):
                    out.append(".")
                    out.extend(m[e+1:])
            else:
                out.append("0.")
                out.extend(["0"]*-(e+1))
                out.append(m)

            return "".join(out)
        except ValueError:
            format_str = "{:."+str(p)+"f}"
            return format_str.format(round(x,p))   
    else:
        format_str = "{:."+str(p)+"f}"
        return format_str.format(round(x,p))

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
