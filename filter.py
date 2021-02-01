#
#  The tests below ignore case
#

def field_exists(msg, fld) -> bool:
    return bool(msg.get(fld, None))

def field_includes(msg, fld, match_value) -> bool:
    return match_value.upper() in msg.get(fld,'').upper()

def field_equals(msg, fld, match_value) -> bool:
    return match_value.upper() == msg.get(fld, '').upper()

def messagefilter(msg) -> bool:
    return (
        field_includes(msg, "Subject", "[CODE4LIB] Job")
    )