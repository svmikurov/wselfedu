/**
 * @module presentation/helpers
 * Utility functions for managing UI state in the translation presentation.
 * Handles answer visibility and button text updates.
 */

import { getPauseState } from '/static/js/lang/presentation/presentation.js';
import {
  getKnownButton,
  getUnknownButton,
  getAnswerElement,
  getPauseButton,
} from '/static/js/lang/presentation/getters.js';

/**
 * Shows the answer element by removing the 'invisible' CSS class.
 * @returns {void}
 */
export function showAnswer() {
  const answerElement = getAnswerElement();

  if (answerElement) {
    answerElement.classList.remove('invisible');
  }
}

/**
 * Hides the answer element by adding the 'invisible' CSS class.
 * @returns {void}
 */
export function hideAnswer() {
  const answerElement = getAnswerElement();

  if (answerElement) {
    answerElement.classList.add('invisible');
  }
}

/**
 * Updates the pause button text based on current pause state.
 * Shows "Продолжить" when paused, "Пауза" when active.
 * @returns {void}
 */
export function updatePauseButtonText() {
  const pauseButton = getPauseButton();

  if (pauseButton) {
    pauseButton.textContent = getPauseState() ? 'Продолжить' : 'Пауза';
  }
}

export function disableMarkKnown() {
  getKnownButton().disabled = true;
  getUnknownButton().disabled = true;
}
