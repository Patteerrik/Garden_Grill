// Adds an event handler to load the map when the "Load Map" button is clicked (main page)
document.addEventListener('DOMContentLoaded', function () {
    var loadMapBtn = document.getElementById("load-map-btn");

    if (loadMapBtn) {
        loadMapBtn.addEventListener("click", function () {
            var mapContainer = document.getElementById("map-container");
            mapContainer.innerHTML = `
                <iframe src="https://maps.google.com/maps?q=59.327597,18.035186&t=&z=13&ie=UTF8&iwloc=&output=embed" 
                        style="border:0;" loading="lazy" allowfullscreen="" aria-hidden="false" tabindex="0"></iframe>
            `;

            // Change top value for .map-title when map is displayed
            var mapTitle = document.querySelector(".map-title");
            if (mapTitle) {
                mapTitle.style.top = "25px"; // Change top value to 25px when map is displayed
            }

            this.style.display = 'none'; // Hides button when maps is loaded
        });
    }
});

// Contact us page

/* jshint esversion: 6 */
(function () {
    'use strict';
    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault(); // Prevent form submission if invalid
                    event.stopPropagation();
                }
                form.classList.add('was-validated'); // Add validation styles to the form
            }, false);
        });
    // Alert fade-out logic
    document.addEventListener('DOMContentLoaded', function () {
        const alert = document.querySelector('.contact-us-alert');

        if (alert) {
            // Fade out the alert after 3 seconds
            setTimeout(function () {
                alert.style.transition = "opacity 1s";
                alert.style.opacity = 0;

                // Remove the alert from DOM after fading out
                setTimeout(function () {
                    alert.remove();
                }, 1000);
            }, 3000);
        }
    });

    // Remove green checkmark on server validation failure
    document.querySelectorAll('.form-control').forEach(function (input) {
        if (input.value && input.classList.contains('is-invalid')) {
            input.classList.remove('is-valid'); // Remove valid class if the field is invalid
        }
    });
})();

// Create reservation

/* jshint esversion: 6 */
(function () {
    'use strict';
    // Select all forms with class 'needs-validation'
    const forms = document.querySelectorAll('.needs-validation');

    // Turn the list of forms into an array, then go through each form
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            // Add a 'submit' event listener to each form
            form.addEventListener('submit', function (event) {
                // Prevent submission if form is invalid
                if (!form.checkValidity()) {
                    event.preventDefault(); // Stop form submission
                    event.stopPropagation(); // Prevent the event from affecting other elements
                }
                // Add validation classes to the form
                form.classList.add('was-validated');
            }, false);
        });

    // Hide alert after 3 seconds
    document.addEventListener('DOMContentLoaded', function () {
        const alert = document.querySelector('.alert');
        if (alert) {
            setTimeout(function () {
                alert.style.transition = "opacity 1s";
                alert.style.opacity = 0; // Fade out the alert
                setTimeout(function () {
                    alert.remove(); // Remove the alert from the DOM after fade out
                }, 1000);
            }, 3000); 
        }
    });
})();

// List reservation

/* jshint esversion: 6 */
// Automatically hide alerts after 3 seconds
setTimeout(function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        alert.style.transition = 'opacity 1s ease-out'; // Fade-out transition
        alert.style.opacity = '0'; // Set alert opacity to 0 for fade out effect
        setTimeout(function() {
            alert.remove(); // Remove alert from DOM after fade out
        }, 1000);
    });
}, 3000);  // 3 seconds delay before fading out

// Register page

/* jshint esversion: 6 */
(function () {
    'use strict';
    // Form validation for register page
    const forms = document.querySelectorAll('.needs-validation');
    // Apply validation to each form
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault(); // Stop form submission if invalid
                    event.stopPropagation(); // Prevent the event from affecting other elements
                }
                form.classList.add('was-validated'); // Add validation styles to the form
            }, false);
        });
    
    // Hide alert after 3 seconds
    document.addEventListener('DOMContentLoaded', function () {
        const alert = document.querySelector('.alert');
        if (alert) {
            setTimeout(function () {
                alert.style.transition = "opacity 1s";
                alert.style.opacity = 0; // Fade out the alert
                setTimeout(function () {
                    alert.remove(); // Remove alert from DOM after fading out
                }, 1000);
            }, 3000);
        }
    });
})();

// Log in

/* jshint esversion: 6 */
(function () {
    'use strict';
    // Apply validation to forms in the login page
    const forms = document.querySelectorAll('.needs-validation');

    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault(); // Prevent form submission if invalid
                    event.stopPropagation(); // Prevent the event from affecting other elements
                }
                form.classList.add('was-validated'); // Add validation styles to the form
            }, false);
        });

    // Hide alert after 3 seconds
    document.addEventListener('DOMContentLoaded', function () {
        const alert = document.querySelector('.alert');
        if (alert) {
            setTimeout(function () {
                alert.style.transition = "opacity 1s";
                alert.style.opacity = 0; // Fade out the alert
                setTimeout(function () {
                    alert.remove(); // Remove alert from DOM after fading out
                }, 1000);
            }, 3000);
        }
    });
})();