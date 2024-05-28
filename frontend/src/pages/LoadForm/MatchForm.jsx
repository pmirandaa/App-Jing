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
export default function MatchForm(){
  const [name, setName] = useState(0);
  const [universitySelect, setUniversitySelect] = useState([]);
  const [universityOptions, setUniversityOptions] = useState([]);
  const { event } = useContext(EventContext);

  function handleNameChange(e){
    setName(e.target.value)
  }  

  function handleSubmit(e){
    e.preventDefault();
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
      
  }, []);


  return(
      <Container>
      <div className={styles.mainContainer}>
        <h2 class="h1-responsive font-weight-bold text-center my-5">
            Crear un nuevo Partido 
        </h2>
        <form onSubmit={handleSubmit}>
          <div className={styles.inputContainer}>
            <input placeholder="Nombre del Canal" className={styles.inputBox} type="text" id="username" name="username" onChange={handleNameChange}/>
          </div>
          <br/>
          <div className={styles.inputContainer}>
            <input placeholder="Nombre del Canal" className={styles.inputBox} type="text" id="username" name="username" onChange={handleNameChange}/>
          </div>
          <br/>
          <div className={styles.inputContainer}>
            <input placeholder="Nombre del Canal" className={styles.inputBox} type="text" id="username" name="username" onChange={handleNameChange}/>
          </div>
          <br/>
          <Select
              placeholder="Universidad"
              options = {universityOptions}
              value= {universitySelect}
              
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