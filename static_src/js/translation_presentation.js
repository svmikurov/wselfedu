'use strict';

/**
 * Presentation study module for managing timed presentation flow
 * @module presentationStudy
 */

// Timing constants (in milliseconds)
const PRESENTATION_TIMEOUT = 2000;
const ANSWER_TIMEOUT = 1000;

// Timer references
let presentationTimer = null;
let answerTimer = null;

/**
 * DOM element selectors used throughout the module
 * @constant {Object} SELECTORS
 * @property {string} ANSWER - CSS selector for answer element
 * @property {string} PRESENTATION_BLOCK - CSS selector for main presentation container
 * @property {string} UPDATE_TRIGGER - CSS selector for update trigger element
 */
const SELECTORS = {
    ANSWER: '#answer',
    PRESENTATION_BLOCK: '#presentation-block',
    UPDATE_TRIGGER: '#update-presentation'
};

/**
 * Target element ID for HTMX event filtering
 * @constant {string} TARGET_ID
 */
const TARGET_ID = 'presentation-block';

/**
 * URL path for fetching presentation data
 * @constant {string} PRESENTATION_URL_PATH
 */
const PRESENTATION_URL_PATH = '/lang/translation/english/study/case/';

/**
 * Retrieves the answer element from DOM
 * @returns {HTMLElement|null} Answer element or null if not found
 */
function getAnswerElement() {
    return document.querySelector(SELECTORS.ANSWER);
}

/**
 * Retrieves the presentation block element from DOM
 * @returns {HTMLElement|null} Presentation block element or null if not found
 */
function getPresentationBlock() {
    return document.querySelector(SELECTORS.PRESENTATION_BLOCK);
}

/**
 * Retrieves the update trigger element from DOM
 * @returns {HTMLElement|null} Update trigger element or null if not found
 */
function getUpdateTrigger() {
    return document.querySelector(SELECTORS.UPDATE_TRIGGER);
}

/**
 * Initializes HTMX event handlers when DOM is fully loaded
 * @listens DOMContentLoaded
 */
document.addEventListener('DOMContentLoaded', () => {
    const presentationBlock = getPresentationBlock();

    if (!presentationBlock) {
        console.error('Presentation block element not found');
        return;
    }

    presentationBlock.addEventListener('htmx:afterSwap', onPresentationBlockUpdate);
});

/**
 * Handles HTMX afterSwap event for presentation block updates
 * @param {Event} event - HTMX afterSwap event object
 * @listens htmx:afterSwap
 */
function onPresentationBlockUpdate(event) {
    // Validate HTTP response status
    if (event.detail?.xhr?.status !== 200) {
        console.warn('Presentation update request failed');
        return;
    }

    setTimers();
}

/**
 * Updates the presentation case by fetching new data and hiding current answer
 */
function updatePresentationCase() {
    hideAnswer();
    clearTimers(); // Clear existing timers before new update

    const updateTrigger = getUpdateTrigger();

    if (updateTrigger) {
        htmx.ajax(
            'GET',
            PRESENTATION_URL_PATH,
            SELECTORS.PRESENTATION_BLOCK
        );
    } else {
        console.error('Update trigger element not found');
    }
}

/**
 * Makes the answer element visible by removing 'invisible' class
 */
function showAnswer() {
    const answerElement = getAnswerElement();
    if (answerElement) {
        answerElement.classList.remove('invisible');
    }
}

/**
 * Hides the answer element by adding 'invisible' class
 */
function hideAnswer() {
    const answerElement = getAnswerElement();
    if (answerElement) {
        answerElement.classList.add('invisible');
    }
}

/**
 * Clears all active timers
 */
function clearTimers() {
    if (presentationTimer) {
        clearTimeout(presentationTimer);
        presentationTimer = null;
    }
    if (answerTimer) {
        clearTimeout(answerTimer);
        answerTimer = null;
    }
}

/**
 * Sets timers for automatic presentation flow
 * @throws {Error} If timers cannot be set properly
 */
function setTimers() {
    clearTimers(); // Clear any existing timers first

    try {
        presentationTimer = setTimeout(updatePresentationCase, PRESENTATION_TIMEOUT);
        answerTimer = setTimeout(showAnswer, ANSWER_TIMEOUT);
    } catch (error) {
        console.error('Failed to set timers:', error);
        clearTimers();
        throw error;
    }
}

// Cleanup event listeners
window.addEventListener('beforeunload', clearTimers);
window.addEventListener('pagehide', clearTimers);

/**
 * Clears timers when presentation block is about to be swapped
 * @listens htmx:beforeSwap
 */
document.addEventListener('htmx:beforeSwap', (event) => {
    if (event.detail?.target?.id === TARGET_ID) {
        clearTimers();
    }
});
