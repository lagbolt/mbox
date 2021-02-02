# 
#    Version:  0.1.0  2/1/21
#
#    License:  CC BY-NC-SA 4.0, https://creativecommons.org/licenses/by-nc-sa/4.0/
#
#    Graeme Williams
#    carryonwilliams@gmail.com
#
#  See the README for instructions about how to use this command
#  

import mailbox
import argparse

# libraries to do character decoding of various sorts
import quopri
import base64
import html

from filter import messagefilter

# quote str so it can be put into a csv file
def quotedquotes(s : str) -> str:
    return '"' + s.replace('"', '""') + '"'

# decode base64 encoded string
# note that character encoding errors are SKIPPED
def b64(b64_string : str) -> str:
    b = base64.b64decode(b64_string)
    return str(b, "utf-8", errors="ignore")

# decode quoted-printable message body
# note that character encoding errors are SKIPPED
def qp(qp_string : str) -> str:
    b = quopri.decodestring(bytes(qp_string, encoding="utf-8"))
    return str(b, "utf-8", errors="ignore")

# for the call to translate in payload_text
translate_table = str.maketrans("\r\nÂ", "   ")

# extract the message body from the message
#   - decode the two formats that we know about
#   - replace carriage return / line feed with space
#   - replace weird Â character with space
#   - unescape things like &amp;
def payload_text(msg):
    # caller ensures msg is text/plain
    cte = msg.get("Content-Transfer-Encoding", None)
    payload = msg.get_payload()
    if cte=="quoted-printable":
        raw_text = qp(payload)
    elif cte=="base64":
        raw_text = b64(payload)
    else:
        raw_text = payload
    return html.unescape(raw_text.translate(translate_table))

def printpayload(m, ofile):
    if (ct := m.get("Content-Type", None)):
        # we assume that multi-part messages don't
        # themselves have payload -- the payload(s)
        # are in the parts
        if (not m.is_multipart()) and ("text/plain" in ct):
            print(quotedquotes(payload_text(m)), file=ofile)
    else:
        print(quotedquotes("No Content-Type"), file=ofile)
        if not m.is_multipart():
            # this is probably some sort of error
            # either in the mbox or our handling
            pass

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", help="Input filename", required=True,
                    nargs="+")
parser.add_argument("--output", "-o", help="Output filename", required=True)
parser.add_argument("--fields", "-f", help="Message fields to include",
                    nargs="*", default=[])
parser.add_argument("--body", "-b", action="store_true", help="Include message body")
args = parser.parse_args()

fields = args.fields

with open(args.output, "w", encoding="utf-8") as outfile:
    headings = fields.copy()
    if args.body:
        headings.append("Message Body")
    print(*headings, sep=",", file=outfile)      # heading row for csv file

    for inputfilename in args.input:
        mb = mailbox.mbox(inputfilename)

        for key in mb.iterkeys():

            try:
                msg = mb.get_message(key)
            except:
                continue       # skip failing messages

            # see filter.py for the definition of this filter,
            # which you can define yourself, if you want
            if not messagefilter(msg):
                continue     # i.e., skip this message

            for f in fields:
                print(quotedquotes(msg.get(f, '')), end=",", file=outfile)
            
            if not args.body:
                continue     # skip further processing
            
            if not msg.is_multipart():
                printpayload(msg, outfile)

            else:
                message_tree = msg.walk()
                if msg.get("Subject", '').startswith("[SPAM"):
                    _ = next(message_tree)     # skip root, which is a spam notification
                    _ = next(message_tree)

                for msgpart in message_tree:
                    printpayload(msgpart, outfile)
        mb.close()