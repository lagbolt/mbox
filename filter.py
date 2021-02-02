# 
#    Version:  0.1.0  2/1/21
#
#    License:  CC BY-NC-SA 4.0, https://creativecommons.org/licenses/by-nc-sa/4.0/
#
#    Graeme Williams
#    carryonwilliams@gmail.com
#
#  The mboxtocsv command uses the messagefilter function in this file
#  to filter which messages to write to the output.
#  

def field_exists(msg, fld) -> bool:
    return bool(msg.get(fld, None))

def field_includes(msg, fld, match_value, ignoreCase=True) -> bool:
    if ignoreCase:
        return match_value.upper() in msg.get(fld,'').upper()
    else:
        return match_value in msg.get(fld,'')

def field_equals(msg, fld, match_value, ignoreCase=True) -> bool:
    if ignoreCase:
        return match_value.upper() == msg.get(fld, '').upper()
    else:
        return match_value == msg.get(fld, '')

# An email message will be included in the output if this function returns True
def messagefilter(msg) -> bool:
    return (
        field_includes(msg, "Subject", "[CODE4LIB] Job")
    )