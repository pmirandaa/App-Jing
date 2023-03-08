import AuthContext from "contexts/UserContext";
import { useContext, useState } from "react";
import * as XLSX from "xlsx";
import axios from "axios";
import { APP_URL } from "constants";

//this function assumes that the file is an excel file
//and nothing about the format of the file
function processData(target, name, sheets){
    if (name === 'file'){
        let reader = new FileReader();
        reader.readAsArrayBuffer(target.files[0]);
        reader.onload = (e) => {
            e.preventDefault();
            var data = new Uint8Array(e.target.result);
            var woorkbook = XLSX.read(data, {type: 'array'});
            console.log("woorkbook");
            woorkbook.SheetNames.forEach(function(sheetName){
                var XL_row_object = XLSX.utils.sheet_to_row_object_array(woorkbook.Sheets[sheetName]);
                sheets.push(
                    XL_row_object, 
                    sheetName
                )
            });
            console.log(sheets);
            return sheets;
        }
    }
}

function FileUploader(){
    const {permissions} = useContext(AuthContext);
    const {authTokens} = useContext(AuthContext);
    const [isSportCoordinator, isEventCoordinator, isUniversityCoordinator, isTeamCoordinator, admin] = permissions ? Object.entries(permissions).map(([key, value]) => value) : null;
    const [selectedfile, setFile] = useState(false);

    //this function assumes that the file is an excel file
    function HandleInputChange( event ){
       event.preventDefault();
       const target = event.target;
       const value = target.type === 'checkbox' ? target.checked : target.value;
       const name = target.name;
       console.log(name);
       console.log(target.files)
       let sheets = [];

        sheets = processData(target, name, sheets);
        setFile(sheets);
        console.log(sheets);
       
    }

    //options return 200 but the data is not being sent
    async function sendData( event ){
        event.preventDefault();
        let data = new FormData();
        data.append('data', selectedfile);
        console.log("data before sending: " + data);
        const response = await axios.post(`http://127.0.0.1:8000/admin/upload-data`, data, {
            method: 'POST',
            mode: 'cors',
            headers: {
                "Origin": "http://127.0.0.1:3000",
                "Content-Type": 'multipart/form-data',
                "Accept": "application/json",
                "Authorization": `Bearer ${authTokens?.access}`,

            },
        },)
    };

    return admin ? 
        <div>
            <form name="uploader" onSubmit={sendData}>
            <input type="file" name="file" id="file" onChange={HandleInputChange} placeholder="Carga de datos"/>
            <button type="submit" >Cargar Archivo</button>
            </form>
        </div> :
        <></>

}

export default FileUploader;