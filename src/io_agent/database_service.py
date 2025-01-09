import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import os


class DatabaseService:
    """
    A class to manage PostgreSQL database connections and queries.
    It provides methods to interact with the database in a modular way.
    """

    def __init__(self, host: str, port: int, dbname: str, user: str, password: str):
        self.host = host
        self.port = port
        self.dbname = dbname
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establish a connection to the PostgreSQL database."""
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                dbname=self.dbname,
                user=self.user,
                password=self.password
            )
            self.cursor = self.connection.cursor()
            print("Connected to the database successfully.")
        except Exception:
            print("Error connecting to the database. Check your credentials.")

    
    def close(self):
        """Close the database connection and cursor."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Database connection closed.")



    def import_csv_to_table(self, csv_file_path: str, table_name: str):
        """
        A helper function
        Imports data from a CSV file into a specified table.

        Args:
            csv_file_path (str): Path to the CSV file.
            table_name (str): Name of the table where data will be inserted.

        Returns:
            None
        """
        try:
            
            df = pd.read_csv(csv_file_path)
            stock_symbol = os.path.splitext(os.path.basename(csv_file_path))[0]
                

            # Step 2: Clean the column names
            
            df.columns = df.columns.str.lower()  # Convert column 
            df.columns = (
                            df.columns
                            .str.strip()  # Remove leading/trailing spaces
                            .str.lower()  # Convert to lowercase
                            .str.replace(r'[^\w\s]', '', regex=True)  # Remove non-alphanumeric characters except spaces
                            .str.replace(' ', '')  # Remove spaces
                        )
            # Convert "price", "open", "high", and "low" columns to numeric by removing commas
            for col in ['price','open', 'high', 'low']:
                if col in df.columns:
                    df[col] = df[col].replace({',': ''}, regex=True).astype(float)

            print(df.columns)
            df['stock_symbol'] = stock_symbol 
            engine = create_engine(f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}")
            df.to_sql(table_name, engine, if_exists='append', index=False)
            print(f"Data successfully imported into {table_name} table!")
                
    
        except Exception as e:
            print(f"Error importing CSV to table: {e}")
            self.connection.rollback()

    def fetch_historical_data(self, stock_symbol: str, start_date: str, end_date: str):
        """
        Fetch historical stock data for a given symbol and date range.

        Args:
            stock_symbol (str): The stock symbol to filter by.
            start_date (str): Start date in 'YYYY-MM-DD' format.
            end_date (str): End date in 'YYYY-MM-DD' format.

        Returns:
            list[dict]: List of dictionaries containing the stock data.
        """
        query = """
        SELECT * FROM stock_data
        WHERE stock_symbol = %s AND date BETWEEN %s AND %s
        ORDER BY date;
        """
        try:
            self.cursor.execute(query, (stock_symbol, start_date, end_date))
            results = self.cursor.fetchall()

            # Fetch column names for the result mapping
            column_names = [desc[0] for desc in self.cursor.description]
            data = [dict(zip(column_names, row)) for row in results]

            return data
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return []



db = DatabaseService(os.environ['DB_URL'], os.environ['DB_PORT'], os.environ['DB_NAME'], os.environ['DB_USERNAME'], os.environ['DB_PASSWORD'])
db.connect()


