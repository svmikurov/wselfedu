const configElement = document.getElementById('scroll-config');
const SCROLL_DELAY = configElement ? parseInt(configElement.dataset.scrollDelay) || 20 : 20;
const FORM_ID = configElement?.dataset.formId;

const CANCEL_BUTTON_ID = 'button-id-cancel'
const SUBMIT_BUTTON_ID = 'submit-id-submit'

appLogger.warn('FORM_ID:', FORM_ID ?? 'undefined');


function scrollToElement(element) {
  element?.scrollIntoView({behavior: 'smooth', block: 'start'});
}

function scrollToTop() {
  window.scrollTo({top: 0, behavior: 'smooth'});
}

document.addEventListener('htmx:afterSwap', (event) => {
  const targetId = event.detail.target.id;
  
  if (targetId === FORM_ID) {
    setTimeout(() => scrollToElement(event.detail.target), SCROLL_DELAY);
  }
});

document.addEventListener('click', (event) => {
  const targetId = event.target.id;

  if (targetId === CANCEL_BUTTON_ID) {
    setTimeout(() => scrollToTop(), SCROLL_DELAY);
  }
});