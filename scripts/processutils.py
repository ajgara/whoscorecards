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
def fmt_r0(x): return str(round(x, 0))

@check_numeric
def fmt_r1(x): return "{:,.1f}".format(float(x))

@check_numeric
def fmt_r2(x): return str(round(x, 2)) 
