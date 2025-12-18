/**
 * @module translation/presentation
 * Core presentation logic for translation question flow.
 * Manages timers, pause states, and question progression.
 */

import {
  SELECTORS,
  getParameters,
  getAnswerElement
} from '/static/js/lang/study/getters.js';
import {
  showAnswer,
  hideAnswer,
  updatePauseButtonText,
} from '/static/js/lang/study/helpers.js';

// Timer references
let questionTimer = null;
let answerTimer = null;
let isPaused = false;

// Constants
const SECONDS_TO_MS = 1000;
const DEFAULT_TIMEOUT = 3; 

/**
 * Updates to the next question.
 * Clears timers, resets UI state, and fetches new presentation case via HTMX.
 * @returns {void}
 */
export function updateQuestion() {
  const parameters = getParameters();

  // Reset state
  resetPause();
  clearTimers();
  hideAnswer();
  updatePauseButtonText();

  // Request bew case
  htmx
    .ajax('GET', parameters.url, SELECTORS.PRESENTATION_BLOCK)
    .catch((error) => {
      appLogger.error('Failed to update presentation:', error);
    });
}

/**
 * Skips to next phase: question → answer, or answer → next question.
 * If question is active: shows answer immediately.
 * If answer is active: shows next question immediately.
 * Updates pause state and UI controls.
 * @returns {void}
 */
export function skipToNext() {
  const answerElement = getAnswerElement();
  const isAnswerVisible = answerElement && !answerElement.classList.contains('invisible');

  if (!isAnswerVisible) {
    clearTimers();
    showAnswer();
    startAnswerTimer();
  } else if (answerTimer) {
    clearTimers();
    updateQuestion();
  } else {
    return;
  }

  resetPause();
  updatePauseButtonText();
}

/**
 * Safely gets timeout value with fallback.
 * @param {number} timeout - Timeout in seconds
 * @returns {number} Timeout in milliseconds
 */
function getTimeoutMs(timeout) {
  const value = Number(timeout);
  return (!isNaN(value) && value > 0) 
    ? value * SECONDS_TO_MS 
    : DEFAULT_TIMEOUT * SECONDS_TO_MS;
}

/**
 * Sets timers for question and answer display sequence.
 * Uses questionTimeout for question, answerTimeout for answer.
 * Resets pause state and updates UI controls.
 * @throws {Error} If timer initialization fails
 * @returns {void}
 */
export function setTimers() {
  const parameters = getParameters();

  clearTimers();
  resetPause();
  updatePauseButtonText();

  try {
    const questionTimeoutMs = getTimeoutMs(parameters?.questionTimeout);
    
    questionTimer = setTimeout(() => {
      showAnswer();
      startAnswerTimer();
    }, questionTimeoutMs);
    
    console.log(`Timers set: question=${questionTimeoutMs}ms`);
  } catch (error) {
    console.error('Failed to set timers:', error);
    clearTimers();
    throw error;
  }
}

/**
 * Starts timer for answer display phase.
 * Automatically advances to next question after answerTimeout.
 * @returns {void}
 */
function startAnswerTimer() {
  const parameters = getParameters();
  const answerTimeoutMs = getTimeoutMs(parameters?.answerTimeout);
  
  answerTimer = setTimeout(updateQuestion, answerTimeoutMs);
  console.log(`Answer timer: ${answerTimeoutMs}ms`);
}

/**
 * Clears all active timers safely.
 * Prevents memory leaks and ensures clean state.
 * @returns {void}
 */
export function clearTimers() {
  if (questionTimer) {
    clearTimeout(questionTimer);
    questionTimer = null;
  }
  if (answerTimer) {
    clearTimeout(answerTimer);
    answerTimer = null;
  }
}

/**
 * Resets pause state to active (not paused).
 * @returns {void}
 */
export function resetPause() {
  isPaused = false;
}

/**
 * Gets current pause state.
 * @returns {boolean} True if presentation is paused, false otherwise
 */
export function getPauseState() {
  return isPaused;
}

/**
 * Toggles pause state between paused and active.
 * @returns {void}
 */
export function revertPauseState() {
  isPaused = !isPaused;
}
