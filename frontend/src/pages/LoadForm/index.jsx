import {
    Button,
    Col,
    Container,
    Modal,
    Row,
    Stack, 
    Dialog
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

export default function LoadForm(){
  const [name, setName] = useState(0);
  const [lastName, setLastName] = useState([]);
  const [email, setEmail] = useState([]);
  const [rut, setRut] = useState([]);
  const [phone, setPhone] = useState([]);
  const [emergencyPhone, setEmergencyPhone] = useState([]);
  const [universitySelect, setUniversitySelect] = useState([]);
  const [universityOptions, setUniversityOptions] = useState([]);
  const { event } = useContext(EventContext);
  const [created, setCreated]= useState(0)

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
      
  }, []);

  function handleNameChange(e){
    setName(e.target.value)
  } 

  function handleLastNameChange(e){
    setLastName(e.target.value)
  }
  
  function handleEmailChange(e){
    setEmail(e.target.value)
  }
  
  function handleRutChange(e){
    setRut(e.target.value)
  }
  function handlePhoneChange(e){
    setPhone(e.target.value)
  }  
  function handleEmergencyPhoneChange(e){
    setEmergencyPhone(e.target.value)
  }

  function handleSelect(e){
    setUniversitySelect(e.value)
  }    

  function handleSubmit(e){
    e.preventDefault();
    const fd = new FormData();
    fd.append('name', name);
    fd.append('lastName', lastName);
    fd.append('email', email);
    fd.append('rut', rut);
    fd.append('phone', phone);
    fd.append('emergencyPhone',emergencyPhone);
    fd.append('university', universitySelect);
    fd.append('event', `${event.id}`);
    axios.post(`${API_URL}/createperson/`, fd, {
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
    })
  }

  function reset(){
    setCreated(0)
    setName(0)
    setLastName(0)
    setEmail([])
    setRut([])
    setPhone([])
    setEmergencyPhone([])
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
            Crear una nueva Persona 
        </h2>
        <form onSubmit={handleSubmit}>
          <div className={styles.inputContainer}>
            <input placeholder="Nombre" className={styles.inputBox} type="text" id="name" name="name" onChange={handleNameChange}/>
          </div>
          <br/>
          <div className={styles.inputContainer}>
            <input placeholder="Apellido" className={styles.inputBox} type="text" id="lastname" name="lastname" onChange={handleLastNameChange}/>
          </div>
          <br/>
          <div className={styles.inputContainer}>
            <input placeholder="Email" className={styles.inputBox} type="text" id="username" name="username" onChange={handleEmailChange}/>
          </div>
          <br/>
          <div className={styles.inputContainer}>
            <input placeholder="Rut" className={styles.inputBox} type="text" id="username" name="username" onChange={handleRutChange}/>
          </div>
          <br/>
          <div className={styles.inputContainer}>
            <input placeholder="Celular" className={styles.inputBox} type="text" id="username" name="username" onChange={handlePhoneChange}/>
          </div>
          <br/>
          <div className={styles.inputContainer}>
            <input placeholder="Contancto de Emergencia" className={styles.inputBox} type="text" id="username" name="username" onChange={handleEmergencyPhoneChange}/>
          </div>
          <br/>
          <Select
              placeholder="Universidad"
              options = {universityOptions}
              onChange={handleSelect}>
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