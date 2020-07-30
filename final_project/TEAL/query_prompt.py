import sys
from final_project import util
from final_project.TEAL import user_prompt


def query_options(database):
    select = input('Query Options: \n\t'
                   'Get Land by County: 1\n\t'
                   'Get Land by Area: 2\n\t'
                   'Get Land by Owner: 3\n\t'
                   'Get Land by Quality: 4\n\t'
                   'View Land Details: 5\n\t'
                   'Get Average Land Rating by County: 6\n\t'
                   'Get Land Area by Owner: 7\n\t'
                   'Get Owners in County: 8\n\t'
                   'Get Critical Land Count by County: 9\n\t'
                   'Get Land by Owner Status: 10\n\t'
                   'Optimize Land Improvement: 11\n\t'
                   'Formulate Custom Query: 12\n\t').lower()

    if select == 'q':
        util.exit_TEAL(database)

    try:
        select = int(select)
    except Exception as e:
        print('Encountered error: ', e, 'while processing user input. Integer expected')
        query_options(database)

    try:
        if select == 1:
            county_name = input('search county name: \t')
            database.get_land_by_county(county_name)
        elif select == 2:
            min_area = int(input('minimum area for search: \t'))
            max_area = int(input('maximum area for search: \t'))
            database.get_land_by_area(min_area, max_area)
        elif select == 3:
            owner_name = input('search owner name: \t')
            database.get_land_by_owner(owner_name)
        elif select == 4:
            min_ratiing = input('minimum rating for search: \t')
            max_rating = input('maximum rating for search: \t')
            database.get_land_by_quality_rating(min_ratiing, max_rating)
        elif select == 5:
            database.view_land_details()
        elif select == 6:
            database.get_average_rating_county()
        elif select == 7:
            database.get_area_by_owner()
        elif select == 8:
            county_name = input('county name for search: \t')
            database.get_owners_in_county(county_name)
        elif select == 9:
            critical_threshold = int(input('critical land quality threshold: \t'))
            database.get_critical_land_count_by_county(critical_threshold)
        elif select == 10:
            status = input('ownership status for search (public/private): \t')
            database.get_land_by_status(status)
        elif select == 11:
            owner_name = input('owner name for optimization: \t')
            county_name = input('county name for optimization: \t')
            database.optimize(owner_name, county_name)
        elif select == 12:
            table = input('table to perform query on: \t')
            distinct = input('DISTINCT (y/n): \t').lower() == 'y'
            compare_val = input('attribute to be queried: \t')
            condition = input('condition on attribute (accepts range using >, <, =): ')

            database.generic_query(table, distinct, compare_val, condition)
        else:
            sys.stdout.write("Query selection not recognized.")
            query_options(database)

        database.write_result()

    except Exception as e:
        print("Encountered error: ", e, "while processing query")
        query_options(database)

    repeat(database)


def repeat(database):
    repeat_modify = input("\tquery again (y/n)?: ").lower()
    if repeat_modify == 'q':
        util.exit_TEAL(database)
    elif repeat_modify == 'y':
        query_options(database)
    else:
        user_prompt.interact(database)
