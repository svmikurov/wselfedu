/**
 * @module translation/initializer
 * Module for initializing and managing the translation presentation lifecycle.
 * Handles DOM setup, HTMX event integration, and resource cleanup.
 */

'use strict';

import {
  DOM_IDS,
  getPresentationBlock,
} from '/static/js/lang/study/getters.js';
import {
  setTimers,
  clearTimers,
  updateQuestion,
} from '/static/js/lang/study/presentation.js';
import { setupEventDelegation } from '/static/js/lang/study/handlers.js';

/**
 * Initializes presentation block functionality.
 * Sets up event listeners for DOM updates, user interactions, and cleanup.
 * Must be called after DOM is fully loaded.
 */
document.addEventListener('DOMContentLoaded', () => {
  const presentationBlock = getPresentationBlock();

  if (!presentationBlock) {
    appLogger.error('Presentation block element not found');
    return;
  }

  presentationBlock.addEventListener(
    'htmx:afterSwap',
    onPresentationBlockUpdate,
  );

  // Set up event delegation for all control buttons
  setupEventDelegation();
  appLogger.log('Added presentation block update listener');

  // Start presentation
  updateQuestion();
});

/**
 * Handles presentation block content updates via HTMX.
 * Starts presentation timers after successful content swap.
 * @param {Event} event - HTMX afterSwap event object
 * @property {Object} event.detail - Event details
 * @property {Object} event.detail.xhr - XHR response object
 * @property {number} event.detail.xhr.status - HTTP status code
 */
function onPresentationBlockUpdate(event) {
  if (event.detail?.xhr?.status !== 200) {
    appLogger.warn('Presentation update request failed');
    return;
  }

  // Start presentation with timeout
  setTimers();
}

/**
 * Clears timers when presentation block is about to be swapped.
 * Prevents timer leaks during dynamic content updates.
 * @listens htmx:beforeSwap
 * @param {Event} event - HTMX beforeSwap event
 * @property {Object} event.detail - Event details
 * @property {Object} event.detail.target - Target element
 * @property {string} event.detail.target.id - Target element ID
 */
document.addEventListener('htmx:beforeSwap', (event) => {
  if (event.detail?.target?.id === DOM_IDS.PRESENTATION_BLOCK) {
    clearTimers();
  }
});

// Cleanup event listeners
window.addEventListener('beforeunload', clearTimers);
window.addEventListener('pagehide', clearTimers);
