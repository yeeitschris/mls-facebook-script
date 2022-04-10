const {app, BrowserWindow} = require("electron");

let win = null;

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