import {
    Button,
    Col,
    Container,
    Modal,
    Row,
    Stack
  } from "react-bootstrap";
  import { useContext, useState, useEffect } from "react";
  import { EventContext } from "contexts/EventContext";
  import { UserContext } from "contexts/UserContext";
  import { sleeper } from "utils";
  import axios from "axios";
  import { API_URL } from "constants";
  import Form from "react-bootstrap/Form";
  //import Stack from '@mui/material/Stack';
  import Select from "react-select";
  import Cookies from "universal-cookie";

//instantiating Cookies class by creating cookies object
 const cookies = new Cookies();
  
  export default function Dataload() {
    const [file, setFile] = useState(null);
    const [universitySelect, setUniversitySelect] = useState([]);
    const { event } = useContext(EventContext);
    const [universityOptions, setUniversityOptions] = useState([]);
    const [sportOptions, setSportOptions] = useState([]);
    const [sportSelect, setSportSelect] = useState([]);

    useEffect(() => {
      const fetch = axios
        .get(`${API_URL}/universities/?event=${event.id}`) //.get(`${API_URL}/university/filters/?event=${event.id}`)
        .then((response) => {
          const object={}
          const lista = []
          response.data.forEach(element => {
            lista.push({value: element.id ,label:element.name})
          });
          console.log(response.data)
          console.log(lista)
          setUniversityOptions(lista);
        })
        .finally(() => {
          console.log(universityOptions)
          //setIsLoading(false);
        });
      const fetch2 = axios
        .get(`${API_URL}/sports/?event=${event.id}`) //.get(`${API_URL}/university/filters/?event=${event.id}`)
        .then((response) => {
          const object={}
          const lista = []
          response.data.forEach(element => {
            lista.push({value: element.id ,label:element.name})
            
            object[element.name]=element.id
            
          });
          console.log(response.data)
          console.log(lista)
          console.log("objeto", object)
          console.log("objetokeys", Object.keys(object))

          setSportOptions(lista);
        })
        .finally(() => {
          console.log(sportOptions)
          //setIsLoading(false);
        });
    }, []);

    function handleUpload(){
      if (!file){
        console.log("no file selected")
        return
      }
      const fd = new FormData();
      fd.append('file', file);
      fd.append('university', universitySelect )

      axios.post(`${API_URL}/dataload/`, fd, {
        credentials: "same-origin",
        withCredentials:true,
        onUploadProgresss: (progressEvent) => {console.log(progressEvent.progress*100)},
        headers:{
          //'Content-Type': 'multipart/form-data',
          "X-CSRFToken": cookies.get("csrftoken")
        }
      })
    }

    function handleUploadEquipos(){
      if (!file){
        console.log("no file selected")
        return
      }
      const fd = new FormData();
      fd.append('file', file);
      fd.append('university', universitySelect )
      fd.append('tipo', 'equipos')

      axios.post(`${API_URL}/dataload/`, fd, {
        credentials: "same-origin",
        withCredentials:true,
        onUploadProgresss: (progressEvent) => {console.log(progressEvent.progress*100)},
        headers:{
          //'Content-Type': 'multipart/form-data',
          "X-CSRFToken": cookies.get("csrftoken")
        }
      })
    }

    function handleUploadPartidos(){
      if (!file){
        console.log("no file selected")
        return
      }
      const fd = new FormData();
      fd.append('file', file);
      fd.append('university', universitySelect )
      

      axios.post(`${API_URL}/dataload/`, fd, {
        credentials: "same-origin",
        withCredentials:true,
        onUploadProgresss: (progressEvent) => {console.log(progressEvent.progress*100)},
        headers:{
          //'Content-Type': 'multipart/form-data',
          "X-CSRFToken": cookies.get("csrftoken")
        }
      })
    }

    function handleDownloadExcel(){
      console.log(sportOptions)
      axios.post(`${API_URL}/excel/`,{}, {
        credentials: "same-origin",
        withCredentials:true,
        responseType: 'blob',
        onUploadProgresss: (progressEvent) => {console.log(progressEvent.progress*100)},
        headers:{
          'Content-Type': 'application/vnd.openxmlformatsofficedocument.spreadsheetml.sheet',
          "X-CSRFToken": cookies.get("csrftoken")
        }
      })
      .then((blob) =>{
        const url = window.URL. createObjectURL(blob.data);
        const link = document.createElement("a");
        link.href= url;
        link.download = "carga.xlsx";
        document.body.appendChild(link);

        link.click();

        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);

      })


    }

    function handleSportMultiChange(selectedOption){
      setSportSelect(selectedOption)

    }

    function handleSelect(e){
      setUniversitySelect(e.value)
    }

    /*<Select
    isClearable
    placeholder="Deporte"
    name="sport"
    inputId="sport"
    options={ sportOptions} //.map()}
    className="basic-custom-select"
    classNamePrefix="select"
    onChange={handleSelect}> </Select> */

    //recordar que para enviar el excel de carga completa no es necesario seleccionar deportes, pues el backend leera los deportes el mismo

    return(
      <div >
        <h1>Carga masiva de datos</h1>
        <Container>
        <Stack gap={3}>

        <Form.Label htmlFor="university">Carga de Personas</Form.Label>
        <Row >
          <Col >
            <Select style={{'margin-bottom': '10px' }}
            isClearable
            placeholder="Universidad"
            name="university"
            inputId="university"
            options={ universityOptions} //.map()}
            className="basic-custom-select"
            classNamePrefix="select"
            onChange={handleSelect}> 
            </Select>
          </Col>
          <Col>
            <input type="file" onChange={(e) => {setFile(e.target.files[0])}}/>
            <button onClick={handleUpload}>Upload personas</button>
          </Col>
        </Row>

        <Form.Label htmlFor="equipos">Carga de Equipos O carga completa</Form.Label>
        <Row >
          <Col xs={3}>
          <Select
          isClearable
          placeholder="Deportes"
          options = {sportOptions}
          value= {sportSelect}
          onChange = {handleSportMultiChange}
          isMulti = {true}>
          </Select>
           
          </Col>
          <Col xs={3}>
            <Select
            isClearable
            placeholder="Universidad"
            name="universityTeams"
            inputId="universityTeams"
            options={ universityOptions} //.map()}
            className="basic-custom-select"
            classNamePrefix="select"
            onChange={handleSelect}> </Select>
          </Col>
          <Col>
            <input type="file" onChange={(e) => {setFile(e.target.files[0])}}/>
            <button onClick={handleUploadEquipos}>Upload equipos</button>
          </Col>
        </Row>

        <Form.Label htmlFor="partidos">Carga de Partidos</Form.Label>
        <Row>
          <Col>
          <Select
          isClearable
          placeholder="Partidos"
          name="university"
          inputId="university"
          options={ universityOptions} //.map()}
          className="basic-custom-select"
          classNamePrefix="select"
          onChange={handleSelect}> </Select>
          </Col>
          <Col>
            <input type="file" onChange={(e) => {setFile(e.target.files[0])}}/>
            <button onClick={handleUpload}>Upload partidos</button>
          </Col>
        </Row>

        <Form.Label htmlFor="partidos">Carga  Completa</Form.Label>
        <Row>
          <Col>
          <Select
          isClearable
          placeholder="Partidos"
          name="university"
          inputId="university"
          options={ universityOptions} //.map()}
          className="basic-custom-select"
          classNamePrefix="select"
          onChange={handleSelect}> </Select>
          </Col>
          <Col>
            <input type="file" onChange={(e) => {setFile(e.target.files[0])}}/>
            <button onClick={handleUpload}>Upload partidos</button>
          </Col>
        </Row>
        </Stack>

        <div>
          <h1>
            Aca esta su excel
          </h1>
          <Select
          placeholder="Deportes"
          options = {sportOptions}
          value= {sportSelect}
          onChange = {handleSportMultiChange}
          isMulti = {true}

          >

          </Select>
          <button onClick={handleDownloadExcel} >Descargar excel</button>
        </div>


        </Container>
      </div>
    )
  }
