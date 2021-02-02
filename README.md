# mbox
A couple of Python programs for interpreting mbox files.

### One important note:

Because their goals are different, the two programs take different approaches to error-handling:  dumpmbox will fail on error, mboxtocsv will _silently_ skip on error.

The two programs have no dependencies outside the standard Python libraries.

## dumpmbox

dumpmbox takes a single mbox file as input.

It can operate in two modes:  it can dump the entire input file, as text, to the output, or it can stop every N messages.

For example:

```
dumpmbox -i example.mbox -o example.txt
dumpmbox -i example.mbox
dumpmbox -i example.mbox --stop 3
```
The first command will convert the input to text and write it to the output file.  The second command will write the output to the console.  The third command will write the output to the console, stopping every 3 messages.

## mboxtocsv

mboxtocsv takes a _list_ of mbox files specified by the -i option (e.g., -i one.mbox two.mbox) and writes an Excel-compatible .csv file specified by the -o option.

Only the messages for which the messagefilter function in filter.py returns True will be included in the output.  You should be able to define whatever logic you want using the utility functions included in filter.py alond with 'and', 'or', 'not' and abundant parentheses.

Only the fields specified by the -f option (e.g., -f Subject Date) are written to the output, plus, if the -b option is included, the message body.

You can see a complete example set of options in example.bat.

Note that characters which cause encoding errors will be skipped, as will messages which failed to be read by the mbox library.  See the code for more details.

At the moment, carriage returns and line feeds in the message body are converted to spaces.  If that isn't what you want, remove the call to translate from the last line of payload_text -- or contact me.

## Questions?

Email me!
