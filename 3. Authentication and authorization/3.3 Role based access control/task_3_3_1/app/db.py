CRUD = ('create', 'read', 'update', 'delete')
create = 0b1000
read = 0b0100
update = 0b0010
delete = 0b0001

USERS_DATA = {
    "admin": {"username": "admin", "password": "adminpass", "role": "admin", 'permissions': create | read | update | delete},
    "user": {"username": "user", "password": "userpass", "role": "user", 'permissions': read | update},
    "user": {"username": "guest", "password": "guestpass", "role": "guest", 'permissions': read}
}
