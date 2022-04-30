const {_electron: electron } = require('playwright')
const { test } = require('@playwright/test')
const { app } = require('electron')

test('launch app', async () => {
    const electronApp = await electron.launch({ args: ['main.js'] })
  // close app
  await electronApp.close()
})

test('start button', async () => {
    const electronApp = await electron.launch({ args: ['main.js'] })
    const appPath = await electronApp.evaluate(async ({ app }) => {
        return app.getAppPath;
    });
    const window = await electronApp.firstWindow();
    console.log(await window.title());
    await window.locator('text = START').click();
  // close app
  await electronApp.close()
})

test('stop button', async () => {
    const electronApp = await electron.launch({ args: ['main.js'] })
    const appPath = await electronApp.evaluate(async ({ app }) => {
        return app.getAppPath;
    });
    const window = await electronApp.firstWindow();
    await window.locator('text = STOP').click();
  // close app
  await electronApp.close()
})

test('selection_Browser', async () => {
    const electronApp = await electron.launch({ args: ['main.js'] })
    const appPath = await electronApp.evaluate(async ({ app }) => {
        return app.getAppPath;
    });
    const window = await electronApp.firstWindow();
    await window.selectOption('select#browser', 'Chrome');
  // close app
  await electronApp.close()
})

test('selection_MLS', async () => {
    const electronApp = await electron.launch({ args: ['main.js'] })
    const appPath = await electronApp.evaluate(async ({ app }) => {
        return app.getAppPath;
    });
    const window = await electronApp.firstWindow();
    await window.selectOption('select#MLS_site', 'Bright');
  // close app
  await electronApp.close()
})