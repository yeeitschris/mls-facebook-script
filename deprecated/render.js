const { app } = require('electron');
const electron = require('electron')
const path = require('path')
const remote = electron.remote
const endBtn = document.getElementById('stopButton')
const ipcRenderer = require('electron').ipcRenderer;

let script_id = 0;
const sendInfo = () => {
    //send information to Main_Runner script to run back-end.
    ipcRenderer.send('sendInfo', document.querySelector('.browser_choice').value,
     document.querySelector('.MLS_username').value, 
    document.querySelector('.MLS_password').value, 
    document.querySelector('.MLS_choice').value, 
    document.querySelector('.FB_email').value,
     document.querySelector('.FB_password').value,
     document.querySelector('.data_path').value,
     document.querySelector('.price_range').value,
     document.querySelector('.zip_code').value,
     document.querySelector('.num_properties').value)
}

ipcRenderer.on('receiveData', (event, data) => {
    const errorTag = document.querySelector("#error");
    errorTag.textContent = data;
});

ipcRenderer.on('receivePID', (event, data) => {
    script_id = data;
});

ipcRenderer.on('killComplete', (event) => {
    document.querySelector("#stopButton").removeAttribute("disabled");
});
/*Gives stop button functionality by killing the current running instance of Python script.*/
const end = () => {
    document.querySelector("#stopButton").setAttribute("disabled", true);
    ipcRenderer.send('kill');
    const errorTag = document.querySelector("#error");
    errorTag.textContent = "Process stopped!";
}




