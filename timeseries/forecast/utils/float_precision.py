
def value_precision_str(value, precision=3, precision_big=1):
    value_precision = precision_big if value >= 100 else precision
    if value_precision == 0:
        return str(int(value))
    else:
        return f"{value:.{value_precision}f}"
