// Add a startWith method to strings
if (typeof String.prototype.startsWith != 'function') {
  String.prototype.startsWith = function (str){
    return this.indexOf(str) == 0;
  };
}

if (typeof Number.prototype.formatThousands != 'function') {
    Number.prototype.formatThousands = function(c, d, t) {
        var n = this,
            // Parse arguments.
            // - Amount of decimals.
            c = isNaN(c = Math.abs(c)) ? 2 : c,

            // - Decimal separator.
            d = d == undefined ? "." : d,

            // - Thousands separator.
            t = t == undefined ? "," : t,

            // If it is less than 0, put a negative sign.
            s = n < 0 ? "-" : "",

            // Keep only c decimals.
            i = parseInt(n = Math.abs(+n || 0).toFixed(c)) + "",

            // Where to put the first thousands separator.
            j = (j = i.length) > 3 ? j % 3 : 0;

       return s
              + (j ? i.substr(0, j) + t : "") 
              + i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + t) 
              + (c ? d + Math.abs(n - i).toFixed(c).slice(2) : "");
    }
}

round = function(x, places) {
    x = x * Math.pow(10, places);
    x = Math.round(x)
    x =  x / Math.pow(10, places);
    return x;
}


check_before_fmt = function(v, func) {
    if(v == undefined) {
        return "-";
    }

    if(isNaN(v)) {
        if(v.indexOf("<") == 0) {
            return v;
        }
        return "-";
    }

    return func(v);
}

r0 = function(v) {
    return check_before_fmt(v, function(v) {return v.formatThousands(0);});
}

r0nt = function(v) {
    return check_before_fmt(v, Math.round(v));
}

r1 = function(v) {
    return check_before_fmt(v, function(v) {return v.formatThousands(1);});
}
r2 = function(v) {
    return check_before_fmt(v, function(v) {return v.formatThousands(2);});
}

r12 = function(v) {
    return check_before_fmt(v, function(v) {
        if (v < 1000000) 
            return v.formatThousands(2);
        return v.formatThousands(1);
    });
}

niz = function(v) {
    if (isNaN(v)) return 0;
    return v;
}

noz = function(v) {
    if (v == undefined)
        return 0
    return v
}



