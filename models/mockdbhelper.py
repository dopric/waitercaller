MOCK_USERS = [
    {
        "email": "opric.dragan@gmail.com",
        "salt": 'Y37obUlflryl5E0OFtX2zGqbazo=',
        "hashed": '314b2a592b2de08e1aeb4e1055996940047683b4d4d361eada63ab6e8b71f4df2f2d17f290e3dd78d7ddca69078db20abfeca25b15987a0f6bb9effa6cf78c00'
    }
]


class MockDbHelper:

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
