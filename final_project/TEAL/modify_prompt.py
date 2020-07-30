import sys
from final_project import util
from final_project.TEAL import user_prompt


def initiate_modify(database):
    table = input('Modify: \n\t'
                  'Table name: \t').lower()
    if table == 'q':
        util.exit_TEAL(database)
    elif table == 'land':
        modify_land(database)
    elif table == 'county':
        modify_county(database)
    elif table == 'improvement':
        modify_improvement(database)
    elif table == 'owner':
        modify_owner(database)
    elif table == '':
        sys.stdout.write('Table must be specified for modify\t')
        initiate_modify(database)
    else:
        sys.stdout.write('Did not recognize table name. Please specify table in database: \n\t'
                         'land\n\t'
                         'county\n\t'
                         'improvement\n\t'
                         'owner\n\t')
        initiate_modify(database)

    repeat(database)

    
def modify_land(database):
    pass


def modify_county(database):
    pass


def modify_owner(database):
    pass


def modify_improvement(database):
    pass


def repeat(database):
    repeat_modify = input("\tmodify again (y/n)?: ").lower()
    if repeat_modify == 'q':
        util.exit_TEAL(database)
    elif repeat_modify == 'y':
        initiate_modify(database)
    else:
        user_prompt.interact(database)
