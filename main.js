const { systemPreferences } = require("electron");
const {app, BrowserWindow, ipcMain, PythonShell} = require("electron", "python-shell");

let win = null;
let browser_choice, MLS_username, MLS_pw, MLS_choice, FB_email, FB_pw, data_path, price_range, zip_code, num_properties;

const createWindow = () => {
    win = new BrowserWindow({
        width: 800,
        height: 600,
        resizable: true,
        webPreferences: {
            nodeIntegration: true //access to Node funcs/APIs
        }
    })

    win.loadFile('index.html');
};

app.whenReady().then(createWindow);
//Runs back-end code based on info gathered from front-end on render.js
ipcMain.on('sendInfo', (event, browser_choice, MLS_username, MLS_pw, MLS_choice, FB_email, FB_pw, data_path, price_range, zip_code, num_properties) => {
    var python = require('child_process').spawn('python', ['./Main_Runner.py', browser_choice, MLS_username, MLS_pw, MLS_choice, FB_email, FB_pw, data_path, price_range, zip_code, num_properties]);
    python.stdout.on('data', function(data){
        console.log("", data.toString('utf8'));
    });
});