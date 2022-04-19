
const ipcRenderer = require('electron').ipcRenderer;
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