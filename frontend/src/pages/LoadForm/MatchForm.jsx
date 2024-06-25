import {
    Button,
    Col,
    Container,
    Modal,

} from "react-bootstrap";
import { useContext, useState, useEffect } from "react";
import { EventContext } from "contexts/EventContext";
import { UserContext } from "contexts/UserContext";
import axios from "axios";
import { API_URL } from "constants";
import Select from "react-select";
import Cookies from "universal-cookie";
import styles from "./LoadForm.module.css";
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { format } from 'date-fns';
import { Link } from "react-router-dom";

const cookies = new Cookies();
export default function MatchForm(){
  const [name, setName] = useState(0);
  const [universitySelect, setUniversitySelect] = useState([]);
  const [universityOptions, setUniversityOptions] = useState([]);
  const [selectedDate, setSelectedDate] = useState(null);
  const [sportOptions, setSportOptions] = useState([]);
  const [sportSelect, setSportSelect] = useState([]);
  const [locationOptions, setLocationOptions] = useState([]);
  const [locationSelect, setLocationSelect] = useState([]);
  const [teamsOptions, setTeamsOptions] = useState([]);
  const [teamsSelect, setTeamsSelect] = useState([]);
  const [created, setCreated]= useState(0)
  const [show, setShow] = useState(false);
  const [dialogContent, setDialogContent] = useState({error:'', row:0, content:''});

  const { event } = useContext(EventContext);

  function handleNameChange(e){
    setName(e.target.value)
  }  

  function handleSubmit(e){
    e.preventDefault();
  }

  function handleClose(){
    setShow(false)
  };
  function handleShow(){
    setShow(true)
  };

  function handleDateChange(e){
    setSelectedDate(e.value)
  }
  function handleSportSelect(e){
    setSportSelect(e.value)
  }    
  function handleLocationSelect(e){
    setLocationSelect(e.value)
  }    
  function handleTeamsSelect(selectedOption){
    setTeamsSelect(selectedOption)
  }    
  

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
      const fetch3 = axios
      .get(`${API_URL}/locations/`) 
      .then((response) => {
        const object={}
        const lista = []
        console.log("location response", response)

        console.log("location data", response.data)

        response.data.results.forEach(element => {
          lista.push({value: element.id ,label:element.name})
          object[element.name]=element.id
          
        });
        console.log(response.data)
        console.log("location",lista)
        console.log("objeto", object)
        console.log("objetokeys", Object.keys(object))

        setLocationOptions(lista);
      })
      const fetch4 = axios
      .get(`${API_URL}/teams/?event=${event.id}`) 
      .then((response) => {
        const object={}
        const lista = []
        response.data.results.forEach(element => {
          const nombre = element.sport_name + " - "+ element.university.name
          lista.push({value: element.id ,label:nombre})
          object[element.name]=element.id
          
        });
        console.log(response.data)
        console.log(lista)
        console.log("objeto", object)
        console.log("objetokeys", Object.keys(object))

        setTeamsOptions(lista);
      })        
  }, []);

  function handleSubmit(e){
    e.preventDefault();
    
    const formattedDate = format(selectedDate, 'yyyy-MM-dd')
    console.log(selectedDate.toDateString("yyyy-MM-dd"))
    console.log(formattedDate)
    const fd = new FormData();
    fd.append('name', name);
    
    fd.append('date', formattedDate);
    fd.append('location', locationSelect);
    fd.append('sport',sportSelect);
    fd.append('university', universitySelect);
    fd.append('teams', JSON.stringify(teamsSelect));
    fd.append('event', `${event.id}`);
    
    axios.post(`${API_URL}/creatematch/`, fd, {
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
      if(response.data.detail=="Persona Creada"){
        setCreated(1)
      }
      if(response.data.detail=="Error"){
        setDialogContent({error:response.data.Error})
        handleShow()
      }
    })
  }

  function reset(){
    setCreated(0)
    setName(0)
    setSelectedDate(0)
    setLocationSelect(0)
    setSportSelect(0)
    setTeamsSelect([])
  }

  if(created){
    return (
      <div className={styles.mainContainer}>
        <div className={styles.titleContainer}>
          <div>Equipo Creado</div>
        </div>
    <Button onClick={()=>reset()}>Crear otro equipo</Button> 
    </div>
    )
  }

  return(
      <Container>
      <div className={styles.mainContainer}>
        <h2 class="h1-responsive font-weight-bold text-center my-5">
            Crear un nuevo Partido 
        </h2>
        <Link to={`/dataLoad`}>
        <button className={styles.submitButton}> Volver</button> 
        </Link>
        <form onSubmit={handleSubmit}>
          <div className={styles.inputContainer}>
            <input placeholder="Nombre" className={styles.inputBox} type="text" id="username" name="username" onChange={handleNameChange}/>
          </div>
          <br/>
          <Select
              placeholder="Lugar"
              options = {locationOptions}
              onChange={handleLocationSelect}>
              </Select>
              <br/>
              <Select
              placeholder="Deporte"
              options = {sportOptions}
              onChange={handleSportSelect}>
              </Select>
              <br/>
              <Select
              placeholder="Equipos"
              options = {teamsOptions}
              value= {teamsSelect}
              onChange={handleTeamsSelect}
              isMulti = {true}>
              </Select>
              <br/>
              <DatePicker
              selected={selectedDate}
              onChange={(date) => setSelectedDate(date)}
              dateFormat="YYYY-MM-dd"
              placeholderText="Selecciona una fecha"
            />
          <br/>
          <div className={styles.buttonContainer} >
            <button className={styles.submitButton}   id="submit-btn" type="submit" > Crear</button> 
          </div> 
          </form>
      </div>
      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Error</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {dialogContent.error} <br/>
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
      </Container>
  )
}