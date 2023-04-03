var form = document.querySelector('form');

/**
 *  Validates the form on submit by checking if any of the textareas are empty.
 *  If any of the textareas are empty, prompts the user if they want to submit the form anyway.
 *  @param {Event} e - The submit event object
 */
function validateForm(e) {
    let emptyFields = false;

    document.querySelectorAll('textarea').forEach((textarea) => {
        if (textarea.value.trim() === '') {
            emptyFields = true;
        }
    });

    if (emptyFields) {
        const confirmation = confirm(
            'Some answer fields are empty. Do you want to submit the assignment anyway?'
        );
        if (!confirmation) {
            e.preventDefault();
        }
    }
}

/**
 * Submits the form data and redirects to the home page upon success.
 * @async @function 
 * submitFormAndRedirect 
 * @returns {Promise<void>}
 */
async function submitFormAndRedirect() {
    const formData = new FormData(form);

    const response = await fetch(viewAssignmentUrl,
        {
            method: 'POST',
            body: formData,
        }
    );

    if (response.ok) {
        window.location.href = homeUrl;
    } else {
        alert(
            'An error occurred while submitting the assignment. Please try again.'
        );
    }
}

/**
 * Prevents the default behavior of the event and displays a confirmation message if the user tries to leave the page. 
 * If the user confirms, it calls the 'submitFormAndRedirect' function to submit the form and redirect to the home page. 
 * @param {Event} e - The event object. 
 * @returns {void}
 */
function submitOnLeave(e) {
    e.preventDefault();

    if (e.currentTarget.confirmNavigation) {
        return;
    }

    const confirmation = confirm('Are you sure you want to leave? This will submit the assignment.');
    if (confirmation) {
        e.currentTarget.confirmNavigation = true;
        submitFormAndRedirect();
    }
}

window.addEventListener('beforeunload', submitOnLeave);

form.addEventListener('submit', async function (e) {
    validateForm(e);
});

document.querySelectorAll('.nav-menu a').forEach((navLink) => {
    navLink.addEventListener('click', submitOnLeave);
});