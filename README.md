# Proxy Server for FUXLOG

### Requirement
`Python 3.11`


### Note
#### Authentication USERNAME/PASSWORD Request
```
+---------+------+-------+------+-------+
| VERSION | ULEN | UNAME | PLEN | PWORD |
+---------+------+-------+------+-------+
|    1    |   1  |  255  |   1  |  255  |
+---------+------+-------+------+-------+
```

`VERSION` must be 1 - Authentication Version


#### Resigter Authentication USERNAME/PASSWORD Request
```
+---------+------+-------+------+-------+
| VERSION | ULEN | UNAME | PLEN | PWORD |
+---------+------+-------+------+-------+
|    1    |   1  |  255  |   1  |  255  |
+---------+------+-------+------+-------+
```

`VERSION` must be 2 - Register Version

Reply from server
```
+---------+--------+
| VERSION | STATUS |
+---------+--------+
|    1    |   1    |
+---------+--------+
```

`STATUS`: 
- 0 Succeeded
- 1 Invalid USERNAME or PASSWORD
    - Required at least 8 characters
    - USERNAME only accept [a-z][0-9]
    - PASSWORD only accept [a-z][A-Z][0-9][!@#$%^&*()_+-=?]
- 2 USERNAME is existed
- 3 General failure from server (Connection/Session/...)