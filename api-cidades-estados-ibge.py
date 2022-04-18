import chunk
import pandas as pd
import requests
import sys

# Import Database Config
sys.path.append('./config')
from database import db, env

# Best Link to read JSON - All in the same level = 0
url = r'https://servicodados.ibge.gov.br/api/v1/localidades/municipios?view=nivelado'

# Getting all data CONTENT
# result = requests.get(url).content

# 1 - Reading Json with Pandas
# 2 - Creating DataFrame from JSON
# 3 - Droping Duplicas if have any
# 4 - Pandas Newers Versions can get direct from url, make GET directly
df = pd.DataFrame(pd.read_json(url,orient='records')).drop_duplicates()

# 1-  Selecting only two coluns, City and State
# 2 - Ordering by city name ascending
df = (df[['municipio-nome','UF-sigla']].sort_values(by=['municipio-nome'],ascending=True))

# Rename Pandas DataFrame Columns
df = df.rename(columns={"municipio-nome":"cidade","UF-sigla":"uf"})

# Setting Variables for Connection
HOST, PORT, DATABASE, USER, PASS = env.pg_backend()

# Passing variables to db Class
database = db(HOST, PORT, DATABASE, USER, PASS)

# Setting con with postgres connector from SqlAlchemy
con = database.pg()

# Inserting directly inside PostgreSQL with Pandas
df.to_sql('MunicipiosIbge',con=con, if_exists='append', chunksize=1000,index=False)
