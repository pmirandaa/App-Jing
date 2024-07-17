import {
  Button,
  Col,
  Container,
  Modal,
  Row,
  Stack
} from "react-bootstrap";
import { useContext, useState, useEffect, useRef } from "react";
import { EventContext } from "contexts/EventContext";
import { UserContext } from "contexts/UserContext";
import axios from "axios";
import { API_URL } from "constants";
import Form from "react-bootstrap/Form";
import Select from "react-select";
import Cookies from "universal-cookie";
import { Link } from "react-router-dom";

//instantiating Cookies class by creating cookies object
const cookies = new Cookies();
  
export default function Dataload() {
  const [file, setFile] = useState(null);
  const [universitySelect, setUniversitySelect] = useState([]);
  const [universitySelect2, setUniversitySelect2] = useState([]);
  const { event } = useContext(EventContext);
  const [universityOptions, setUniversityOptions] = useState([]);
  const [sportOptions, setSportOptions] = useState([]);
  const [sportSelect, setSportSelect] = useState([]);
  const [dialogContent, setDialogContent] = useState({detail:"", error:'', row:0, content:''});
  const dialogRef = useRef(null);
  const [show, setShow] = useState(false);

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

  function toggleDialog(){
    if (!dialogRef.current){
      return;
    }
    dialogRef.current.hasAttribute("open")
    ? dialogRef.current.close()
    : dialogRef.current.showModal();
  }

  function handleClose(){
    setShow(false)
  };
  function handleShow(){
    setShow(true)
  };

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
    .then(response =>{
      console.log(response)
      if(response.data.detail=="Error"){
        setDialogContent({...dialogContent, error:response.data.Error, row:response.data.row,  content:response.data.content})
        handleShow()
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
    .then(response =>{
      console.log(response)
      if(response.data.detail=="Error"){
        setDialogContent({...dialogContent,detail:response.data.detail, error:response.data.Error, row:response.data.row,  content:response.data.content})
        handleShow()
      }
      else{
        setDialogContent({...dialogContent,detail:response.data.detail, error:response.data.Error, row:response.data.row,  content:response.data.content})
        handleShow()
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
    fd.append('university', universitySelect)

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

  function handleSelectPersonas(e){
    setUniversitySelect(e.value)
  }

  function handleSelectEquipos(e){
    setUniversitySelect2(e.value)
  }

  return(
    <div >
      <h1>Carga de datos: {event.name}</h1>
      <Container> {
        // Carga Masiva de datos: En esta pagian ud podrá subir un archivo excel con los datos de los participantes. Al final de la página ud 
        // puede descargar un excel prediseñado con los deportes que desea subir a la página
        // Antes de subir el archivo ud debe seleccionar la universidad a la que perteneces los deportistas.
        // Asegurese de no escribir el rut de forma erronea
        // mas informacion (BOTÓN)
        } 
      <Stack gap={2}>
      <h2> Carga individual</h2>
      
      <Row>
      <Col  xs={3}>
      <Link to={`/loadForm`}>
      <button class="btn btn-primary" >Añadir Persona</button>
      </Link>
      </Col>
      <Col  xs={3}>
      <Link to={`/TeamForm`}>
      <button class="btn btn-primary" >Añadir Equipo</button>
      </Link>
      </Col>
      <Col  xs={3}>
      <Link to={`/MatchForm`}>
      <button class="btn btn-primary" >Añadir Partido</button> 
      </Link>
      </Col>
      <Col  xs={3}>
      <Link to={`/ResultForm`}>
      <button class="btn btn-primary" >Añadir Resultado</button> 
      </Link>
      </Col>
      </Row>
      <h2>Carga Multiple</h2>
      <p>Carga Masiva de datos: En esta pagina ud. podrá subir un archivo excel con los datos de los participantes. Al final de la página ud 
         puede descargar un excel prediseñado con los deportes que desea subir a la página
         Antes de subir el archivo ud debe seleccionar la universidad a la que perteneces los deportistas.
         No es necesario que los miembros de un equipo esten registrados; se les registrará autmáticamente.</p>
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
          onChange={handleSelectPersonas}> 
          </Select>
        </Col>
        <Col>
          <input type="file" onChange={(e) => {setFile(e.target.files[0])}}/>
        </Col>
        <Col>
          <button class="btn btn-primary" onClick={handleUpload}>Subir personas</button>
        </Col>
      </Row>

      <Form.Label htmlFor="equipos">Carga de Equipos</Form.Label>
      {/*<p>Cada hoja corresponde a un deporte y cada fila a un miembro del equipo</p>*/}
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
          onChange={handleSelectEquipos}> </Select>
        </Col>
        <Col>
          <input type="file" onChange={(e) => {setFile(e.target.files[0])}}/>
        </Col>
        <Col>
          <button class="btn btn-primary" onClick={handleUploadEquipos}>Subir equipos</button>
        </Col>
      </Row>
       {/* 

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
      
      */}
      </Stack>
      <div>
        <br/>
        <h1>
          Plantilla Excel
        </h1>
        <p>Seleccione TODOS los deportes que quiere ingresar para obtener el excel pre diseñado. Si desea agregar sólo personas, no seleccione nada. 
        Cada hoja corresponde a un deporte y cada fila a un participante. Llene todos los datos de cada participante. Puede editar el archivo en cualquier programa pero el archivo debe subir un archivo Excel.</p>
        <Row>
          <Col xs={6}>
            <Select
            placeholder="Deportes (Selección Múltiple)"
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
        <br />
      </div>
      </Container>
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>{dialogContent.detail}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {dialogContent.error} <br/>
          Fila:{dialogContent.row}  <br/>
          Contenido:{dialogContent.content}<br/>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
          <Button variant="primary" onClick={handleClose}>
            Save Changes
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  )
}
