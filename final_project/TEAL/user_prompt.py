import sys
from final_project import util
from final_project.TEAL import queries, input_prompt, modify_prompt, delete_prompt, query_prompt

def user_prompt():
    sys.stdout.write("Welcome to TEAL (Texas Explorer for Arid Land)\n\t"
                     "To exit, press q\n"
                     "Database Setup: \t\n")

    defaults = input("Use Defaults (y/n): ").lower() == 'y'

    if defaults:
        database_file = util.get_base_dir() / 'final_project/database/TEAL.sqlite'
        land_csv = util.get_base_dir() / 'final_project/input/land.csv'
        county_csv = util.get_base_dir() / 'final_project/input/county.csv'
        owner_csv = util.get_base_dir() / 'final_project/input/owner.csv'
        improvement_csv = util.get_base_dir() / 'final_project/input/improvement.csv'

    else:
        database_file = get_database("Please provide a path to the database: ")
        land_csv = get_csv("Please provide land data: ")
        county_csv = get_csv("Please provide county data: ")
        owner_csv = get_csv("Please provide land owner data: ")
        improvement_csv = get_csv("Please provide land improvement data: ")

    database = queries.Database(database_file)

    database.load_land_data(land_csv)
    database.load_county_data(county_csv)
    database.load_owner_data(owner_csv)
    database.load_improvement_data(improvement_csv)

    sys.stdout.write('Database successfully initialized.')

    select = selection_prompt()

    while select != 'q':
        if select == 'i':
            input_prompt.initiate_insert()
        elif select == 'd':
            delete_prompt.initiate_delete()
        elif select == 'm':
            modify_prompt.initiate_modify()
        elif select == 'o':
            query_prompt.query_options()
        else:
            select = selection_prompt()


def selection_prompt():
    select = input("Operations: \n\t"
                     "Initiate insert: i \n"
                     "Initiate delete: d \n"
                     "Initiate modification: m \n"
                     "Query Options: o \n")

    return select


def get_database(prompt):
    database_file = input(prompt)
    if database_file.lower() == 'q':
        util.exit_TEAL()

    if not database_file.endswith('.sqlite'):
        get_database('Please provide a path to a sqlite file')

    database_file = util.get_base_dir() / 'final_project/database' / database_file

    if not database_file.is_file():
        get_database("Database file not found. Please provide sqlite file in database directory: ")

    return database_file


def get_csv(prompt):
    csv = input(prompt)
    if csv.lower() == 'q':
        exit_TEAL()

    if not csv.endswith('.csv'):
        get_csv("Please provide the data in csv format: ")

    csv = util.get_base_dir() / 'final_project/input' / csv
    if not csv.is_file():
        get_csv("File not found. Please provide name of csv in input directory: ")

    return csv
