import pytest
import asyncio
from playwright.async_api import async_playwright, expect
from .utils import generate_random_email, generate_random_post_content, generate_random_post_title

random_email = generate_random_email()
random_title = generate_random_post_title()
random_content = generate_random_post_content()

curr_email = random_email
curr_title = random_title
curr_content = random_content

first_name = "Sona"
last_name = "Ghazaryan"
password = "Password1!"



@pytest.mark.asyncio
async def test_creating_account():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://sonagh.xyz/")
        
        # Goes to the feed and clicks on the  Register button
        button = page.get_by_text("Register")
        await button.click()

        # Fills the "First Name:" field
        xpath = "/html/body/div/div/div/div/form/div[1]/input"  
        name_field = page.locator(f'xpath={xpath}')
        await name_field.fill(first_name)

        # Fills the "Last Name:" field
        xpath = "/html/body/div/div/div/div/form/div[2]/input"  
        surname_field = page.locator(f'xpath={xpath}')
        await surname_field.fill(last_name)

        # Fills the "Email:" field
        xpath = "/html/body/div/div/div/div/form/div[3]/input"  
        email_field = page.locator(f'xpath={xpath}')
        await email_field.fill(random_email)

        # Fills the "Password:" field
        xpath = "/html/body/div/div/div/div/form/div[4]/div/input"  
        password_field = page.locator(f'xpath={xpath}')
        await password_field.fill(password)

        # Clicks on the "Register" button
        xpath = "/html/body/div/div/div/div/form/button"  
        register_btn = page.locator(f'xpath={xpath}')     
        await register_btn.click()

        xpath = '/html/body/div/div/div/div/h2'
        element = page.locator(f'xpath={xpath}')
        await expect(element).to_have_text("Login") 

        await browser.close()


@pytest.mark.asyncio
async def test_login():
    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://sonagh.xyz/")
        
        # Goes to the feed and clicks on the Login button
        button = page.get_by_text("Login")
        await button.click()

        # Fills the "Email:" field
        xpath = "/html/body/div/div/div/div/form/div[1]/input"  
        email_field = page.locator(f'xpath={xpath}')
        await email_field.fill(curr_email)

        # Fills the "Password:" field
        xpath = "/html/body/div/div/div/div/form/div[2]/div/input"  
        password_field = page.locator(f'xpath={xpath}')
        await password_field.fill(password)

        # Clicks on the "LOGIN" button
        xpath = "/html/body/div/div/div/div/form/button"  
        sign_in_btn = page.locator(f'xpath={xpath}')     
        await sign_in_btn.click()  

        # Wait for a second before checking the text
        await page.wait_for_timeout(1000)
        xpath = "/html/body/div/div/header/nav/div[2]/a"
        element = page.locator(f'xpath={xpath}')
        await expect(element).to_have_text(first_name + " " + last_name)

        await browser.close()


async def login(page, email, password):
    print("Navigating to login page...")
    await page.goto("https://sonagh.xyz/login")

    # Fills the "Email:" field
    email_xpath = "/html/body/div/div/div/div/form/div[1]/input"
    email_field = page.locator(f'xpath={email_xpath}')
    await email_field.fill(email)


    # Fills the "Password:" field
    password_xpath = "/html/body/div/div/div/div/form/div[2]/div/input"
    password_field = page.locator(f'xpath={password_xpath}')
    await password_field.fill(password)


    # Clicks on the "LOGIN" button
    login_btn_xpath = "/html/body/div/div/div/div/form/button"
    login_btn = page.locator(f'xpath={login_btn_xpath}')
    await login_btn.click()
    await page.wait_for_load_state("networkidle")



@pytest.mark.asyncio
async def test_create_post():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()



        await login(page, curr_email, password)

        # Navigate to the create post page
        await page.goto("https://sonagh.xyz")

        # Fills the "Title:" field
        title_xpath = "/html/body/div/div/div/div[1]/div/form/div[1]/input"
        title_field = page.locator(f'xpath={title_xpath}')
        await title_field.fill(curr_title)

        # Fills the "Content:" field
        content_xpath = "/html/body/div/div/div/div[1]/div/form/div[2]/textarea"
        content_field = page.locator(f'xpath={content_xpath}')
        await content_field.fill(curr_content)

 
        # Clicks on the "Submit" button
        submit_btn_xpath = "/html/body/div/div/div/div[1]/div/form/button"
        submit_btn = page.locator(f'xpath={submit_btn_xpath}')
        await submit_btn.click()

        # Checks for a success message or redirect to the post page
        success_message = page.locator("text=Post created successfully")
        await expect(success_message).to_be_visible()

         # Checks if the the title of the created post is correct
        title = page.locator(f"text={curr_title}")
        await expect(title).to_be_visible()


        # Checks if the the content of the created post is correct
        content = page.locator(f"text={curr_content}")
        await expect(content).to_be_visible()

        await browser.close()



@pytest.mark.asyncio
async def test_like_post():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await login(page, curr_email, password)

        # Gets the curr post div by the title
        post = page.locator(f"div.post-item:has(h3:text('{curr_title}'))")
        
        # Get the like button
        like_button = post.locator(".like-button")

        # Get the count next to the like button
        like_count = await post.locator(".like-button span").text_content()


        # clicks on the like button
        await like_button.click()

        # Validate the like count is increased
        await expect(post.locator(".like-button span")).to_have_text(str(int(like_count) + 1))

        # clicks on the like button
        await like_button.click()

        # Validate the like count is decreased
        await expect(post.locator(".like-button span")).to_have_text(like_count)

        await browser.close()


@pytest.mark.asyncio
async def test_update_post():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await login(page, curr_email, password)

        post = page.locator(f"div.post-item:has(h3:text('{curr_title}'))")

        # Click the three-dot menu button
        three_dot_button = post.locator(".dropbtn")
        await three_dot_button.click()

        # Click the "Update" button
        update_button = post.locator("a:has-text('Update')")
        await update_button.click()

        # Add assertions or further interactions as needed
        await expect(page.locator("text=Update Post")).to_be_visible()

        xpath = "/html/body/div/div/div/form/div[1]/input"
        title_field = page.locator(f'xpath={xpath}')
        await title_field.fill(f"{curr_title} + updated")

        xpath = "/html/body/div/div/div/form/div[2]/textarea"
        content_field = page.locator(f'xpath={xpath}')
        await content_field.fill(f"{curr_content} + updated")

    
        # Clicks on the "Update" button
        xpath = "/html/body/div/div/div/form/button"  
        update_btn = page.locator(f'xpath={xpath}')     
        await update_btn.click()

        # Checks if the success message is received
        success_message = page.locator("text=Post updated successfully!")
        await expect(success_message).to_be_visible()


        # Wait for redirecting before checking the text
        await page.wait_for_timeout(2000)


        # Checks if the the title of the updated post is correct
        title = page.locator(f"text={curr_title} + updated")
        await expect(title).to_be_visible()


        # Checks if the the content of the updated post is correct
        content = page.locator(f"text={curr_content} + updated")
        await expect(content).to_be_visible()


@pytest.mark.asyncio
async def test_delete_post():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await login(page, curr_email, password)

        post = page.locator(f"div.post-item:has(h3:text('{curr_title}'))")

        # Click the three-dot menu button
        three_dot_button = post.locator(".dropbtn")
        await three_dot_button.click()

        # Click the "Update" button
        update_button = post.locator("a:has-text('Delete')")
        await update_button.click()


        # Checks if the success message is received
        success_message = page.locator("text=Post deleted successfully!")
        await expect(success_message).to_be_visible()


        # Wait for redirectio before checking the text
        await page.wait_for_timeout(1000)


        # Checks if the the title of the updated post is correct
        title = page.locator(f"text={curr_title} + updated")
        await expect(title).not_to_be_visible()


        # Checks if the the content of the updated post is correct
        content = page.locator(f"text={curr_content} + updated")
        await expect(content).not_to_be_visible()


@pytest.mark.asyncio
async def test_update_account():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await login(page, curr_email, password)

        # Clicks on the Account Name
        xpath = "/html/body/div/div/header/nav/div[2]/a"
        element = page.locator(f'xpath={xpath}')
        await element.click()

        # Checks if the the Account Details page is opened
        content = page.locator(f"text=Account Details")
        await expect(content).to_be_visible()

        # Clicks on the Edit button
        xpath = "/html/body/div/div/div/span"
        element = page.locator(f'xpath={xpath}')
        await element.click()

        # Checks if the the Re-authenticate text is displayed
        content = page.locator(f"text=Re-authenticate")
        await expect(content).to_be_visible()

        # Checks if the the Please enter your password to continue. text is displayed
        content = page.locator(f"text=Please enter your password to continue.")
        await expect(content).to_be_visible()

        # Fills in the password
        xpath = "/html/body/div/div/div/div[2]/div/input"
        password_field = page.locator(f'xpath={xpath}')
        await password_field.fill(password)

        # Clicks on the "Submit" button
        xpath = "/html/body/div/div/div/div[2]/div/button"
        element = page.locator(f'xpath={xpath}')
        await element.click()
        
        # fills the email to be updated
        xpath = "/html/body/div/div/div/div/div[1]/div/input"
        email_field = page.locator(f'xpath={xpath}')
        await email_field.fill(f"updated+{curr_email}")

        # Clicks on the checkmark icon for updating the email
        xpath = "/html/body/div/div/div/div/div[1]/div/button/img"
        element = page.locator(f'xpath={xpath}')
        await element.click()

        await page.wait_for_timeout(2000)


        # # Checks if the success message is received
        # success_message = page.locator("div.notification.success:has-text('Email updated successfully!')")
        # await expect(success_message).to_be_visible()

        # fills the First Name to be updated
        xpath = "/html/body/div/div/div/div/div[2]/div/input"
        name_field = page.locator(f'xpath={xpath}')
        await name_field.fill(f"updated+{first_name}")

        await page.wait_for_timeout(2000)


        # Clicks on the checkmark icon for updating the first name
        xpath = "/html/body/div/div/div/div/div[2]/div/button/img"
        element = page.locator(f'xpath={xpath}')
        await element.click()
        
        # # Checks if the success message is received
        # success_message = page.locator("text=First Name updated successfully!!")
        # await expect(success_message).to_be_visible()


        # fills the First Name to be updated
        xpath = "/html/body/div/div/div/div/div[3]/div/input"
        surname_field = page.locator(f'xpath={xpath}')
        await surname_field.fill(f"updated+{last_name}")

        # Clicks on the checkmark icon for updating the last name
        xpath = "/html/body/div/div/div/div/div[3]/div/button/img"
        element = page.locator(f'xpath={xpath}')
        await element.click()
        
        # # Checks if the success message is received
        # success_message = page.locator("text=Last Name updated successfully!!")
        # await expect(success_message).to_be_visible()

        # fills the password to be updated
        xpath = "/html/body/div/div/div/div/div[4]/input"
        password_field = page.locator(f'xpath={xpath}')
        await password_field.fill(f"{password}U")


        # Clicks on the checkmark icon for updating the password
        xpath = "/html/body/div/div/div/div/div[4]/button/img"
        element = page.locator(f'xpath={xpath}')
        await element.click()
        
        await page.wait_for_timeout(2000)
      
        # # Checks if the success message is received 
        # success_message = page.locator("text=Password updated successfully!!")
        # await expect(success_message).to_be_vis   ible()

        # Clicks on the Sign out
        xpath = "/html/body/div/div/header/nav/div[2]/button"
        element = page.locator(f'xpath={xpath}')
        await element.click()

        await login(page, f"updated+{curr_email}", f"{password}U")

        await page.wait_for_timeout(2000)
        # Checks if the first and last name are displayed in the header after the sign in
        xpath = "/html/body/div/div/header/nav/div[2]/a" 
        element = page.locator(f'xpath={xpath}')
        await expect(element).to_have_text(f"updated+{first_name} updated+{last_name}") 


@pytest.mark.asyncio
async def test_delete_post():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await login(page, curr_email, password)

        post = page.locator(f"div.post-item:has(h3:text('{curr_email}'))")

         # Clicks on the Account Name
        xpath = "/html/body/div/div/header/nav/div[2]/a"
        element = page.locator(f'xpath={xpath}')
        await element.click()

        # Checks if the the Account Details page is opened
        content = page.locator(f"text=Account Details")
        await expect(content).to_be_visible()

        # Clicks on the Edit button
        xpath = "/html/body/div/div/div/span"
        element = page.locator(f'xpath={xpath}')
        await element.click()

        # Checks if the the Re-authenticate text is displayed
        content = page.locator(f"text=Re-authenticate")
        await expect(content).to_be_visible()

        # Checks if the the Please enter your password to continue. text is displayed
        content = page.locator(f"text=Please enter your password to continue.")
        await expect(content).to_be_visible()

        # Fills in the password
        xpath = "/html/body/div/div/div/div[2]/div/input"
        password_field = page.locator(f'xpath={xpath}')
        await password_field.fill(password)

        # Clicks on the "Submit" button
        xpath = "/html/body/div/div/div/div[2]/div/button"
        element = page.locator(f'xpath={xpath}')
        await element.click()


@pytest.mark.asyncio
async def test_delete_account():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await login(page, f"updated+{curr_email}", f"{password}U")

         # Clicks on the Account Name
        await page.wait_for_timeout(2000)
        xpath = "/html/body/div/div/header/nav/div[2]/a"
        element = page.locator(f'xpath={xpath}')
        await element.click()

        # Clicks on the Edit button
        xpath = "/html/body/div/div/div/span"
        element = page.locator(f'xpath={xpath}')
        await element.click()


        # Fills in the password
        xpath = "/html/body/div/div/div/div[2]/div/input"
        password_field = page.locator(f'xpath={xpath}')
        await password_field.fill(f"{password}U")


        # Clicks on the "Submit" button
        xpath = "/html/body/div/div/div/div[2]/div/button"
        element = page.locator(f'xpath={xpath}')
        await element.click()

        # Clicks on the "Delete account" button 
        xpath = "/html/body/div/div/div/div/div[5]/button"
        element = page.locator(f'xpath={xpath}')
        await element.click()


        # Check if the Confirm Account Deletion text is displayed
        content = page.locator(f"text=Confirm Account Deletion")
        await expect(content).to_be_visible()

        # Check if the Are you sure you want to delete your account? text is displayed
        content = page.locator(f"text=Are you sure you want to delete your account?")
        await expect(content).to_be_visible()

        # Click on the "Delete Account" button
        xpath = "/html/body/div/div/div/div[2]/div/div/button[1]"
        element = page.locator(f"xpath={xpath}")

        # Ensure any modal is closed before clicking
        modal_close_button = page.locator("selector_for_modal_close_button")  # Update the selector
        if await modal_close_button.is_visible():
            await modal_close_button.click()

        # Attempt the click with force option
        await element.click(force=True)


        xpath = '/html/body/div/div/div/div/h2'
        element = page.locator(f'xpath={xpath}')
        await expect(element).to_have_text("Register")

        await login(page, f"updated+{curr_email}", f"{password}U")

        # Checks that the sign in with deleted account is displayed
        content = page.locator(f"text=Invalid email or password")
        await expect(content).to_be_visible()