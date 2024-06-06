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
import Table from "react-bootstrap/Table";
import { Link } from "react-router-dom";
import styles from "./LoadForm.module.css";

const cookies = new Cookies();
export default function TeamForm(){
  const [name, setName] = useState(0);
  const [universitySelect, setUniversitySelect] = useState([]);
  const [universityOptions, setUniversityOptions] = useState([]);
  const [sportOptions, setSportOptions] = useState([]);
  const [sportSelect, setSportSelect] = useState([]);
  const [personOptions, setPersonOptions] = useState([]);
  const [personSelect, setPersonSelect] = useState([]);
  const { event } = useContext(EventContext);
  const [created, setCreated]= useState(0)
  const [eventSelect, setEventSelect] = useState([])
  const [eventOptions, setEventOptions] = useState([])

  //revisar que los deportes cambien al cambiar el evento y que el evento sea 
  //el actual seleccionado en la pagina por defecto
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
      const fetch3 = axios
      .get(`${API_URL}/persons/`) 
      .then((response) => {
        const object={}
        const lista = []
        response.data.results.forEach(element => {
          lista.push({value: element.id ,label:element.name})
        });
        console.log(lista)
        setPersonOptions(lista);
      })
      .finally(() => {
        console.log(personOptions)
        //setIsLoading(false);
      });
      const fetch4 = axios
      .get(`${API_URL}/events/`)
      .then(sleeper(500))
      .then((response) => {
        console.log(response.data);
        const res =
          response.data?.map((eve) => ({
            value: eve.id,
            label: eve.name,
            data: eve,
          })) ?? [];
        setEventOptions(res.reverse());
      })
  }, []);

  function handleSubmit(e){
    e.preventDefault();
    const fd = new FormData();
    fd.append('university', universitySelect);
    fd.append('sport', sportSelect);
    fd.append('event', eventSelect);
    fd.append('persons', JSON.stringify(personSelect))

    const fetch= axios.post(`${API_URL}/createteam/`, fd, {
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
        if(response.data.detail=="Equipo Creado"){
          setCreated(1)
        }
      })
    }
  
  function handleSportChange(e){
    setSportSelect(e.value)
  }

  function handlePersonMultiChange(selectedOption){
    setPersonSelect(selectedOption)
  }

  function handleUniversityChange(e){
    setUniversitySelect(e.value)
  }

  function handleEventChange(e){
    setEventSelect(e.value)
  }

  function reset(){
    setCreated(0)
    setPersonSelect([])
    setName(0)
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
            Crear un nuevo equipo 
        </h2>
        <form onSubmit={handleSubmit}>
        <Select
            placeholder="Deporte"
            options = {sportOptions}
            
            onChange = {handleSportChange}>
        </Select>
          <br/>
        <Select
            placeholder="Evento"
            options = {eventOptions}
            
            onChange= {handleEventChange}>
        </Select>
          <br/>
        <Select
            placeholder="Universidad"
            options = {universityOptions}
            
            onChange= {handleUniversityChange}>
        </Select>
        <br/>
        <Select
            placeholder="Personas"
            options = {personOptions}
            value= {personSelect}
            onChange = {handlePersonMultiChange}
            isMulti = {true}>
        </Select>
          <br/>
          <div className={styles.buttonContainer} >
            <button className={styles.submitButton}   id="submit-btn" type="submit" > Crear</button> 
          </div> 
          </form>
      </div>
      </Container>
  )
}