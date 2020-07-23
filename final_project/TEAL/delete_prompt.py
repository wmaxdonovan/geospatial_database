from final_project import util


def initiate_delete(database):
    table = input('Delete: \n'
                  'Table name: ').lower()
    if table == 'q':
        util.exit_TEAL(database)
    elif table == 'land':
        insert_land(database)
    elif table == 'county':
        insert_county(database)
    elif table == 'improvement':
        insert_improvement(database)
    elif table == 'owner':
        insert_owner(database)
    elif table == '':
        sys.stdout.write('Table must be specified for insert')
        initiate_insert(database)
    else:
        sys.stdout.write('Did not recognize table name. Please specify table in database: \n'
                         'land\n'
                         'county\n'
                         'improvement\n'
                         'owner\n')
        initiate_insert(database)
