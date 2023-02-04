import datetime

products = [
    {
        "id": "14444c17-804c-46ef-8a76-0fb26ad14324",
        "name": "Edit Email",
        "description": "This extension is useful to edit email in outlook.",
        "version_id": "14444c17-804c-46ef-8a76-0fb26ad14326",
        "image": "",
        "created_on": str(datetime.date.today()),
        "modified_on": str(datetime.date.today())
    }
]

versions = [
    {
        "id": "14444c17-804c-46ef-8a76-0fb26ad14326",
        "product_id": "14444c17-804c-46ef-8a76-0fb26ad14324",
        "tag": "1.0.0",
        "currency": "USD",
        "price": 25,
        "path": "",
        "created_on": str(datetime.date.today()),
        "modified_on": str(datetime.date.today())
    }
]

transactions = [
    {
        "id": "14444c17-804c-46ef-8a76-0fb26ad14328",
        "user_id": "14444c17-804c-46ef-8a76-0fb26ad14329",
        "product_id": "14444c17-804c-46ef-8a76-0fb26ad14324",
        "version_id": "14444c17-804c-46ef-8a76-0fb26ad14326",
        "qty": 1,
        "currency": "USD",
        "price": 25,
        "total_amt": 25,
        "ordered_on": str(datetime.date.today()),
        "expired_on": str(datetime.date.today() + datetime.timedelta(days=5*365))
    }
]

users = [
    {
        "id": "14444c17-804c-46ef-8a76-0fb26ad14329",
        "email": "harshilpatel984@gmail.com",
        "first_name": "harshil",
        "last_name": "patel",
        "profile_image": "",
        "password_1": "admin@123",
        "password_2": "admin@123",
        "otp_varified": False,
    }
]