import sys
from final_project import util
from final_project.TEAL import queries, input_prompt, modify_prompt, delete_prompt, query_prompt


def user_prompt():
    sys.stdout.write("Welcome to TEAL (Texas Explorer for Arid Land)\n\t"
                     "To exit, press q\n"
                     "Database Setup: \t\n")

    defaults = input("\tUse Defaults (y/n): ").lower()

    if defaults == 'q':
        util.exit_TEAL(None)

    if defaults == 'y':
        database_file = util.get_base_dir() / 'final_project/database/TEAL.sqlite'
        land_csv = util.get_base_dir() / 'final_project/input/land.csv'
        county_csv = util.get_base_dir() / 'final_project/input/county.csv'
        owner_csv = util.get_base_dir() / 'final_project/input/owner.csv'
        improvement_csv = util.get_base_dir() / 'final_project/input/improvement.csv'
        governs_csv = util.get_base_dir() / 'final_project/input/governs.csv'
        owns_csv = util.get_base_dir() / 'final_project/input/owns.csv'

    else:
        database_file = get_database("\tPlease provide a path to the database: ", None)
        land_csv = get_csv("\tPlease provide land data: ", None)
        county_csv = get_csv("\tPlease provide county data: ", None)
        owner_csv = get_csv("\tPlease provide land owner data: ", None)
        improvement_csv = get_csv("\tPlease provide land improvement data: ", None)
        governs_csv = get_csv("\tPlease provide land governance data: ", None)
        owns_csv = get_csv("\tPlease provide land ownership data: ", None)

    database = queries.Database(database_file)

    database.load_land_data(land_csv)
    database.load_county_data(county_csv)
    database.load_owner_data(owner_csv)
    database.load_improvement_data(improvement_csv)
    database.load_governs_data(governs_csv)
    database.load_owns_data(owns_csv)

    sys.stdout.write('\tDatabase successfully initialized.\n')

    interact(database)


def interact(database):
    select = selection_prompt()

    while select != 'q':
        if select == 'i':
            input_prompt.initiate_insert(database)
        elif select == 'd':
            delete_prompt.initiate_delete(database)
        elif select == 'm':
            modify_prompt.initiate_modify(database)
        elif select == 'o':
            query_prompt.query_options(database)
        else:
            select = selection_prompt()

    util.exit_TEAL(database)


def selection_prompt():
    select = input("Operations: \n\t"
                     "Initiate insert: i \n\t"
                     "Initiate delete: d \n\t"
                     "Initiate modification: m \n\t"
                     "Query Options: o \n\t")

    return select


def get_database(prompt, database):
    database_file = input(prompt)
    if database_file.lower() == 'q':
        util.exit_TEAL(database)

    if not database_file.endswith('.sqlite'):
        get_database('\tPlease provide a path to a sqlite file: ', database)

    database_file = util.get_base_dir() / 'final_project/database' / database_file

    if not database_file.is_file():
        get_database("\tDatabase file not found. Please provide sqlite file in database directory: ", database)

    return database_file


def get_csv(prompt, database):
    csv = input(prompt)
    if csv.lower() == 'q':
        util.exit_TEAL(database)

    if not csv.endswith('.csv'):
        get_csv("\tPlease provide the data in csv format: ", database)

    csv = util.get_base_dir() / 'final_project/input' / csv
    if not csv.is_file():
        get_csv("File not found. Please provide name of csv in input directory: ", database)

    return csv
