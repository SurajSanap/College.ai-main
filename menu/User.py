import asyncio
import random
import sqlite3
import string

import streamlit as st
from firebase_admin import auth, exceptions
from httpx_oauth.clients.google import GoogleOAuth2

# Initialize Streamlit title
st.title("College.ai")

# Initialize SQLite database
conn = sqlite3.connect("user_data.db")
c = conn.cursor()
c.execute(
    """CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY, username TEXT, password TEXT, email TEXT)"""
)
conn.commit()

# Initialize Google OAuth2 client
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"
redirect_url = "YOUR_REDIRECT_URL"
client = GoogleOAuth2(client_id=client_id, client_secret=client_secret)


async def get_access_token(client: GoogleOAuth2, redirect_url: str, code: str):
    """
    The function `get_access_token` asynchronously retrieves an access token from Google OAuth2 using a
    provided code and redirect URL.

    Args:
      client (GoogleOAuth2): GoogleOAuth2 instance that handles the OAuth2 authentication with Google
    APIs.
      redirect_url (str): The `redirect_url` parameter is the URL to which the user will be redirected
    after they have granted permission to the application. This URL is typically provided by the
    application as part of the OAuth2 flow to handle the authorization response.
      code (str): The `code` parameter is typically a one-time authorization code that is provided by
    the authorization server as part of the OAuth 2.0 authorization flow. This code is exchanged for an
    access token that can be used to make authenticated requests to the API on behalf of the user.

    Returns:
      The `get_access_token` function is returning the result of calling the `client.get_access_token`
    method with the provided `code` and `redirect_url` parameters.
    """
    return await client.get_access_token(code, redirect_url)


async def get_email(client: GoogleOAuth2, token: str):
    """
    The function `get_email` retrieves the user ID and email using a Google OAuth2 client and a token.

    Args:
      client (GoogleOAuth2): GoogleOAuth2 object that handles authentication and communication with
    Google APIs.
      token (str): The `token` parameter is a string that represents the authentication token used to
    access the Google API. It is passed to the `get_email` function to authenticate the user and
    retrieve their email address.

    Returns:
      The function `get_email` is returning a tuple containing the `user_id` and `user_email` obtained
    from the `client.get_id_email(token)` method.
    """
    user_id, user_email = await client.get_id_email(token)
    return user_id, user_email


def get_logged_in_user_email():
    """
    The function `get_logged_in_user_email` attempts to retrieve the logged-in user's email address
    using OAuth authentication and Firebase authentication.

    Returns:
      The function `get_logged_in_user_email` is returning the email address of the logged-in user if
    the user is successfully authenticated and their email is retrieved. If any errors occur during the
    process, the function returns `None`.
    """
    try:
        query_params = st.query_params()
        code = query_params.get("code")
        if code:
            token = asyncio.run(get_access_token(client, redirect_url, code))
            st.experimental_set_query_params()

            if token:
                user_id, user_email = asyncio.run(
                    get_email(client, token["access_token"])
                )
                if user_email:
                    try:
                        user = auth.get_user_by_email(user_email)
                    except exceptions.FirebaseError:
                        user = auth.create_user(email=user_email)
                    st.session_state.email = user.email
                    return user.email
        return None
    except:
        pass


def show_login_button():
    """
    The function `show_login_button` generates a button with a link for logging in via Google using the
    specified authorization URL and styling.
    """
    authorization_url = asyncio.run(
        client.get_authorization_url(
            redirect_url,
            scope=["email", "profile"],
            extras_params={"access_type": "offline"},
        )
    )
    button_html = f'<a href="{authorization_url}" target="_self" style="text-decoration: none;"><button style="background-color: #2F80ED; color: white; border: none; padding: 10px 20px; border-radius: 5px; font-size: 16px; cursor: pointer;">Login via Google</button></a>'
    st.markdown(button_html, unsafe_allow_html=True)


def generate_otp():
    """
    The function generates a 6-digit one-time password (OTP) using random digits.

    Returns:
      The function `generate_otp()` is returning a randomly generated 6-digit OTP (One Time Password)
    consisting of digits 0-9.
    """
    otp = "".join(random.choices(string.digits, k=6))
    return otp


def send_otp(email, otp):
    """
    The function `send_otp` takes an email and OTP as input and displays a message indicating that an
    OTP has been sent to the provided email along with the OTP value.

    Args:
      email: The `email` parameter is a string that represents the email address to which the OTP
    (One-Time Password) will be sent.
      otp: The `otp` parameter in the `send_otp` function is typically a one-time password (OTP) that is
    generated and sent to the user's email address for verification or authentication purposes. It is a
    temporary code that is usually used for a single login session or transaction to enhance security.
    """
    st.write(f"An OTP has been sent to {email}. Your OTP is: {otp}")


def main():
    """
    The `main` function in the provided Python code snippet implements an authentication portal allowing
    users to login, sign up, or recover a forgotten password.
    """
    st.write("<h1><center> Authentication Portal</center></h1>", unsafe_allow_html=True)

    if "logged_in" not in st.session_state:
        form_type = st.selectbox(
            "Login/Signup/Forgot Password", ["Login", "Sign Up", "Forgot Password"]
        )

        if form_type == "Login":
            form = st.form(key="login_form")
            form.subheader("Login")

            user = form.text_input("Username")
            password = form.text_input("Password", type="password")

            if form.form_submit_button("Login"):
                c.execute(
                    "SELECT * FROM users WHERE username=? AND password=?",
                    (user, password),
                )
                result = c.fetchone()
                if result:
                    st.session_state["user"] = user
                    st.session_state["logged_in"] = True
                    st.success("Logged in successfully!")
                else:
                    st.error("Invalid username or password")

            get_logged_in_user_email()
            show_login_button()

        elif form_type == "Sign Up":
            form = st.form(key="signup_form")
            form.subheader("Sign Up")

            new_user = form.text_input("New Username")
            new_password = form.text_input("New Password", type="password")
            email = form.text_input("Email")

            if form.form_submit_button("Sign Up"):
                c.execute(
                    "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
                    (new_user, new_password, email),
                )
                conn.commit()
                st.success("Account created successfully! Please login.")
                # st.balloons()
            get_logged_in_user_email()
            show_login_button()

        elif form_type == "Forgot Password":
            form = st.form(key="forgot_password_form")
            form.subheader("Forgot Password")

            email = form.text_input("Enter Email")

            if form.form_submit_button("Send OTP"):
                c.execute("SELECT * FROM users WHERE email=?", (email,))
                result = c.fetchone()
                if result:
                    otp = generate_otp()
                    send_otp(email, otp)
                    st.success("OTP sent successfully! Check your email.")
                else:
                    st.error("Email not found in database")

    else:
        st.subheader("Logged in")
        st.write("You are logged in as:", st.session_state["user"])

        if st.button("Logout"):
            del st.session_state["logged_in"]
            del st.session_state["user"]
            st.success("Logged out successfully!")


if __name__ == "__main__":
    main()
