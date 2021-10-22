# This module contains functions for creation and interaction with the frequency analysis database

import sqlite3

connection = sqlite3.connect("freq_table.db")
cursor = connection.cursor()

def create_db():
    """create database, but first drop it if it already exists"""
    cursor.execute("DROP TABLE IF EXISTS freq_table;")
    sql_command = """CREATE TABLE freq_table 
        (Letter VARCHAR(1) PRIMARY KEY);"""
    cursor.execute(sql_command)
    connection.commit()

def read_csv_file(filename):
    """return readlines() from file with given filename"""
    with open(filename, "r", encoding="UTF-8") as csv_file:
        return csv_file.readlines()

def get_columns_from_db():
    """returns a list of the columns in db-table"""
    cursor.execute("SELECT name FROM PRAGMA_TABLE_INFO('freq_table')")
    return [col[0] for col in cursor]

def add_lang_columns(language_list):
    """add one column to db-table for each language in language-list"""
    for language in language_list:
        cursor.execute(f"ALTER TABLE freq_table ADD COLUMN {language} FLOAT;")
    connection.commit()
    #current_columns = get_columns_from_db()
    #print("current_columns:", current_columns, "len:", len(current_columns))

def format_row(row):
    """Takes a list as argument, leaves the first entry as a string and converts the rest
    of entries to float, and then returns a correctly formatted list"""
    formatted_row = [row[0]] # initiate list with the first entry (the actual letter)
    for value in row[1:]:
        try:
            value = float(value)
            formatted_row.append(value)
        except:
            print("conversion to float failed for value:", value, ", letter:", formatted_row[0])
            break
    return formatted_row

def fill_rows_in_db(frequency_table):
    """fill db with contents from frequency table (which is readlines() from csv-file).
    Code is messy and not optimal because further development is wanted, but not prioritized. 
    Optimally we would define which columns values should go into."""
    scrub = " ~%*()"    # many entries in csv-file contain these characters that need to be removed
    for row in frequency_table[1:]: #  [1:] because first row is only headers
        row = [value.strip().strip(scrub).strip(scrub) for value in row.split(";")] # scrub unwanted characters from each row
        formatted_row = format_row(row) # format row so that it contains correct data types for db-entry
        #column_names_string = ""   # want to be able to specify which columns, but can't get it to work - leaving these parts commented out of code
        values_string = "" # initiate variable as empty string
        for header in get_headers(frequency_table)[:-1]:    # iterate through headers, except for last one which is added later
            #column_names_string += header + ", "
            values_string += '?, '  # add one "?, " for each header
        #column_names_string += get_headers(frequency_table)[:-1][-1]
        values_string += "?"    # add last ?
        sql_command = f"INSERT INTO freq_table VALUES ({values_string});"
        cursor.execute(sql_command, formatted_row)  # replace variables (values_string) with entries in formatted row
    connection.commit()

def get_headers(frequency_table):
    """Return a list of headers (first row) in readlines() from csv-file"""
    return [header.strip() for header in frequency_table[0].split(";")]

def create_complete_db():
    """First creates db and table, then reads csv-file and adds one column 
    to table for each language, then fill db-table with values from the read csv-file"""
    create_db()
    print("Database successfully created!")    
    frequency_table = read_csv_file("frequency_tables.csv")
    print("CSV-file successfully read!")
    # make a list of all the headers to make a language list
    language_list = get_headers(frequency_table)[1:] # first entry is not a language
    add_lang_columns(language_list)
    fill_rows_in_db(frequency_table)
    print("Data successfully loaded into database, you are ready to go!")

def make_fa_dict_from_db(language):
    """Takes a language(string) as argument and returns a fa-dictionary for that language,
    if the language is available in database"""
    try:    # try selecting all values from the given language-column where the value is not 0
        sql_command = f"SELECT Letter, {language} FROM freq_table \
                    WHERE {language} != 0"
        cursor.execute(sql_command)
    except: 
        print("Something went wrong,", language, "might not be available in database.")
    fa_dict = {}
    for row in cursor:
        fa_dict[row[0]] = row[1]
    return fa_dict

def make_all_fa_dicts_from_db():
    """creates a fa-dict for each language available in database, 
    returns a dictionary with language names as keys and fa-dicts as values"""
    headers = get_columns_from_db()
    language_list = headers[1:]
    all_fa_dict = {}
    for language in language_list:
        current_fa = make_fa_dict_from_db(language)
        all_fa_dict[language] = current_fa
    return all_fa_dict

if __name__ == "__main__":
    create_complete_db()



