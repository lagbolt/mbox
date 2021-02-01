import mailbox
import argparse
import sys

def dumpmsg(k, m, ofile):
   print(10*'=', "Dumping message", k, len(m), type(m), 10*'=', file=ofile)
   for p in m.walk():
      print(">>>>> Walk: ", type(p), file=ofile)
      for f,v in p.items():
         print(f, '///', v[0:200], file=ofile)
      if not p.is_multipart():
            print("PAYLOAD:", p.get_payload()[0:50], file=ofile)

parser = argparse.ArgumentParser()
parser.add_argument("--input", "-i", help="Input filename")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--stop", "-s", type=int, help="Stop every n messages")
group.add_argument("--output", "-o", help="Output filename")

args = parser.parse_args()

mb = mailbox.mbox(args.input)

outputfile = open(args.output, 'w') if args.output else sys.stdout

for i, (k, msg) in enumerate(mb.iteritems()):
   dumpmsg(k, msg, outputfile)
   if args.stop and not ((i+1) % int(args.stop)):
      input("Hit return for next message: ")