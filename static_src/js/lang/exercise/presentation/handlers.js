/**
 * @module presentation/controls
 * Module for handling UI control interactions in the translation presentation.
 * Uses event delegation to manage dynamic buttons and controls presentation state.
 */

import { DOM_IDS } from '/static/js/lang/exercise/presentation/getters.js';
import {
  updateQuestion,
  getPauseState,
  revertPauseState,
  clearTimers,
  setTimers,
  skipToNext,
} from '/static/js/lang/exercise/presentation/presentation.js';
import {
  updatePauseButtonText,
  disableMarkKnown,
} from '/static/js/lang/exercise/presentation/helpers.js';

/**
 * Sets up event delegation for all control buttons.
 * Handles clicks on dynamically updated buttons via HTMX.
 */
export function setupEventDelegation() {
  document.addEventListener('click', (event) => {
    const target = event.target.closest('button');
    if (!target) return;

    switch (target.id) {
      case DOM_IDS.KNOWN_BUTTON:
        handleKnown();
        disableMarkKnown();
        event.preventDefault(); // Preventing possible duplication
        break;
      case DOM_IDS.UNKNOWN_BUTTON:
        skipToNext();
        disableMarkKnown();
        event.preventDefault();
        break;
      case DOM_IDS.NEXT_BUTTON:
        updateQuestion();
        event.preventDefault();
        break;
      case DOM_IDS.SHOW_BUTTON:
        skipToNext();
        event.preventDefault();
        break;
      case DOM_IDS.PAUSE_BUTTON:
        togglePause();
        event.preventDefault();
        break;
    }
  });
}

/**
 * Handles "I know" button click.
 * Updates question when user knows the current answer.
 * @throws {Error} If question update fails
 */
export function handleKnown() {
  appLogger.debug(
    '[handleKnown] "I know" button clicked, initiating question update',
  );

  try {
    updateQuestion();
    appLogger.info('[handleKnown] Question successfully updated');
  } catch (error) {
    appLogger.error('[handleKnown] Failed to update question:', error);
    throw error;
  }
}

/**
 * Handles "I don't know" button click.
 * Marks current question as unknown and updates to next question.
 */
export function handleUnknown() {
  appLogger.debug('[handleKnown] "I don\'t know" button clicked');

  try {
    appLogger.debug(
      '[handleUnknown] "I know" btn click, updating question ...',
    );
    updateQuestion();
    appLogger.info('[handleUnknown] Question updated successfully');
  } catch (error) {
    appLogger.error('[handleUnknown] Failed to update question:', error);
  }
}

/**
 * Toggles pause state for presentation timers.
 * Clears timers when paused, restarts them when resumed.
 */
export function togglePause() {
  revertPauseState();

  if (getPauseState()) {
    clearTimers();
    appLogger.info('[togglePause] Pause toggled to: PAUSED');
  } else {
    setTimers();
    appLogger.info('[togglePause] Pause toggled to: RESUMED');
  }

  updatePauseButtonText();
}
