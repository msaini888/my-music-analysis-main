#client_id = '575003a724fb4f64bebd10949606f9e5'
#client_secret = '9f70d62278184dbc929af2c840ad7195'
#username = 'a07wqhmlqmvs0lfjbckmgiizu'
#redirect_uri = 'http://localhost:7777/callback'
#scope = 'user-read-recently-played'

import os

client_id = os.environ.get('CLIENT_ID')
print(client_id)