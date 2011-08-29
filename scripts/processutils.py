def process_svg_template(context, template_xml):
    for (key, value) in context.items():
        template_xml = template_xml.replace('{%s}' % key, value)

    return template_xml

def check_numeric(fn):
    def _check_numeric(x):
        if (x == None or str(x).strip() == ""):
            return "0"
        else:
            return fn(x)
    return _check_numeric


# formatting functions
none_is_zero = lambda x : 0 if x == None else float(x)
fmt_pop = lambda x : str(round(x / 1000000.0, 1))

@check_numeric
def fmt_1000(x): return "{:,.0f}".format(float(x) * 1000)

@check_numeric
def fmt_perc(x): return str(round(x * 100, 1))

@check_numeric
def fmt_perc0(x): return str(int(round(x * 100, 0)))

@check_numeric
def fmt_r0(x): return str(round(x, 0))

@check_numeric
def fmt_r1(x): return "{:,.1f}".format(float(x))

@check_numeric
def fmt_r2(x): return str(round(x, 2)) 

class xmlutils(object):
    @staticmethod
    def get_el_by_id(dom, elname, id):
        elements = dom.getElementsByTagName(elname)
        match = [el for el in elements if el.hasAttribute("id") and el.attributes["id"].value == id]
        return None if len(match) == 0 else match[0]

class numutils(object):
    @staticmethod
    def condround(val):
        if val < 0.1:
            return val
        elif val < 1:
            return round(val, 1)
        elif val < 100:
            return round(val)
        else:
            return round(val, -1)
    @staticmethod
    def safediv(num, den):
        if not isinstance(num, numbers.Number) or not isinstance(den, numbers.Number):
            return 0
        if den == 0:
            return 0.0
        else:
            return num / den

