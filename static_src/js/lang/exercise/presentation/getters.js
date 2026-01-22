/**
 * @module presentation/getters
 * DOM element selectors, IDs, and getter functions for the translation presentation.
 * Provides centralized access to DOM elements and configuration parameters.
 */

export const DOM_IDS = {
  SETTINGS_BLOCK: 'settings-block',
  ANSWER: 'answer',
  PRESENTATION_BLOCK: 'presentation-block',
  UPDATE_TRIGGER: 'update-presentation',
  KNOWN_BUTTON: 'known-button',
  UNKNOWN_BUTTON: 'unknown-button',
  NEXT_BUTTON: 'next-button',
  SHOW_BUTTON: 'show-button',
  PAUSE_BUTTON: 'pause-button',
};

/**
 * DOM element selectors used throughout the module.
 * @constant {Object} SELECTORS
 * @property {string} ANSWER - CSS selector for answer element
 * @property {string} PRESENTATION_BLOCK - CSS selector for main presentation container
 * @property {string} UPDATE_TRIGGER - CSS selector for update trigger element
 * @property {string} KNOWN_BUTTON - CSS selector for "I know" button
 * @property {string} UNKNOWN_BUTTON - CSS selector for "I don't know" button
 * @property {string} NEXT_BUTTON - CSS selector for "Next question" button
 * @property {string} SHOW_BUTTON - CSS selector for "Show answer" button
 * @property {string} PAUSE_BUTTON - CSS selector for "Pause" button
 */
export const SELECTORS = {
  ANSWER: '#answer',
  PRESENTATION_BLOCK: '#presentation-block',
  UPDATE_TRIGGER: '#update-presentation',
  KNOWN_BUTTON: '#known-button',
  UNKNOWN_BUTTON: '#unknown-button',
  NEXT_BUTTON: '#next-button',
  SHOW_BUTTON: '#show-button',
  PAUSE_BUTTON: '#pause-button',
};

/**
 * Creates a generic DOM element getter function.
 * @param {string} selector - CSS selector string
 * @returns {Function} Function that returns the element or null if not found
 */
function createElementGetter(selector) {
  return () => document.querySelector(selector);
}

// Element getters
export const getAnswerElement = createElementGetter(SELECTORS.ANSWER);
export const getPresentationBlock = createElementGetter(
  SELECTORS.PRESENTATION_BLOCK,
);
export const getKnownButton = createElementGetter(SELECTORS.KNOWN_BUTTON);
export const getUnknownButton = createElementGetter(SELECTORS.UNKNOWN_BUTTON);
export const getPauseButton = createElementGetter(SELECTORS.PAUSE_BUTTON);

/**
 * Retrieves presentation parameters from the parameters block element.
 * @returns {Object} Presentation configuration object
 * @property {number} questionTimeout - Question display timeout in milliseconds
 * @property {number} answerTimeout - Answer reveal timeout in milliseconds
 * @property {string} url - URL endpoint for fetching presentation cases
 */
export function getParameters() {
  const block = document.getElementById(DOM_IDS.SETTINGS_BLOCK);
  return {
    questionTimeout: parseInt(block?.dataset.question),
    answerTimeout: parseInt(block?.dataset.answer),
    url: block?.dataset.url,
  };
}

/**
 * Retrieves translation study case parameters
 * from the parameters block element
 * to request presentation case.
 * @returns {Object} Case parameters
 */
export function getCaseParameters() {
  const block = document.getElementById(DOM_IDS.SETTINGS_BLOCK);

  return {
    category: block?.dataset.category,
    mark: block?.dataset.mark,
    source: block?.dataset.source,
    start_period: block?.dataset.startPeriod,
    end_period: block?.dataset.endPeriod,
    translation_order: block?.dataset.translationOrder,
    word_count: block?.dataset.wordCount,
  };
}