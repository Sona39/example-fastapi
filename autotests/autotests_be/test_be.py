# import pytest
# import aiohttp
# from playwright.async_api import async_playwright
# from data import generate_random_email, generate_random_post_content, generate_random_post_title


# random_email = generate_random_email()
# random_title = generate_random_post_title()
# random_content = generate_random_post_content()

# curr_email = random_email
# curr_title = random_title
# curr_content = random_content

# first_name = "Sona"
# last_name = "Ghazaryan"
# password = "Password1!"

# BASE_URL = "https://api.ferny.xyz" 

# @pytest.mark.asyncio
# async def test_create_acc():

#     # Use aiohttp to test the backend
#     async with aiohttp.ClientSession() as session:
#         # Step 3a: Create a new user
#         create_post_url = f"{BASE_URL}/posts/"
#         request_data = {
#         "title": "new post",
#         "content": "new content"
#         }

#         # successful account creation
#         async with session.post(create_post_url, json=request_data) as response:
#             assert response.status == 201
#             response_json = await response.json()
#             assert request_data["title"] == response_json["title"]
#             assert request_data["content"] == response_json["content"]
#             assert curr_email == response_json["email"]
#             assert type(response_json["id"]) == int


# @pytest.mark.asyncio
# async def test_registered_email():

#     # Use aiohttp to test the backend
#     async with aiohttp.ClientSession() as session:

#         create_user_url = f"{BASE_URL}/users/"
#         request_data = {
#             "first_name": first_name,
#             "last_name": last_name,
#             "email": curr_email,
#             "password": password
#         }

#         error_detail = "Email already registered"

#         # email already registered
#         async with session.post(create_user_url, json=request_data) as response:
#             assert response.status == 400
#             response_json = await response.json()
            
#             assert error_detail == response_json["detail"]



# @pytest.mark.asyncio
# async def test_register_without_first_name():

#     # Use aiohttp to test the backend
#     async with aiohttp.ClientSession() as session:

#         create_user_url = f"{BASE_URL}/users/"


#         initial_request_data = {
#             "first_name": first_name,
#             "last_name": last_name,
#             "email": random_email,
#             "password": password
#         }

#         for i in range(3):
#             request_data = initial_request_data[i]


#         # checking if we receive the correct error when not sending the first_name
#         async with session.post(create_user_url, json=request_data) as response:
#             assert response.status == 422
#             response_json = await response.json()
            
#             detail = response_json["detail"][0]
            
#             # checks that the type has a "missing" value 
#             assert detail["type"] == "missing"

#             # checks that the loc indicates which values are missing 
#             assert detail["loc"][0] == "body"
#             assert detail["loc"][1] == "first_name"

#             # checks that the msg has a "Field required" value 
#             assert detail["msg"] == "Field required"

#             # checks that the input array contains what was sent in the request 
#             assert detail["input"] == request_data