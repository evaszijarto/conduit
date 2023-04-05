sign_up_user = {
    'username': 'conduit_test_user_01',
    'email': '@conduit_test_user_01.com',
    'password': 'Password123'
}

login_user = {
    'username': 'conduit_test_user_10',
    'email': '@conduit_test_user_10.com',
    'password': 'Password123'
}
user = []

btns_menu_logged_in_expected_text = [" New Article", " Settings", f'{sign_up_user["username"]}', " Log out", "Your Feed"]

btns_menu_logged_out_expected_text = ["Home", "Sign in", "Sign up", "Global Feed"]
