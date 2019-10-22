# datajoint_seung
Datajoint databases in Seung Lab.

## Database configuration
Database location: Princeton Neuroscience Institute, Princeton University

- HOST: seungdj01.princeton.edu
- USER: Your Princeton net id (ex. jabae)
- PASSWORD: Your Princeton net id password

*You have to be affiliated with Princeton University to access the database.

### Accessing the database
```python3
import datajoint as dj

# Datajoint credentials
dj.config["database.host"] = "seungdj01.princeton.edu"
dj.config["database.user"] = "your_netid"
dj.config["database.password"] = "your_netid_pw"

dj.conn()
```

or

```python3
dj.config.load("dj_conf.json")

dj.conn()
```

#### dj_conf.json
```
{
    "database.host": "seungdj01.princeton.edu", 
    "database.password": "your_netid_password", # Need to edit
    "database.user": "your_netid", # Need to edit
    "database.port": 3306,
    "database.reconnect": true,
    "connection.init_function": null,
    "connection.charset": "",
    "loglevel": "INFO",
    "safemode": true,
    "fetch_format": "array",
    "display.limit": 50,
    "display.width": 25,
    "display.show_tuple_count": true,
    "history": [
    ]
}
```

## Pinky40
### Schema ERD

## Pinky
### Schema ERD
![](pinky/pinky_ERD.png)
