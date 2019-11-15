import datetime

MOCK_USERS = [
    {
        "email": "opric.dragan@gmail.com",
        "salt": 'Y37obUlflryl5E0OFtX2zGqbazo=',
        "hashed": '314b2a592b2de08e1aeb4e1055996940047683b4d4d361eada63ab6e8b71f4df2f2d17f290e3dd78d7ddca69078db20abfeca25b15987a0f6bb9effa6cf78c00'
    }
]

MOCK_TABLES = [{"_id": "1", "number": "1", "owner": "test@example.com","url": "mockurl"}]


MOCK_REQUESTS = [{"_id": "1", "table_number": "1","table_id": "1", "time": datetime.datetime.now()}]

class MockDbHelper:
    def get_tables(self, owner_id):
        return MOCK_TABLES
    
    def delete_table(self, table_id):
        for i, table in enumerate(MOCK_TABLES):
            if table.get("_id") == table_id:
                del MOCK_TABLES[i]
                break

    def add_table(self, number, owner):
        MOCK_TABLES.append(
            {"_id": str(number), "number": number, "owner": owner})
        return number

    def update_table(self, _id, url):
        for table in MOCK_TABLES:
            if table.get("_id") == _id:
                table["url"] = url
                break

    def get_user(self, email):
        print("search for user ", email)
        user = [x for x in MOCK_USERS if x['email'] == email]
        if user:
            print("user found ")
            return user[0]

        print("user not registred")
        return None

    def add_user(self, email, salt, hashed):
        MOCK_USERS.append({"email": email, "salt": salt, "hashed": hashed})

    def get_requests(self, request_id):
        return MOCK_REQUESTS

    def delete_request(self, request_id):
        for i, request in enumerate(MOCK_REQUESTS):
            if request['_id'] == request_id:
                del MOCK_REQUESTS[i]
                break
