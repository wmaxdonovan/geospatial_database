import sqlite3
import csv
import sys
from final_project.TEAL import user_prompt


class Database:
    def __init__(self, database_file):
        self.db_file = database_file
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cur = self.conn.cursor()

            self.cur.execute('DROP TABLE IF EXISTS county')
            self.cur.execute('DROP TABLE IF EXISTS land')
            self.cur.execute('DROP TABLE IF EXISTS improvement')
            self.cur.execute('DROP TABLE IF EXISTS owner')

            self.cur.execute('CREATE TABLE IF NOT EXISTS county '
                             '(id INTEGER NOT NULL PRIMARY KEY, '
                             'name VARCHAR, '
                             'pop INTEGER, '
                             'growth_rate FLOAT)')
            self.cur.execute('CREATE TABLE IF NOT EXISTS owner '
                             '(id INTEGER NOT NULL PRIMARY KEY, '
                             'status VARCHAR, '
                             'name VARCHAR)')
            self.cur.execute('CREATE TABLE IF NOT EXISTS land '
                             '(id INTEGER NOT NULL PRIMARY KEY, '
                             'owner_id INTEGER, '
                             'county_id INTEGER, '
                             'rating INTEGER, '
                             'area INTEGER,'
                             'FOREIGN KEY(owner_id) REFERENCES owner(id)'
                             'FOREIGN KEY(county_id) REFERENCES county(id))')
            self.cur.execute('CREATE TABLE IF NOT EXISTS improvement '
                             '(id INTEGER NOT NULL PRIMARY KEY, '
                             'improvement_type VARCHAR, '
                             'cost FLOAT, '
                             'improvement INTEGER)')

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
                self.insert_into_land(row[0], row[1], row[2], row[3], row[4])

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
                self.insert_into_improvement(row[0], row[1], row[2], row[3])

    def load_owner_data(self, owner_csv):
        with owner_csv.open('r') as owner_csv:
            read_csv = csv.reader(owner_csv, delimiter=',')
            first_line = True
            for row in read_csv:
                if first_line:
                    first_line = False
                    continue
                self.insert_into_owner(row[0], row[1], row[2])

    def insert_into_land(self, land_id, owner_id, county_id, rating, area):
        self.cur.execute('INSERT INTO land (id, owner_id, county_id, rating, area) '
                         'VALUES (?, ?, ?, ?, ?)',
                         (int(land_id), int(owner_id), int(county_id), int(rating), int(area)))

    def insert_into_county(self, county_id, county_name, pop, growth_rate):
        self.cur.execute('INSERT INTO county (id, name, pop, growth_rate) '
                         'VALUES (?, ?, ?, ?)',
                         (int(county_id), county_name, int(pop), float(growth_rate)))

    def insert_into_improvement(self, improvement_id, improvement_type, cost, improvement):
        self.cur.execute('INSERT INTO improvement (id, improvement_type, cost, improvement) '
                         'VALUES (?, ?, ?, ?)',
                         (int(improvement_id), improvement_type, float(cost), int(improvement)))

    def insert_into_owner(self, owner_id, status, name):
        self.cur.execute('INSERT INTO owner (id, status, name)'
                         'VALUES (?, ?, ?)',
                         (int(owner_id), status, name))

    def write_csv(self, csv_path):
        with csv_path.open('w') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            row = self.cur.fetchone()
            while row is not None:
                csv_writer.writerow(row)
                row = self.cur.fetchone()

    def get_land_by_county(self, county_id, county_name):
        self.cur.execute('SELECT L.*, C.* '
                         'FROM land L '
                         'INNER JOIN county C '
                         'ON C.id = L.county_id '
                         'WHERE L.county_id = ? '
                         'OR C.name = ?', (county_id, county_name))

    def get_land_by_area(self, min_area, max_area):
        self.cur.execute('SELECT * '
                         'FROM land '
                         'WHERE ((? IS NULL) OR (area >= ?)) '
                         'OR ((? IS NULL) OR (area <= ?))',
                         (min_area, min_area, max_area, max_area))

    def get_land_by_owner(self, owner_id, owner_name):
        self.cur.execute('SELECT * '
                         'FROM land '
                         'INNER JOIN owner '
                         'ON owner.id = land.owner_id '
                         'WHERE((? IS NULL) OR (? = land.owner_id)) '
                         'OR ((? IS NULL) OR (? = owner.name))',
                         (owner_id, owner_id, owner_name, owner_name))

    def get_land_by_quality_rating(self, min_rating, max_rating):
        self.cur.execute('SELECT * '
                         'FROM land '
                         'WHERE((? IS NULL) OR (rating >= ?)) '
                         'OR ((? IS NULL) OR (rating <= ?))',
                         (min_rating, min_rating, max_rating, max_rating))

    def view_land_details(self):
        self.cur.execute('SELECT L.*, '
                         'O.name AS owner_name, '
                         'O.status AS owner_status, '
                         'C.name AS county_name, '
                         'C.growth_rate AS county_growth_rate, '
                         'C.pop AS county_population '
                         'FROM land L '
                         'INNER JOIN owner O '
                         'ON O.id = L.owner_id '
                         'INNER JOIN county C '
                         'ON C.id = L.owner_id')

    def get_average_rating_county(self):
        self.cur.execute('SELECT county.id, county.name, AVG(land.rating) '
                         'FROM county '
                         'INNER JOIN land '
                         'ON land.county_id = county.id '
                         'GROUP BY county.id, county.name')

    def get_area_by_owner(self):
        self.cur.execute('SELECT owner.id, owner.name, SUM(land.area) as owned_area '
                         'FROM owner '
                         'INNER JOIN land '
                         'ON land.owner_id = owner.id '
                         'GROUP BY owner.id, owner.name'
                         )

    def get_owners_in_county(self, county_id, county_name):
        self.cur.execute('SELECT owner.id owner_id, owner.name owner_name, '
                         'SUM(land.area), '
                         'county.id county_id, county.name county_name '
                         'FROM owner '
                         'INNER JOIN land '
                         'ON owner.id = land.owner_id '
                         'INNER JOIN county '
                         'ON county.id = land.county_id '
                         'WHERE((? IS NULL) OR (land.county_id = ?)) '
                         'OR ((? IS NULL) OR (county.name = ?))'
                         'GROUP BY owner.id, owner.name, county.id, county.name',
                         (county_id, county_id, county_name, county_name))

    def get_critical_land_count_by_county(self, critical_threshold):
        self.cur.execute('SELECT county.id, county.name, COUNT(land.id) as critical_count '
                         'FROM county '
                         'INNER JOIN land '
                         'ON county.id = land.county_id '
                         'WHERE land.rating <= ? '
                         'GROUP BY county.id, county.name ',
                         critical_threshold)

    def get_land_by_status(self, land_status):
        self.cur.execute('SELECT * '
                         'FROM land '
                         'INNER JOIN owner '
                         'ON owner.id = land.owner_id '
                         'WHERE owner.status = ?', land_status)

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
