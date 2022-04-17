import pandas as pd
import requests


# Best Link to read JSON - All in the same level = 0
url = r'https://servicodados.ibge.gov.br/api/v1/localidades/municipios?view=nivelado'

# Getting all data CONTENT
result = requests.get(url).content

# 1 - Reading Json with Pandas
# 2 - Creating DataFrame from JSON
# 3 - Droping Duplicas if have any
df = pd.DataFrame(pd.read_json(result,orient='records')).drop_duplicates()

# 1-  Selecting only two coluns, City and State
# 2 - Ordering by city name ascending
df = (df[['municipio-nome','UF-sigla']].sort_values(by=['municipio-nome'],ascending=True))

