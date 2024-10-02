### Manual testing

#### Navigation and Links

* For not inlogged users

| Action | Expectation| Result|
| --- | --- | --- |
| Click on all links in the navbar and footer. | The user is navigated to the correct page without errors. | The user is navigated to the correct page without errors. |
| Click on "Menu" button | The user is navigated to the "Menu" page | The user is navigated to the "Menu" page |
| Click on "log in" link in the welcome text | The user is navigated to the "Login" page | The user is navigated to the "Login" page |
| Click on "register" link in the welcome text | The user is navigated to the "Register" page | The user is navigated to the "Register" page |

* For logged in users

| Action | Expectation| Result|
| --- | --- | --- |
| Click on "Garden and Grill" logo | The user is navigated to the main page | The user is navigated to the main page |
| Click on "Create Reservation" button | The user is navigated to the "Create Reservation" page | The user is navigated to the "Create Reservation" page |
| Click on "Menu" button | The user is navigated to the "Menu" page | The user is navigated to the "Menu" page |
| Click on "Contact Us" link in the welcome text | The user is navigated to the "Contact Us" page | The user is navigated to the "Contact Us" page |


#### User Registration

| Action | Expectation | Result |
| --- | --- | --- |
| Submit registration form with valid data | The user is successfully registered and redirected. And registration email is sent to user | The user is successfully registered and redirected. And registration email is sent to user |
| Submit registration form with missing username | A message "Please fill out this field" appears | A message "Please fill out this field" appears |
| Submit registration form with missing email | A message "Please fill out this field" appears | A message "Please fill out this field" appears |
| Submit registration form with invalid email format | A message "Invalid email adress" appears | A message "Invalid email adress" appears |
| Submit registration form with missing password | A message "Please fill out this field" appears | A message "Please fill out this field" appears |
| Submit registration form with mismatched password and confirm password | A message "Passwords do not match" appears | A message "Passwords do not match" appears |
| Click on the "Login here" link on the registration page | The user is navigated to the login page | The user is navigated to the login page |

#### Login and Logout

| Action | Expectation | Result |
| --- | --- | --- |
| Log in with valid credentials | The user is logged in and redirected to main page | The user is logged in and redirected to main page |
| Enter invalid credentials on the login page | A message "Invalid username or password." appears | A message "Invalid username or password." appears |
| Log in | The user is directed to home page for logged in users | The user is directed to home page for logged in users |
| Log out after being logged in | The user is logged out and redirected to home page | The user is logged out and redirected to home page |
| User session ends when the browser is closed | The session is terminated and the user is logged out | The session is terminated and the user is logged out |
| User session ends after 10 minutes of inactivity | The session is terminated and the user is logged out | The session is terminated and the user is logged out |

#### Booking System (User)

| Action | Expectation | Result |
| --- | --- | --- |
| Click on "Edit" from "Your current reservations" page as a logged-in user | The user is navigated to the "Contact Us" page | The user is navigated to the "Contact Us" page |

##### Create reservation (User)

| Action | Expectation | Result |
| --- | --- | --- |
| Create a reservation as a guest | The reservation is created, a confirmation message with details appears, a confirmation email is sent to the user, and the reservation appears in the reservation list | The reservation is created, a confirmation message with details appears, a confirmation email is sent to the user, and the reservation appears in the reservation list |
| Submit the form without entering a username | A message "Please enter your name." appears | A message "Please enter your name." appears |
| Submit the form without entering a date | A message "Please select a date." appears | A message "Please select a date." appears |
| Attempt to book a past date | The form should prevent submission and display an appropriate error message | Not expectet result!!!! |
| Submit the form without entering a time | A message "Please select a time." appears | A message "Please select a time." appears |
| Attempt to book a time outside of restaurant hours | A message "The reservation time must be between 12:00 PM and 10:00 PM." appears | A message "The reservation time must be between 12:00 PM and 10:00 PM." appears |
| Submit the form without entering the number of guests | A message "Please enter the number of guests." appears | A message "Please enter the number of guests." appears |
| Attempt to book more than 50 seats (max capacity) for a specific time slot | A message "The selected time is fully booked." appears | A message "The selected time is fully booked." appears |

#### Booking System (Admins)

| Action | Expectation | Result |
| --- | --- | --- |
| Click on "Edit" from "Current reservations" page as a logged-in admin | The admin is navigated to the "Edit Reservation" page | The admin is navigated to the "Edit Reservation" page |
| Click on "Cancel" from "Current reservations" page as a logged in admin | A message "Reservation has been canceled. Cancellation email sent." appears, and the page refreshes | A message "Reservation has been canceled. Cancellation email sent." appears, and the page refreshes |
| Click on "Update reservation" on the "Edit Reservation" page | Admin is navigated to the "Current Reservations" page, a message "Reservation has been updated." appears, the page updates with the new information, and a confirmation email is sent to the user | Admin is navigated to the "Current Reservations" page, a message "Reservation has been updated." appears, the page updates with the new information, and a confirmation email is sent to the user |

##### Create reservation (Admin)

| Action | Expectation | Result |
| --- | --- | --- |
| Create a reservation as an admin | The reservation is created with an additional email field, a confirmation message with details appears, a confirmation email is sent, and the reservation appears in the reservation list for logged in admins | The reservation is created with an additional email field, a confirmation message with details appears, a confirmation email is sent, and the reservation appears in the reservation list for logged in admins |
| Submit the form without entering a username | A message "Please enter your name." appears | A message "Please enter your name." appears |
| Submit the form without entering a date | A message "Please select a date." appears | A message "Please select a date." appears |
| Attempt to book a past date | A message "The reservation date cannot be in the past." appears | A message "The reservation date cannot be in the past." appears |
| Attempt to book a time that has already passed today | A message "The reservation time cannot be in the past." appears | A message "The reservation time cannot be in the past." appears |
| Submit the form without entering a time | A message "Please select a time." appears | A message "Please select a time." appears |
| Attempt to book a time outside of restaurant hours | A message "The reservation time must be between 12:00 PM and 10:00 PM." appears | A message "The reservation time must be between 12:00 PM and 10:00 PM." appears |
| Submit the form without entering the number of guests | A message "Please enter the number of guests." appears | A message "Please enter the number of guests." appears |
| Submit the form without entering an email | A message "Please enter a valid email." appears | A message "Please enter a valid email." appears |
| Enter an invalid email address | A message "Invalid email address." appears | A message "Invalid email address." appears |
| Enter an email that is not registered | A message "This email is not registered. Please use a registered email." appears | A message "This email is not registered. Please use a registered email." appears |
| Attempt to book more than 50 seats (max capacity) for a specific time slot | A message "The selected time is fully booked." appears | A message "The selected time is fully booked." appears |

#### Error Pages (404 and 500)

| Action | Expectation | Result |
| --- | --- | --- |
| Visit an invalid URL | The 404 page is displayed with a message and return link | The 404 page is displayed with a message and return link |
| Trigger a server error | The 500 page is displayed with a message and return link | The 500 page is displayed with a message and return link |

#### Validator testing

##### HTML

##### CSS

##### PYTHON

##### JAVASCRIPT

#### Lighthouse testing

#### Responsiveness Testing

#### Accessibility Testing

#### Security Testing


