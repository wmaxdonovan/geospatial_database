import sys
from final_project import util
from final_project.TEAL import user_prompt


def initiate_delete(database):
    try:
        table = input('Delete: \n\t'
                      'Table name: \t').lower()
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
            sys.stdout.write('Table must be specified for delete\t')
            initiate_delete(database)
        else:
            sys.stdout.write('Did not recognize table name. Please specify table in database: \n\t'
                             'land\n\t'
                             'county\n\t'
                             'improvement\n\t'
                             'owner\n\t')
            initiate_delete(database)
    except Exception as e:
        print("Encountered error: ", e, "while attempting delete.")
        initiate_delete(database)
    repeat(database)


def delete_land(database):
    delete_on = input("Deleting from land. Specify deletion attribute: \n\t"
                      "Delete table: t\n\t"
                      "Delete on id: id\n\t"
                      "Delete on county_id: cid\n\t"
                      "Delete on owner_id: oid\n\t"
                      "Delete on quality rating: r\n\t"
                      "Delete on area: a\n\t").lower()

    if delete_on == 'q':
        util.exit_TEAL(database)
    elif delete_on == 't':
        database.delete_table('land')
    elif delete_on == 'id':
        delete_id = input('id to delete: \t')
        if delete_id.isdigit():
            database.delete_item('land', 'id', '=' + delete_id)
        else:
            sys.stdout.write('id must be an integer')
            delete_land(database)
    elif delete_on == 'cid':
        delete_cid = input('delete on cid (accepts range using <, >, =): \t')
        database.delete_item('land', 'county_id', delete_cid)
    elif delete_on == 'oid':
        delete_oid = input('delete on oid (accepts range using <, >, =): \t')
        database.delete_item('land', 'owner_id', delete_oid)
    elif delete_on == 'r':
        delete_rating = input('delete on rating (accepts range using <, >, =): \t')
        database.delete_item('land', 'rating', delete_rating)
    elif delete_on == 'a':
        delete_area = input('delete on area (accepts range using <, >, =): \t')
        database.delete_item('land', 'area', delete_area)
    else:
        sys.stdout.write("Did not recognize selection.\t")
        delete_land(database)

    repeat(database)


def delete_county(database):
    delete_on = input("Deleting from county. Specify deletion attribute: \n\t"
                      "Delete table: t\n\t"
                      "Delete on id: id\n\t"
                      "Delete on name: n\n\t"
                      "Delete on population: p\n\t"
                      "Delete on growth rate: gr\n\t").lower()
    if delete_on == 'q':
        util.exit_TEAL(database)
    elif delete_on == 't':
        database.delete_table('county')
    elif delete_on == 'id':
        delete_id = input('id to delete: \t')
        if delete_id.isdigit():
            database.delete_item('county', 'id', '=' + delete_id)
        else:
            sys.stdout.write('id must be an integer\t')
            delete_land(database)
    elif delete_on == 'n':
        delete_name = input('name to delete: \t')
        database.delete_item('county', 'name', '= "' + delete_name + '"')
    elif delete_on == 'p':
        delete_pop = input('population to delete (accepts range using >, <, =): \t')
        database.delete_item('county', 'pop', delete_pop)
    elif delete_on == 'gr':
        delete_gr = input('growth rate to delete (accepts range using >, <, =): \t')
        database.delete_item('county', 'growth_rate', delete_gr)
    else:
        sys.stdout.write("\tDid not recognize selection.\t")
        delete_county(database)

    repeat(database)


def delete_improvement(database):
    delete_on = input("Deleting from improvement. Specify deletion attribute: \n\t"
                      "Delete table: t\n\t"
                      "Delete on id: id\n\t"
                      "Delete on improvement_type: it\n\t"
                      "Delete on cost: c\n\t"
                      "Delete on improvement level: i\n\t").lower()
    if delete_on == 'q':
        util.exit_TEAL(database)
    elif delete_on == 't':
        database.delete_table('improvement')
    elif delete_on == 'id':
        delete_id = input('id to delete: \t')
        if delete_id.isdigit():
            database.delete_item('improvement', 'id', '=' + delete_id)
        else:
            sys.stdout.write('id must be an integer\t')
            delete_land(database)
    elif delete_on == 'it':
        delete_improvement_type = input("improvement type to delete: \t").lower()
        database.delete_item('improvement', 'improvement_type', '= "' + delete_improvement_type + '"')
    elif delete_on == 'c':
        delete_cost = input('cost to delete (accepts range using >, <, =): \t')
        database.delete_item('improvement', 'cost', delete_cost)
    elif delete_on == 'i':
        delete_i = input('improvement level to delete (accepts range using >, <, =): \t')
        database.delete_item('improvement', 'improvement', delete_i)
    else:
        sys.stdout.write("\tDid not recognize selection.\t")
        delete_improvement(database)

    repeat(database)


def delete_owner(database):
    delete_on = input("Deleting from owner. Specify deletion attribute: \n\t"
                      "Delete table: t\n\t"
                      "Delete on id: id\n\t"
                      "Delete on status: s\n\t"
                      "Delete on name: n\n\t").lower()
    if delete_on == 'q':
        util.exit_TEAL(database)
    elif delete_on == 't':
        database.delete_table('owner')
    elif delete_on == 'id':
        delete_id = input('id to delete: \t')
        if delete_id.isdigit():
            database.delete('land', 'id', '=' + delete_id)
        else:
            sys.stdout.write('id must be an integer\t')
            delete_land(database)
    elif delete_on == 's':
        delete_status = input('status to delete (private/public): \t')
        database.delete_item('owner', 'status', '= "' + delete_status + '"')
    elif delete_on == 'n':
        delete_name = input('name to delete: \t')
        database.delete_item('owner', 'name', '= "' + delete_name + '"')
    else:
        sys.stdout.write("Did not recognize selection.\t")
        delete_owner(database)

    repeat(database)


def repeat(database):
    repeat_delete = input("\tDelete again (y/n)?: ").lower()
    if repeat_delete == 'q':
        util.exit_TEAL(database)
    elif repeat_delete == 'y':
        initiate_delete(database)
    else:
        user_prompt.interact(database)
