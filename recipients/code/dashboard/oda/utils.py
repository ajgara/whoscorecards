def safe_div(a, b):
    try:
        return float(a) / float(b)
    except:
        return None

def safe_mul(a, b):
    try:
        return float(a) * float(b)
    except:
        return None