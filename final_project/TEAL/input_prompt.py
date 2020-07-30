import sys
from final_project import util
from final_project.TEAL import user_prompt


def initiate_insert(database):
    try:
        table = input('Insert: \n\t'
                      'If you do not wish to specify an input, press enter \n\t'
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
        elif table == 'governs':
            insert_governs(database)
        elif table == 'owns':
            insert_owns(database)
        elif table == '':
            sys.stdout.write('Table must be specified for insert\n')
            initiate_insert(database)
        else:
            sys.stdout.write('Did not recognize table name. Please specify table in database: \n\t'
                             'land\n\t'
                             'county\n\t'
                             'improvement\n\t'
                             'owner\n')
            initiate_insert(database)
    except Exception as e:
        print('Encountered error: ', e, ' while attempting to insert.')
        initiate_insert(database)

    repeat(database)


def insert_land(database):
    owner_id = input('\tOwner id: ')
    county_id = input('\tCounty id: ')
    rating = input('\tQuality rating: ')
    area = input('\tLand area: ')
    database.insert_into_land(rating, area)
    database.insert_into_governs(database.land_id, county_id)
    database.insert_into_owns(database.land_id, owner_id)
    sys.stdout.write('Successfully inserted land_id: ' + database.land_id + ' into land\n')

    repeat(database)


def insert_county(database):
    county_name = input('\tCounty name: ')
    state = input('\tState: ')
    pop = input('\tPopulation: ')
    area = input('\tArea: ')
    database.insert_into_county(county_name, state, pop, area)
    sys.stdout.write('Successfully inserted county_id: ' + database.county_id + ' into county\n')

    repeat(database)


def insert_improvement(database):
    improvement_type = input('\tImprovement improvement_type: ')
    cost = input('\tImprovement cost: ')
    improvement = input('\tImprovement factor: ')
    database.insert_into_improvement(improvement_type, cost, improvement)
    sys.stdout.write('Successfully inserted improvement_id: ' + database.improvement_id + ' into improvement\n')

    repeat(database)


def insert_owner(database):
    status = input('\tOwner status (public/private): ')
    name = input('\tOwner name: ')
    database.insert_into_owner(status, name)
    sys.stdout.write('Successfully inserted owner_id: ' + database.owner_id + ' into owner\n')

    repeat(database)


def insert_governs(database):
    land_id = input('\tLand id: ')
    county_id = input('\tCounty id: ')
    database.insert_into_governs(land_id, county_id)


def insert_owns(database):
    land_id = input('\tLand id: ')
    owner_id = input('\tOwner id: ')
    database.insert_into_owns(land_id, owner_id)


def repeat(database):
    repeat_input = input('Insert again (y/n)?: \n').lower()
    if repeat_input == 'q':
        util.exit_TEAL(database)
    elif repeat_input == 'y':
        initiate_insert(database)
    else:
        user_prompt.interact(database)
