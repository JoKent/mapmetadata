## script to read the gdas export xl sheet and convert to a MARC file 
import sys
import os
import csv
import datetime
import argparse 
from pymarc import Record, Field, Subfield, Indicators, Leader
from pymarc import TextWriter


def gdasmarcwriter(infile, outfile):
    writer = TextWriter(open(outfile,'wt'))
    with open(infile, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            record = Record()
            record.leader = Leader("     nem a22     5u 4500")
            record.add_field(Field(tag='005', data=datetime.datetime.now().strftime("%Y%m%d%H%M%S")+'.0'))
            record.add_field(Field(tag='007', data='aj |||||'))
            record.add_field(Field(tag='007', data='cr c|||||a|na|'))
            if row['F008_field']:
                record.add_field(Field(tag='008', data='260202'+row['F008_field']))
            record.add_field(Field(tag = '034', indicators = Indicators('0','#'), 
                subfields = [ Subfield(code='a', value='a'),
                            Subfield(code='d', value=row['034_d']), 
                            Subfield(code='e', value=row['034_e']), 
                            Subfield(code='f', value=row['034_f']), 
                            Subfield(code='g', value=row['034_g']) ] ))
            if row['referenceId']:
                record.add_field(Field(tag = '035', indicators = Indicators('#','#'), subfields = [Subfield(code='a', value='(uk)'+row['referenceId'])]))
            record.add_field(Field(tag = '040', indicators = Indicators('#','#'), subfields = [Subfield(code='a', value='uk'),Subfield(code='b', value='eng'),Subfield(code='c', value='uk')]))
            record.add_field(Field(tag = '052', indicators = Indicators('#','#'), subfields = [Subfield(code='a', value='uk'),Subfield(code='b', value='eng')]))
            record.add_field(Field('110  '+row['F110']))
            record.add_field(
            Field(tag = '245',
                indicators = Indicators('1','0'),
                subfields = [
                    Subfield(code='a', value=row['marcTitle_245a']),
                    Subfield(code='h', value='[electronic resource] /'),
                    Subfield(code='c', value=row['marcPublisher']+'.')
                    ]))
            if row['F250a_edition_']:
                record.add_field(Field(tag = '250', indicators = Indicators('#','#'),
                        subfields = [Subfield(code='a', value=row['F250a_edition_'])]))
            if row['F255']:
                record.add_field(Field('255  ##'+row['F255']))
            if row['F264_1']:
                record.add_field(Field('264  #1'+row['F264_1'].replace(':$b',' :$b')))
            record.add_field(Field('300  ##$a1 geospatial database'))
            record.add_field(Field('336  ##$acartographic image$2rdacontent'))
            record.add_field(Field('336  ##$acartographic dataset$2rdacontent'))
            record.add_field(Field('337  ##$acomputer$2rdamedia'))
            record.add_field(Field('338  ##$aonline resource$2rdacarrier'))
            if row['F342_00']:
                record.add_field(Field('342  00'+row['F342_00']))
            if row['F342_01']:
                record.add_field(Field('342  01'+row['F342_01']))
            if row['F342_02']:
                record.add_field(Field('342  02'+row['F342_02']))
            if row['F342_05']:
                record.add_field(Field('342  05'+row['F342_05']))
            if row['F651']:
                record.add_field(Field('651  #0'+row['F651'].replace('\\','$').replace('$0','').replace('$a ','$a')))
            if row['F651_1']:
                record.add_field(Field('651  #0'+(row['F651_1'].replace('\\','$').replace('$a ','$a'))))
            if row['F651_2']:
                record.add_field(Field('651  #7'+row['F651_2'].replace('\\','$').replace('$z ','$z').replace('$a ','$a').replace('$2 ','$2').replace('0 (','0(')))
            # if row['F651_3']:
            #     record.add_field(Field('651  #7'+row['F651_3'].replace('\\','$').replace('$a ','$a')))
            if row['F655_1']:
                record.add_field(Field('655  #7'+row['F655_1'].replace('\\','$').replace('$a ','$a').replace('$2 ','$2')))
            if row['F655_2']:
                record.add_field(Field('655  #7'+row['F655_2'].replace('\\','$').replace('$a ','$a').replace('$2 ','$2')))
            if row['F655_3']:
                record.add_field(Field('655  #7'+row['F655_3'].replace('\\','$').replace('$a ','$a').replace('$2 ','$2')))
            if row['Deeplinks URL']:
                record.add_field(Field('856  40$u'+row['Deeplinks URL']))
            writer.write(record)
    writer.close()
    with open(outfile, "r") as file:
        mrk = file.read().replace("  \\\\", "")
    with open(outfile, "w") as file:
        file.write(mrk)



def main():
    parser = argparse.ArgumentParser(description="Process an input csv and save results to a mrk file.")
    parser.add_argument("inputfile", help="Path to the input csv file.")
    parser.add_argument("outputfile", help="Path to the output mrk file.")
    args = parser.parse_args()

    # Validate that infile exists and is a file
    if not os.path.isfile(args.inputfile):
        print(f"Error: '{args.inputfile}' is not a valid file.", file=sys.stderr)
        sys.exit(1)

    # Ensure output directory exists
    outdir = os.path.dirname(args.outputfile) or "."
    if not os.path.exists(outdir):
        print(f"Error: Output directory '{outdir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    gdasmarcwriter(args.inputfile, args.outputfile)


main()



