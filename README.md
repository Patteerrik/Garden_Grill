# Garden adn Grill

* Garden and Grill is a fictional restaurant located in the centre of stockholm. It is a full-stack web project built using the Django MVC framework. The project aims to provide a user friendly platform where customers can make table reservations at the restaurant "Garden & Grill." The system has been developed with a focus on user experience, security, and efficient reservation management, both for restaurant administrators and guests. [The live link can be found here:](https://gardengrill-d40b8e344381.herokuapp.com/)

![Alt text](main/static/images/AmIResponsive.png)

## Agile planning

## Features

### Users (Guests)
* Users can register, log in and log out.
* Guests can book a table using a simpl form where they enter their name, date, time and number of guests.
* Guests can manage their booking by sending a request email to the restaurant.
* When a reservation is created, updated or canceled the user recieves a confirmation email.


### Administrators
* Administrators have access to a list that displays all current reservations and can edit or cancel reservations.
* Administrators can see available spots so that admin have a clear view on the restaurants capacity during the day.
* The system automatically removes expired reservations to ensure it remains up to date.

## Tecknologies used
* Django
* Html
* CSS
* Javascript
* Python
* Bootstrap


### Navigation bar 
* The navigationbar appears on every page and is responsive.
* It helps to organize content for an easy to use experience.
* Clicking on the logo will direct the user to home page.
* The Navbar looks different depending the users logged in status.

  * #### Logged-in user

  ![Alt text](main/static/images/Logged_in_user_navbar.png)

  * #### Not logged-in user

  ![Alt text](main/static/images/Not_logged_in_user_navbar.png)


## Footer

![Alt text](main/static/images/Footer.png)

## Register 

![Alt text](main/static/images/Register_readme.png)

## Login

![Alt text](main/static/images/Login_readme.png)

## Create reservation

![Alt text](main/static/images/Create_reservations_readme.png)

## My reservations

## Manage reservation (Admin)

## Edit reservation (Admin)

## Contact us 

## Bugs

## Testing and validation

## Features left to implement
* Forgot password
* Search bar so that admin can easily find existing reservations.
## Deployment