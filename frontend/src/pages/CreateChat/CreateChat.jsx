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
import styles from "./CreateChat.module.css";

const cookies = new Cookies();
export default function CreateChat() {
    const { event } = useContext(EventContext);
    const { user } = useContext(UserContext);
    const [chats, setChats] = useState([]);
    const [created, setCreated]= useState(0)
    const [personOptions, setPersonOptions] = useState([]);
    const [personSelect, setPersonSelect] = useState([]);
    const [name, setName] = useState(0);

    useEffect(() => {
      const fetch = axios
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
      }, [])

    function handleNameChange(e){
      setName(e.target.value)
    }  

    function handlePersonMultiChange(selectedOption){
      setPersonSelect(selectedOption)
    }

    function handleSubmit(e){
      e.preventDefault();
      const fd = new FormData();
      fd.append('name', name);
      fd.append('event', event.id);
      //fd.append('persons', []);
      fd.append('persons', JSON.stringify(personSelect))

      //personSelect.forEach(element => {
        //console.log(element)
       // fd.append("persons", element)
      //});
      console.log(fd.persons)
      const fetch= axios.post(`${API_URL}/createnewchat/`, fd, {
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
        if(response.data.detail=="chat creado"){
          setCreated(1)

        }
      })
    }

    function reset(){
      setCreated(0)
      setPersonSelect([])
      setName(0)

    }

    //Usar el mismo estilo que para el login
    if(created){
      return <Button onClick={()=>reset()}>Crear otro chat</Button> 
    }

    return(
      <Container>
      <div className={styles.mainContainer}>
        <h2 class="h1-responsive font-weight-bold text-center my-5">
            Crear un nuevo canal
        </h2>
        <form onSubmit={handleSubmit}>
          <div className={styles.inputContainer}>
            <input placeholder="Nombre del Canal" className={styles.inputBox} type="text" id="username" name="username" onChange={handleNameChange}/>
          </div>
          <br/>
          <Select
              placeholder="Personas"
              options = {personOptions}
              value= {personSelect}
              onChange = {handlePersonMultiChange}
              isMulti = {true}>
              </Select>
          <div className={styles.buttonContainer} >
            <button className={styles.submitButton}   id="submit-btn" type="submit" > Login</button> 
          </div> 
          </form>
      </div>
      </Container>)
}