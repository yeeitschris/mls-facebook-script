const { SIGINT } = require("constants");
const { systemPreferences } = require("electron");
const {app, BrowserWindow, ipcMain, PythonShell} = require("electron", "python-shell");

let win = null;
let script_id  = null;
let dataString = "";
const errors = [];

const createWindow = () => {
    win = new BrowserWindow({
        width: 800,
        height: 600,
        resizable: false,
        webPreferences: {
            nodeIntegration: true //access to Node funcs/APIs
        }
    })

    win.loadFile('index.html');
};

app.whenReady().then(createWindow);
//Runs back-end code based on info gathered from front-end on render.js

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') app.quit()
  })

ipcMain.on('sendInfo', (event, browser_choice, MLS_username, MLS_pw, MLS_choice, FB_email, FB_pw, data_path, price_range, zip_code, num_properties) => {
    var python = require('child_process').spawn('python', ['./Main_Runner.py', browser_choice, MLS_username, MLS_pw, MLS_choice, FB_email, FB_pw, data_path, price_range, zip_code, num_properties]);
    script_id = python.pid;
    win.webContents.send('receiveData', "");
    win.webContents.send('receivePID', script_id);
    console.log(script_id);
    python.stderr.on('data', function(data){
        dataString = data.toString('utf8');
        errors.push(dataString);
        console.log("", dataString);
        win.webContents.send('receiveData', dataString);
    });
});

ipcMain.on('kill', async () => {
if(script_id)
{
    try
    {
        await process.kill(script_id, 'SIGINT');
        script_id = null;
    }
    catch(error)
    {
        console.error(error);
    }
}
win.webContents.send('killComplete');
})

