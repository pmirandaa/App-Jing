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
        .get(`${API_URL}/universities/?event=${event.id}`) 
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
        .get(`${API_URL}/sports/?event=${event.id}`) 
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
      fd.append('event',event.id)

      axios.post(`${API_URL}/persondataload/`, fd, {
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
      console.log(event["id"])
      console.log(universitySelect)
      const a =  event["id"]
      const fd = new FormData();
      fd.append('file', file);
      fd.append('university', universitySelect)
      fd.append('type', 'teams')
      fd.append('event',event.id) // comntemplar el cambio a id en lugar de name
      fd.append('end','end')

      axios.post(`${API_URL}/dataload/`, fd, {
        credentials: "same-origin",
        withCredentials:true,
        onUploadProgresss: (progressEvent) => {console.log(progressEvent.progress*100)},
        headers:{
          'Content-Type': 'multipart/form-data',
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
      console.log(sportSelect)
      //arreglar el formato de sports
      const fd = new FormData();
      sportSelect.forEach(element => {
        console.log(element)
        fd.append(element["label"], element["value"])
        //Object.keys(sportSelect)

        
      });
      //fd.append('sports', sportSelect )
      console.log(fd)
      axios.post(`${API_URL}/excel/`,fd, {
        credentials: "same-origin",
        withCredentials:true,
        responseType: 'blob',
        onUploadProgresss: (progressEvent) => {console.log(progressEvent.progress*100)},
        headers:{
          //'Content-Type': 'application/vnd.openxmlformatsofficedocument.spreadsheetml.sheet',
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

    return(
      <div >
        <h1>Carga masiva de datos</h1>
        <Container> {
         // Carga Masiva de datos: En esta pagian ud podrá subir un archivo excel con los datos de los participantes. Al final de la página ud 
         // puede descargar un excel prediseñado con los deportes que desea subir a la página
         // Antes de subir el archivo ud debe seleccionar la universidad a la que perteneces los deportistas.
         // Asegurese de no escribir el rut de forma erronea
         // mas informacion (BOTÓN)
         } 
        <Stack gap={3}>

        <Form.Label htmlFor="university">Carga de Personas</Form.Label>
        <Row >
          <Col xs={6}>
            <Select
            isClearable
            placeholder="Universidad"
            name="university"
            inputId="university"
            options={ universityOptions}
            className="basic-custom-select"
            classNamePrefix="select"
            onChange={handleSelect}> 
            </Select>
          </Col>
          <Col>
            <input type="file" onChange={(e) => {setFile(e.target.files[0])}}/>
          </Col>
          <Col>
            <button class="btn btn-primary" onClick={handleUpload}>Upload personas</button>
          </Col>
        </Row>

        <Form.Label htmlFor="equipos">Carga de Equipos O carga completa</Form.Label>
        <Row >
          <Col xs={6}>
            <Select
            isClearable
            placeholder="Universidad"
            name="universityTeams"
            inputId="universityTeams"
            options={ universityOptions}
            className="basic-custom-select"
            classNamePrefix="select"
            onChange={handleSelect}> </Select>
          </Col>
          <Col>
            <input type="file" onChange={(e) => {setFile(e.target.files[0])}}/>
          </Col>
          <Col>
            <button class="btn btn-primary" onClick={handleUploadEquipos}>Upload equipos</button>
          </Col>
        </Row>

        <Form.Label htmlFor="partidos">Carga de Partidos</Form.Label>
        <Row>
          <Col xs={6}>
          <Select
          isClearable
          placeholder="Partidos"
          name="university"
          inputId="university"
          options={universityOptions}
          className="basic-custom-select"
          classNamePrefix="select"
          onChange={handleSelect}> </Select>
          </Col>
          <Col>
            <input type="file" onChange={(e) => {setFile(e.target.files[0])}}/>
            </Col>
            <Col>
            <button class="btn btn-primary" onClick={handleUpload}>Upload partidos</button>
          </Col>
        </Row>

        </Stack>

        <div>
          <h1>
            Acá esta su excel
          </h1>
          <p>Seleccione los deportes que quiere ingresar para obtener el excel pre diseñado</p>
          <Row>
            <Col xs={6}>
              <Select
              placeholder="Deportes"
              options = {sportOptions}
              value= {sportSelect}
              onChange = {handleSportMultiChange}
              isMulti = {true}>
              </Select>
            </Col>

          <Col xs={6}>
            <button class="btn btn-primary" onClick={handleDownloadExcel} >Descargar excel</button>
          </Col>
          </Row>
        </div>


        </Container>
      </div>
    )
  }
