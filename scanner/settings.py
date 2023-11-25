# Main

db_name = "profiles.db"
log_level = "INFO"
max_page_views = 30
months_to_revisit_alumni = 3
months_to_revisit_non_alumni = 6
batch_size_for_reviewing_non_alumni = 20
batch_size_for_reviewing_new_profiles = 20


# browserhelper.py
buffer_seconds_after_page_get = 1
max_time_for_load = 10
sleep_after_js_load = 0.5

# crawler.py
sleep_between_profiles = 8


# loginreader.py
login_url = "https://www.linkedin.com/login/"
login_username_input_id = 'username'
login_password_input_id = 'password'
post_login_landing_url_snippet = 'feed'

# pagereader.py
profile_id_selector = 'a[href^="https://www.linkedin.com/in/"]:not([href^="https://www.linkedin.com/in/AC"])'

# profilereader.py
wait_for_element_on_profile_page = 'h1'
education_details_path = 'details/education/'
wait_for_element_on_education_page = '.scaffold-layout__main h2'
selector_for_is_alum = '.scaffold-layout__main a[href*="https://www.linkedin.com/company/36631/"]'
selector_for_get_name = 'h1'
selector_for_get_location = ':is(.pv-text-details__right-panel, .pv-text-details__left-panel--full-width) + div > span:first-of-type'
selector_for_get_connections = '.pv-top-card--list > :last-child > span > span'

# searchreader.py
selector_for_search_input = '.search-global-typeahead__input'