import sys
from final_project import util


def initiate_delete(database):
    table = input('Delete: \n'
                  'Table name: ').lower()
    if table == 'q':
        util.exit_TEAL(database)
    elif table == 'land':
        delete_land(database)
    elif table == 'county':
        delete_county(database)
    elif table == 'improvement':
        delete_improvement(database)
    elif table == 'owner':
        delete_owner(database)
    elif table == '':
        sys.stdout.write('Table must be specified for delete')
        initiate_delete(database)
    else:
        sys.stdout.write('Did not recognize table name. Please specify table in database: \n'
                         'land\n'
                         'county\n'
                         'improvement\n'
                         'owner\n')
        initiate_delete(database)


def delete_land(database):
    delete_on = input("Deleting from land. Specify deletion attribute: \n\t"
                      "Delete table: t\n"
                      "Delete on id: id\n"
                      "Delete on quality rating: r\n").lower()

    if delete_on == 'q':
        util.exit_TEAL(database)
    elif delete_on == 't':
        database.delete_table('land')


def delete_county(database):
    delete_on = input("Deleting from county. Specify deletion attribute: \n\t"
                      "Delete table: t\n"
                      "Delete on id: id\n"
                      "Delete on name: n\n").lower()
    if delete_on == 'q':
        util.exit_TEAL(database)
    elif delete_on == 't':
        database.delete_table('county')


def delete_improvement(database):
    delete_on = input("Deleting from improvement. Specify deletion attribute: \n\t"
                      "Delete table: t\n"
                      "Delete on id: id\n"
                      "Delete on improvement_type: it\n").lower()
    if delete_on == 'q':
        util.exit_TEAL(database)
    elif delete_on == 't':
        database.delete_table('improvement')


def delete_owner(database):
    delete_on = input("Deleting from owner. Specify deletion attribute: \n\t"
                      "Delete table: t\n"
                      "Delete on id: id\n"
                      "Delete on name: n\n").lower()
    if delete_on == 'q':
        util.exit_TEAL(database)
    elif delete_on == 't':
        database.delete_table('owner')