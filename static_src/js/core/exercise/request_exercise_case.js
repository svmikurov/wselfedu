// Request new exercise case on page load event

const EXERCISE_BLOCK = '#exercise-block';
const EXERCISE_DATA_ID = 'exercise-conditions';

document.addEventListener('DOMContentLoaded', () => {
  const exerciseBlock = document.querySelector(EXERCISE_BLOCK);

  if (!exerciseBlock) {
    appLogger.error('Exercise block element not found');
    return;
  }

  exerciseBlock.addEventListener('htmx:afterSwap', onExerciseBlockUpdate);
  updateExercise();
});

function onExerciseBlockUpdate(event) {
  if (event.detail?.xhr?.status !== 200) {
    appLogger.console.warn('Exercise case update request failed');
  }
}

function updateExercise() {
  htmx
    .ajax('POST', '', {
      values: getCaseParameters(),
      target: EXERCISE_BLOCK,
    })
    .catch((error) => {
      appLogger.error('Failed to update exercise case:', error);
    });
}

function getCaseParameters() {
  const block = document.getElementById(EXERCISE_DATA_ID);
  return {
    status: 'new_case',
    ...getDataParams(block),
  };
}

function getDataParams(element) {
  if (!element?.dataset) return {};
  
  return Object.keys(element.dataset).reduce((params, key) => {
    params[key.replace(/-/g, '_')] = element.dataset[key];
    return params;
  }, {});
}