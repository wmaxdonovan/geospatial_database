import sqlite3
import csv


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
                             'county_name VARCHAR, '
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
            exit(1)

    def delete_table(self, table_name):
        self.cur.execute('DROP TABLE IF EXISTS ' + table_name)

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
        self.cur.execute('INSERT INTO land (id, owner_id, county_id, rating, area)'
                         'VALUES (?, ?, ?, ?, ?)',
                         (int(land_id), int(owner_id), int(county_id), int(rating), int(area)))

    def insert_into_county(self, county_id, county_name, pop, growth_rate):
        self.cur.execute('INSERT INTO county (id, county_name, pop, growth_rate)'
                         'VALUES (?, ?, ?, ?)',
                         (int(county_id), county_name, int(pop), float(growth_rate)))

    def insert_into_improvement(self, improvement_id, improvement_type, cost, improvement):
        self.cur.execute('INSERT INTO improvement (id, improvement_type, cost, improvement)'
                         'VALUES (?, ?, ?, ?)',
                         (int(improvement_id), improvement_type, float(cost), int(improvement)))

    def insert_into_owner(self, owner_id, status, name):
        self.cur.execute('INSERT INTO owner (id, status, name)'
                         'VALUES (?, ?, ?)',
                         (int(owner_id), status, name))

    def remove_from_table(self, table, table_id):
        self.cur.execute('DELETE FROM ' + table +
                         'WHERE id = ?' + int(table_id))

    def write_csv(self, csv_path):
        with csv_path.open('w') as write_csv:
            write_csv = csv.writer(write_csv, delimiter=',')
            row = self.cur.fetchone()
            while row is not None:
                write_csv.writerow(row)
                row = self.cur.fetchone()

    def get_land_by_county(self, county_id, county_name):
        self.cur.execute('SELECT L.*, C.*'
                         'FROM land'
                         'INNER JOIN county C'
                         'ON C.id = L.county_id'
                         'WHERE L.county_id = ?'
                         'OR C.name = ?', (county_id, county_name))

    def get_land_by_area(self, min_area, max_area):
        self.cur.execute('SELECT *'
                         'FROM land'
                         'WHERE ((? IS NULL) OR (area >= ?)) '
                         'AND ((? IS NULL) OR (area <= ?))',
                         (min_area, min_area, max_area, max_area))

    def get_land_by_owner(self, owner_id, owner_name):
        self.cur.execute('SELECT *'
                         'FROM land'
                         'INNER JOIN owner'
                         'ON owner.id = land.owner_id'
                         'WHERE((? IS NULL) OR (? = land.owner_id))'
                         'AND((? IS NULL) OR (? = owner.name))',
                         (owner_id, owner_id, owner_name, owner_name))

    def get_land_by_quality_rating(self, min_rating, max_rating):
        self.cur.execute('SELECT *'
                         'FROM land'
                         'WHERE((? IS NULL) OR (rating >= ?))'
                         'AND((? IS NULL) OR (rating <= ?))',
                         (min_rating, min_rating, max_rating, max_rating))

    def view_land_details(self):
        self.cur.execute('SELECT L.*,'
                         'O.name AS owner_name,'
                         'O.status AS owner_status,'
                         'C.name AS county_name,'
                         'C.growth_rate AS county_growth_rate,'
                         'C.pop AS county_population'
                         'FROM land L'
                         'INNER JOIN owner O'
                         'ON O.id = L.owner_id'
                         'INNER JOIN county C'
                         'ON C.id = L.owner_id')

    def get_average_rating_county(self):
        self.cur.execute('SELECT county.id, county.name, AVG(land.rating)'
                         'FROM county'
                         'INNER JOIN land'
                         'ON land.county_id = county.id'
                         'GROUP BY county.id, county.name')

    def get_area_by_owner(self):
        self.cur.execute('SELECT owner.id, owner.name, SUM(land.area) as owned_area'
                         'FROM owner'
                         'INNER JOIN land'
                         'ON land.owner_id = owner.id'
                         'GROUP BY owner.id, owner.name'
                         )

    def get_owners_in_county(self, county_id, county_name):
        self.cur.execute('SELECT owner.id owner_id, owner.name owner_name, '
                         'county.id county_id, county.name, county_name'
                         'FROM owner'
                         'INNER JOIN land'
                         'ON owner.id = land.owner_id'
                         'INNER JOIN county'
                         'ON county.id = land.county_id'
                         'WHERE((? IS NULL) OR (land.county_id = ?)) '
                         'AND ((? IS NULL) OR (county.name = ?))',
                         (county_id, county_id, county_name, county_name))

    def get_critical_land_count_by_county(self, critical_threshold):
        self.cur.execute('SELECT county.id, county.name, COUNT(land.id) as critical_count'
                         'FROM county'
                         'INNER JOIN land'
                         'ON county.id = land.county_id'
                         'WHERE land.rating <= ?'
                         'GROUP BY county.id, county.name',
                         critical_threshold)

    def get_land_by_status(self, land_status):
        self.cur.execute('SELECT *'
                         'FROM land'
                         'INNER JOIN owner'
                         'ON owner.id = land.owner_id'
                         'WHERE owner.status = ?', land_status)

    def generic_query(self, table, distinct=False, cols=None, identifier=None,
                      desired_rows=None, compare_val=None, low_col=None, high_col=None):
        """
        Constructs and executes a query on @table of the following form
        (all clauses in square brackets are optional, depending on parameters
        given):
        SELECT [DISTINCT] * FROM table [WHERE low_col <= compare_val AND
            high_col >= compare_val] [AND/WHERE identifier IN (desired_rows)]
        or, if columns are specified using @cols:
        SELECT [DISTINCT] cols FROM table [WHERE low_col <= compare_val AND
            high_col >= compare_val] [AND/WHERE identifier IN (desired_rows)]
        The result of this query is returned.
        If an exception is raised when connecting/querying the database, this
        method prints the error message and quits the program.

        Args:
            table: string - the name of the table to be queried
            distinct: (optional) boolean - if true, the query result contains no
                duplicates
            cols: (optional) list of strings - each string in this list is a
                column name that will be returned. If this argument is not
                specified, all columns from the specified table will be returned
            identifier: (optional) string - the column name which will be
                compared to the desired_rows values. If this argument is
                specified, desired_rows must also be specified, otherwise both
                will be treated as None.
            desired_rows: (optional) tuple of strings - the values of the
                identifier column which are being queried. If this argument is
                specified, identifier must also be specified, otherwise both
                will be treated as None.
            compare_val: (optional) string - the value which should fall in the
                range of [low_col, high_col]. If this argument is specified,
                low_col and high_col must also be specified, otherwise these
                three arguments will be treated as None.
            low_col: (optional) string - the column name of the lower bound of
                the desired range. If this argument is specified, compare_val
                and high_col must also be specified, otherwise these three
                arguments will be treated as None.
            high_col: (optional) string - the column name of the upper bound of
                the desired range. If this argument is specified, compare_val
                and low_col must also be specified, otherwise these three
                arguments will be treated as None.

        Returns:
            the result of the query formed as a list of dictionaries where each
            dictionary represents a row returned (the keys in each dictionary
            are the column names and they are mapped to the values in the
            database)
        """
        try:
            # Forms a connection to the database
            self.conn.row_factory = sqlite3.Row

            # the query starts with SELECT
            query = "SELECT "

            # if distinct is true, append the DISTINCT keyword
            if distinct:
                query += "DISTINCT "

            # if cols is not specified, all columns are returned, otherwise
            # the specified column names are joined by commas and inserted
            # into the query
            if cols is None:
                query += "* FROM " + table
            else:
                query += ",".join(cols) + " FROM " + table

            # appends the range part of the query if all 3 components are
            # specified
            append_range = compare_val is not None and \
                           low_col is not None and \
                           high_col is not None
            if append_range:
                query += " WHERE " + low_col + " <= " + compare_val + \
                         " AND " + high_col + " >= " + compare_val

            if desired_rows is None or identifier is None:
                # Since identifier and desired_rows are None, the following
                # command will execute the query as formulated above on all the
                # rows of the database.
                self.cur.execute(query)

            else:
                # if the range has already been appending, the identifier part
                # of the query is another AND clause, otherwise it is the
                # beginning of the WHERE clause
                if append_range:
                    query += " AND "
                else:
                    query += " WHERE "
                # filters which rows should be returned from the query
                query += identifier + " IN " + \
                         "({})".format(','.join(['?'] * len(desired_rows)))
                # Here, desired_rows is a parameter to the query as the list of
                # rows for which information is wanted. This list will be
                # formatted as specified in the query above (i.e. all elements
                # are separated by a comma and the list is surrounded by
                # parentheses).
                self.cur.execute(query, desired_rows)

            # construct a list of dictionaries, where each dictionary in
            # the list corresponds to a row in the database table storing
            # the information for the row
            result = []
            row = self.cur.fetchone()
            while row is not None:
                result.append(dict(row))
                row = self.cur.fetchone()

            return result

        except Exception as e:
            print("DatabaseReader.query(): The program encountered the "
                  "following exception while connecting to and querying table",
                  table, "from database", self.db_file, ":", e, "\nExiting.")
            exit(1)
