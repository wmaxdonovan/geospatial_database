import sys
from final_project import util


def initiate_insert():
    table = input('Insert: \n'
                  'If you do not wish to specify an input, press enter \n'
                  'Table name: ').lower()
    if table == 'q':
        util.exit_TEAL()
    elif table == 'land':
        pass
    elif table == 'county':
        pass
    elif table == 'improvement':
        pass
    elif table == 'owner':
        pass
    elif table == '':
        sys.stdout.write('Table must be specified for insert')
        initiate_insert()
