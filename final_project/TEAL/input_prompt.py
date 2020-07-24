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
        print('Encountered error ', e, ' while attempting to insert.')
        initiate_insert(database)

    repeat(database)


def insert_land(database):
    land_id = input('\tLand id: ')
    owner_id = input('\tOwner id: ')
    county_id = input('\tCounty id: ')
    rating = input('\tQuality rating: ')
    area = input('\tLand area: ')
    database.insert_into_land(land_id, owner_id, county_id, rating, area)
    sys.stdout.write('Successfully inserted land_id: ' + land_id + ' into land\n')

    repeat(database)


def insert_county(database):
    county_id = input('\tCounty id: ')
    county_name = input('\tCounty name: ')
    pop = input('\tPopulation: ')
    growth_rate = input('\tGrowth rate: ')
    database.insert_into_county(county_id, county_name, pop, growth_rate)
    sys.stdout.write('Successfully inserted county_id: ' + county_id + ' into county\n')

    repeat(database)


def insert_improvement(database):
    improvement_id = input('\tImprovement id: ')
    improvement_type = input('\tImprovement improvement_type: ')
    cost = input('\tImprovement cost: ')
    improvement = input('\tImprovement factor: ')
    database.insert_into_improvement(improvement_id, improvement_type, cost, improvement)
    sys.stdout.write('Successfully inserted improvement_id: ' + improvement_id + ' into improvement\n')

    repeat(database)


def insert_owner(database):
    owner_id = input('\tOwner id: ')
    status = input('\tOwner status (public/private): ')
    name = input('\tOwner name: ')
    database.insert_into_owner(owner_id, status, name)
    sys.stdout.write('Successfully inserted owner_id: ' + owner_id + ' into owner\n')

    repeat(database)


def repeat(database):
    repeat_input = input('Insert again (y/n)?: \n').lower()
    if repeat_input == 'q':
        util.exit_TEAL(database)
    elif repeat_input == 'y':
        initiate_insert(database)
    else:
        user_prompt.interact(database)
