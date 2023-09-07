import pandas as pd
import hashlib

usr_df = pd.read_csv('Generated_Data/users.csv')
usr_df['password_hash'] = usr_df['user_id'].apply(lambda x: hashlib.sha256(x.encode()).hexdigest())

usr_df.to_csv('Generated_Data/users.csv', index=False)