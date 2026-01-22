document.addEventListener('DOMContentLoaded', () => {
  const testBlock = document.querySelector('#test-block');

  if (!testBlock) {
    appLogger.error('Test block element not found');
    return;
  }

  testBlock.addEventListener(
    'htmx:afterSwap',
    onTestBlockUpdate,
  );

  // Start test
  updateTest();
});


function onTestBlockUpdate(event) {
  if (event.detail?.xhr?.status !== 200) {
    appLogger.console.warn('Test update request failed');
    return;
  }
}


function updateTest() {
  htmx
    .ajax(
      'POST',
      '',
      {
        values: {status: 'new_case'},
        target: '#test-block',
      }
    )
    .catch((error) => {
      appLogger.error('Failed to update test:', error);
    });
}
