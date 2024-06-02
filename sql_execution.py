import sqlite3 
import pandas as pd

def execute_sf_query(sql):
    query = sql
    conn = None
    cur = None
    try:
        # Establish a connection to SQLite database
        conn = sqlite3.connect('dataset_alumni.db')

        # Create a cursor object
        cur = conn.cursor()

        # Execute the query
        cur.execute(query)

        # Fetch all results
        query_results = cur.fetchall()

        # Get column names from the cursor description
        column_names = [col[0] for col in cur.description]

        # Create a Pandas DataFrame
        data_frame = pd.DataFrame(query_results, columns=column_names)

        # Return the DataFrame
        return data_frame

    except sqlite3.Error as e:
        print("sqlite Error:", e)
        return None

    except Exception as e:
        print("An error occurred:", e)
        return None

    finally:
        # Close the cursor and connection
        if cur:
            cur.close()
        if conn:
            conn.close()


