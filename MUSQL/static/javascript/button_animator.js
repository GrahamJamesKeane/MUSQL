/**
 * Animates buttons on hover/focus with a GIF image.
 * @param {string} static_image - The path to the static button image.
 * @param {string} gif - The path to the animated GIF image.
 */
function button_animator(static_image, gif) {
  const buttons = document.querySelectorAll('.button-container');

  buttons.forEach(button => {
    const img = button.querySelector('img');

    // Load the GIF image before hover
    const gifImage = new Image();
    gifImage.src = gif;

    // On hover, replace the static image with the animated GIF
    button.addEventListener('mouseenter', () => {
      img.src = gif;
      img.classList.add('gif');
      button.classList.remove('focus');
    });

    // On leave, revert to the static image
    button.addEventListener('mouseleave', () => {
      img.src = static_image;
      img.classList.remove('gif');
      button.classList.remove('focus');
    });

    // On focus, add the focus class to enable the transition effect
    button.addEventListener('focus', () => {
      button.classList.add('focus');
    });

    // On blur, remove the focus class to disable the transition effect
    button.addEventListener('blur', () => {
      button.classList.remove('focus');
    });
  });
}
