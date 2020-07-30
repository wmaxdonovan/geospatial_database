import sqlite3
import csv
import sys
from final_project.TEAL import user_prompt


class Database:
    def __init__(self, database_file):
        self.db_file = database_file
        self.land_id = 0
        self.county_id = 0
        self.owner_id = 0
        self.improvement_id = 0
        self.governs_id = 0
        self.owns_id = 0
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cur = self.conn.cursor()

            self.cur.execute('DROP TABLE IF EXISTS county')
            self.cur.execute('DROP TABLE IF EXISTS land')
            self.cur.execute('DROP TABLE IF EXISTS improvement')
            self.cur.execute('DROP TABLE IF EXISTS owner')
            self.cur.execute('DROP TABLE IF EXISTS governs')
            self.cur.execute('DROP TABLE IF EXISTS owns')

            self.cur.execute('CREATE TABLE IF NOT EXISTS county '
                             '(id INTEGER NOT NULL PRIMARY KEY, '
                             'name VARCHAR, '
                             'state VARCHAR, '
                             'pop INTEGER, '
                             'area FLOAT)')
            self.cur.execute('CREATE TABLE IF NOT EXISTS owner '
                             '(id INTEGER NOT NULL PRIMARY KEY, '
                             'status VARCHAR, '
                             'name VARCHAR)')
            self.cur.execute('CREATE TABLE IF NOT EXISTS land '
                             '(id INTEGER NOT NULL PRIMARY KEY, '
                             'rating INTEGER, '
                             'area INTEGER)')
            self.cur.execute('CREATE TABLE IF NOT EXISTS improvement '
                             '(id INTEGER NOT NULL PRIMARY KEY, '
                             'improvement_type VARCHAR, '
                             'cost FLOAT, '
                             'improvement INTEGER)')
            self.cur.execute('CREATE TABLE IF NOT EXISTS governs '
                             '(id INTEGER NOT NULL PRIMARY KEY, '
                             'land_id INTEGER, '
                             'county_id INTEGER, '
                             'FOREIGN KEY (land_id) REFERENCES land(id) ON DELETE CASCADE, '
                             'FOREIGN KEY (county_id) REFERENCES county(id) ON DELETE CASCADE)')
            self.cur.execute('CREATE TABLE IF NOT EXISTS owns '
                             '(owns_id INTEGER NOT NULL PRIMARY KEY, '
                             'land_id INTEGER, '
                             'owner_id INTEGER, '
                             'FOREIGN KEY (land_id) REFERENCES land(id) ON DELETE CASCADE, '
                             'FOREIGN KEY (owner_id) REFERENCES owner(id) ON DELETE CASCADE)')

        except Exception as e:
            print("The program encountered the following exception while trying"
                  " to initialize the database: ", e)
            user_prompt.user_prompt()

    def insert_table(self, table_name, cols):
        self.cur.execute('DROP TABLE IF EXISTS ' + table_name)
        self.cur.execute('CREATE TABLE IF NOT EXISTS ' + table_name +
                         'id INTEGER NOT NULL PRIMARY KEY')

        for name, data_type in zip(cols.keys(), cols.values()):
            self.cur.execute('DECLARE ' + table_name + ' TABLE ' + name + ' ' + data_type)

        sys.stdout.write('Successfully inserted table ' + table_name + '\n')

    def delete_table(self, table_name):
        self.cur.execute('DROP TABLE IF EXISTS ' + table_name)
        sys.stdout.write('Successfully deleted ' + table_name + '\n')

    def delete_item(self, table_name, col, condition):
        self.cur.execute('DELETE FROM ' + table_name + ' WHERE ' + col + condition)
        sys.stdout.write('Successfully deleted ' + condition + ' from ' + col + ' in ' + table_name + '\n')

    def load_land_data(self, land_csv):
        with land_csv.open('r') as land_csv:
            read_csv = csv.reader(land_csv, delimiter=',')
            first_line = True
            for row in read_csv:
                if first_line:
                    first_line = False
                    continue
                self.insert_into_land(row[0], row[1])

    def load_county_data(self, county_csv):
        with county_csv.open('r') as county_csv:
            read_csv = csv.reader(county_csv, delimiter=',')
            first_line = True
            for row in read_csv:
                if first_line:
                    first_line = False
                    continue
                self.insert_into_county(row[0], row[1], row[2], row[3])

    def load_improvement_data(self, improve_csv):
        with improve_csv.open('r') as improve_csv:
            read_csv = csv.reader(improve_csv, delimiter=',')
            first_line = True
            for row in read_csv:
                if first_line:
                    first_line = False
                    continue
                self.insert_into_improvement(row[0], row[1], row[2])

    def load_owner_data(self, owner_csv):
        with owner_csv.open('r') as owner_csv:
            read_csv = csv.reader(owner_csv, delimiter=',')
            first_line = True
            for row in read_csv:
                if first_line:
                    first_line = False
                    continue
                self.insert_into_owner(row[0], row[1])

    def load_governs_data(self, governs_csv):
        with governs_csv.open('r') as governs_csv:
            read_csv = csv.reader(governs_csv, delimiter=',')
            first_line = True
            for row in read_csv:
                if first_line:
                    first_line = False
                    continue
                self.insert_into_governs(row[0], row[1])

    def load_owns_data(self, owns_csv):
        with owns_csv.open('r') as owns_csv:
            read_csv = csv.reader(owns_csv, delimiter=',')
            first_line = True
            for row in read_csv:
                if first_line:
                    first_line = False
                    continue
                self.insert_into_owns(self.owns_id, row[0], row[1])

    def insert_into_land(self, rating, area):
        self.cur.execute('INSERT INTO land (id, rating, area) '
                         'VALUES (?, ?, ?)',
                         (self.land_id, rating, area))
        self.land_id += 1

    def insert_into_county(self, county_name, state, pop, area):
        self.cur.execute('INSERT INTO county (id, name, state, pop, area) '
                         'VALUES (?, ?, ?, ?, ?)',
                         (self.county_id, county_name, state, pop, area))
        self.county_id += 1

    def insert_into_improvement(self, improvement_type, cost, improvement):
        self.cur.execute('INSERT INTO improvement (id, improvement_type, cost, improvement) '
                         'VALUES (?, ?, ?, ?)',
                         (self.improvement_id, improvement_type, float(cost), int(improvement)))
        self.improvement_id += 1

    def insert_into_owner(self, status, name):
        self.cur.execute('INSERT INTO owner (id, status, name) '
                         'VALUES (?, ?, ?)',
                         (str(self.owner_id), status, name))
        self.owner_id += 1

    def insert_into_governs(self, land_id, county_id):
        self.cur.execute('INSERT INTO governs (id, land_id, county_id) '
                         'VALUES (?, ?, ?)',
                         (self.governs_id, int(land_id), int(county_id)))
        self.governs_id += 1

    def insert_into_owns(self, owns_id, land_id, owner_id):
        self.cur.execute('INSERT INTO owns (owns_id, land_id, owner_id) '
                         'VALUES (?, ?, ?)',
                         (int(owns_id), int(land_id), owner_id))
        self.owns_id += 1

    def write_csv(self, csv_path):
        with csv_path.open('w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            row = self.cur.fetchone()
            while row is not None:
                csv_writer.writerow(row)
                row = self.cur.fetchone()

    def get_land_by_county(self, county_name):
        self.cur.execute('SELECT land.*, county.* '
                         'FROM governs '
                         'INNER JOIN county '
                         'ON governs.county_id = county.id '
                         'WHERE county.name = ? '
                         'INNER JOIN land '
                         'ON governs.land_id = land.id ',
                         county_name)

    def get_land_by_area(self, min_area, max_area):
        self.cur.execute('SELECT county.state, county.name, land.rating, land.area '
                         'FROM governs '
                         'INNER JOIN county '
                         'ON governs.county_id = county.id '
                         'INNER JOIN land '
                         'ON governs.land_id = land.id '
                         'WHERE ((? IS NULL) OR (land.area >= ?)) '
                         'AND ((? IS NULL) OR (land.area <= ?))',
                         (min_area, min_area, max_area, max_area))

    def get_land_by_owner(self, owner_name):
        self.cur.execute('SELECT * '
                         'FROM owns '
                         'INNER JOIN land '
                         'ON land.id = owns.land_id '
                         'INNER JOIN owner '
                         'ON owner.id = owns.owner_id '
                         'WHERE ((? IS NULL) OR (? = owner.name))',
                         (owner_name, owner_name))

    def get_land_by_quality_rating(self, min_rating, max_rating):
        self.cur.execute('SELECT county.state, county.name, land.area, land.rating '
                         'FROM governs '
                         'INNER JOIN county '
                         'ON governs.county_id = county.id '
                         'INNER JOIN land '
                         'ON governs.land_id = land.id '
                         'WHERE((? IS NULL) OR (rating >= ?)) '
                         'AND ((? IS NULL) OR (rating <= ?))',
                         (min_rating, min_rating, max_rating, max_rating))

    def view_land_details(self):
        self.cur.execute('SELECT land.*, '
                         'owner.name AS owner_name, '
                         'owner.status AS owner_status, '
                         'county.name AS county_name, '
                         'county.area AS county_area, '
                         'county.state AS state, '
                         'county.pop AS county_population '
                         'FROM owns '
                         'INNER JOIN governs '
                         'ON owns.land_id = governs.land_id '
                         'INNER JOIN county '
                         'ON county.id = governs.county_id '
                         'INNER JOIN owner '
                         'ON owns.owner_id = owner.id '
                         'INNER JOIN land '
                         'ON owns.land_id = land.id')

    def get_average_rating_county(self):
        self.cur.execute('SELECT county.id, county.name, AVG(land.rating) '
                         'FROM county '
                         'INNER JOIN governs '
                         'ON governs.county_id = county.id '
                         'INNER JOIN land '
                         'ON governs.land_id = land.id '
                         'GROUP BY county.id, county.name')

    def get_area_by_owner(self):
        self.cur.execute('SELECT owner.id, owner.name, SUM(land.area) as owned_area '
                         'FROM owner '
                         'INNER JOIN owns '
                         'ON owns.owner_id = owner.id '
                         'INNER JOIN land '
                         'ON owns.land_id = land.id '
                         'GROUP BY owner.id, owner.name')

    def get_owners_in_county(self, county_name):
        self.cur.execute('SELECT owner.id owner_id, owner.name owner_name, '
                         'SUM(land.area), '
                         'county.id county_id, county.name county_name, county.state state '
                         'FROM owner '
                         'INNER JOIN owns '
                         'ON owner.id = owns.owner_id '
                         'INNER JOIN governs '
                         'ON owns.land_id = governs.land_id '
                         'INNER JOIN land '
                         'ON land.id = owns.land_id '
                         'INNER JOIN county '
                         'ON county.id = governs.county_id '
                         'WHERE (? IS NULL) OR (county.name = ?) '
                         'GROUP BY owner.id, owner.name, county.id, county.name',
                         (county_name, county_name))

    def get_critical_land_count_by_county(self, critical_threshold):
        self.cur.execute('SELECT county.id, county.name, COUNT(land.id) as critical_count '
                         'FROM governs '
                         'INNER JOIN county '
                         'ON county.id = governs.county_id '
                         'INNER JOIN land '
                         'ON land.id = governs.land_id '
                         'WHERE land.rating <= (?) '
                         'GROUP BY county.id, county.name',
                         critical_threshold)

    def get_land_by_status(self, land_status):
        self.cur.execute('SELECT * '
                         'FROM owns '
                         'INNER JOIN land '
                         'ON owns.land_id = land.id '
                         'INNER JOIN owner '
                         'ON owns.owner_id = owner.id '
                         'WHERE owner.status = ?',
                         land_status)

    def optimize(self, owner_name, county_name):
        self.cur.execute('SELECT * '
                         'FROM improvement')

        improvement = {}

        row = self.cur.fetchone()
        while row is not None:
            plan_id = row[0]
            improvement_type = row[1]
            cost = row[2]
            rating_improvement = row[3]
            improvement[improvement_type] = {'plan_id': plan_id, 'cost': cost, 'rating_improvement': rating_improvement}
            row = self.cur.fetchone()

        query = 'SELECT land.id, land.rating, land.area ' \
                'FROM land '

        owner_flag = False
        if owner_name != '':
            owner_flag = True
            query += 'INNER JOIN owns ' \
                     'ON land.id = owns.land_id ' \
                     'INNER JOIN owner ' \
                     'ON owns.owner_id = owner.id '

        county_flag = False
        if county_name != '':
            county_flag = True
            query += 'INNER JOIN governs ' \
                     'ON governs.land_id = land.id ' \
                     'INNER JOIN county ' \
                     'ON governs.county_id = county.id ' \
                     'WHERE county.name = ' + county_name
            if owner_flag:
                query += ' AND owner.name = ' + owner_name

        if owner_flag and not county_flag:
            query += 'WHERE owner.name = ' + owner_name

        self.cur.execute(query)

        land = {}
        row = self.cur.fetchone()
        while row is not None:
            plan_id = row[0]
            rating = row[1]
            area = row[2]
            land[plan_id] = {'rating': rating, 'area': area}
            row = self.cur.fetchone()

        for improvement_type, improvement_data in zip(improvement.keys(), improvement.values()):
            cost_sum = 0
            improvement_sum = 0
            land_sum = 0
            for land_id, land_data in zip(land.keys(), land.values()):
                land_sum += land_data['area']
                cost_sum += (land_data['area'] * improvement_data['cost'])
                improvement_sum += min(improvement_data['rating_improvement'], 8 - land_data['rating'])
            improvement[improvement_type]['total_cost'] = cost_sum
            improvement[improvement_type]['total_land'] = land_sum
            improvement[improvement_type]['avg_improvement'] = improvement_sum / len(land)
            improvement[improvement_type]['cost_per_unit_improvement'] = \
                round(cost_sum / improvement_sum, 3)

        for improvement_type in improvement:
            print(improvement_type, improvement[improvement_type])

    def generic_query(self, table, distinct, compare_val, condition):
        query = "SELECT "
        if distinct:
            query += "DISTINCT "
        query += "* FROM " + table
        if compare_val is not None:
            query += " WHERE " + compare_val + condition

        self.cur.execute(query)

    def write_result(self):
        row = self.cur.fetchone()
        while row is not None:
            print(row)
            row = self.cur.fetchone()
