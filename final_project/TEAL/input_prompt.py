import sys
from final_project import util


def initiate_insert(database):
    table = input('Insert: \n'
                  'If you do not wish to specify an input, press enter \n'
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


def insert_land(database):
    land_id = input('Land id: ')
    owner_id = input('Owner id: ')
    county_id = input('County id: ')
    rating = input('Quality rating: ')
    area = input('Land area: ')
    database.insert_into_land(land_id, owner_id, county_id, rating, area)


def insert_county(database):
    county_id = input('County id: ')
    county_name = input('County name: ')
    pop = input('Population: ')
    growth_rate = input('Growth rate: ')
    database.insert_into_county(county_id, county_name, pop, growth_rate)


def insert_improvement(database):
    improvement_id = input('Improvement id: ')
    improvement_type = input('Improvement improvement_type: ')
    cost = input('Improvement cost: ')
    improvement = input('Improvement factor: ')
    database.insert_into_improvement(improvement_id, improvement_type, cost, improvement)


def insert_owner(database):
    owner_id = input('Owner id: ')
    status = input('Owner status (public/private): ')
    name = input('Owner name: ')
    database.insert_into_owner(owner_id, status, name)
