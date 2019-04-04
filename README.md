# Simple File Server

Basic run:
```
python install -r requirements.txt
python -m flask run
```

Docker run:
```
docker-compose up -d
```

After running server accessible under `http://localhost:5000/`
##Endpoints:
| Endpoint | Arguments | Response | Description |
| --- | --- | --- | --- |
| upload | file => form-data | `{ "file_id": <file_id> }` | Uploads file to server |
| <file_id> | file_id => url | file_data | Downloads file from server |

###Common responses:
| Status Code | Response data | Description |
| --- | --- | --- |
| 403 | `{"error": "authorization failed"}` | auth_code was not provided |
| 404 | `{"error": "file_not_found"}` | File was not found in files folder |


##Authentication
Server implements simple authentication: `auth_code` cookie should be same as `AUTH_CODE` environment variable.
`AUTH_CODE` can be defined in `.env` file.