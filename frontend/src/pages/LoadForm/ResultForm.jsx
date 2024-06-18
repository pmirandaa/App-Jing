import {
    Button,
    Container,
    Modal,
} from "react-bootstrap";
import { useContext, useState, useEffect, useRef } from "react";
import { EventContext } from "contexts/EventContext";
import { UserContext } from "contexts/UserContext";
import axios from "axios";
import { API_URL } from "constants";
import Select from "react-select";
import Cookies from "universal-cookie";
import styles from "./LoadForm.module.css";
import 'react-datepicker/dist/react-datepicker.css';

const cookies = new Cookies();
export default function MatchForm(){
  const [name, setName] = useState(0);
  const [sportOptions, setSportOptions] = useState([]);
  const [sportSelect, setSportSelect] = useState([]);
  const sportRef = useRef()

  const [matchOptions, setMatchOptions] = useState([]);
  const [matchSelect, setMatchSelect] = useState([]);
  
  const [teamsOptions, setTeamsOptions] = useState([]);
  const [teamsSelect, setTeamsSelect] = useState([]);
  const [created, setCreated]= useState(0)
  const [show, setShow] = useState(false);
  const [dialogContent, setDialogContent] = useState({error:'', row:0, content:''});
  const [isPlayedChecked, setIsPlayedChecked] = useState(false);
  const [isClosedChecked, setIsClosedChecked] = useState(false);
  const [values, setValues] = useState({});


  const { event } = useContext(EventContext);

  useEffect(() => {
    
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
           
  }, []);

  const handlePlayedCheckboxChange = () => {
    setIsPlayedChecked(!isPlayedChecked);
  };
  const handleClosedCheckboxChange = () => {
    setIsClosedChecked(!isClosedChecked);
  };

  function handleClose(){
    setShow(false)
  };
  function handleShow(){
    setShow(true)
  };

  function handleSportSelect(e){
    setSportSelect(e.value)
    getMatches(e.value)
  }    
  function handleMatchSelect(e){
    setMatchSelect(e.value)
    console.log("match", e)
    const lista = []

    e.teams.forEach(team =>{
        lista.push({value: team.team_id ,label:team.team_university_short_name})
    })
    setTeamsOptions(lista)
  }    
  function handleTeamsSelect(selectedOption){
    setTeamsSelect(selectedOption)
  }    

  const handleChange = (index, element) => {
    const newValues = { ...values, [index]: element.target.value };
    console.log(newValues)
    setValues(newValues);
  };
  

  function getMatches(id){
    const fetch = axios
      .get(`${API_URL}/matches/?sport=${id}`) 
      .then((response) => {
        const object={}
        const lista = []
        response.data.results.forEach(element => {
          lista.push({value: element.id ,label:element.name, teams:element.teams})
        });
        console.log(response.data)
        console.log(lista)
        setMatchOptions(lista);
      })
      .finally(() => {
        console.log(matchOptions)
        //setIsLoading(false);
      });
  }

  function handleSubmit(e){
    e.preventDefault();
    console.log("equipos ganadores", teamsSelect)
    const lista = []
    teamsSelect.forEach((team)=>{
        lista.push(team.value)
    })
    console.log("id ganadores", lista)

    const fd = new FormData();
    fd.append("match", matchSelect);
    fd.append('teamScore', JSON.stringify(values));
    fd.append("winners", JSON.stringify(lista))
    fd.append("played", isPlayedChecked)
    fd.append("closed", isClosedChecked)
    fd.append('event', `${event.id}`);
    
    axios.post(`${API_URL}/createresult/`, fd, {
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
      if(response.data.detail=="Resultado Creado"){
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
    setMatchSelect(0)
    setSportSelect(0)
    setTeamsSelect([])
  }

  if(created){
    return (
      <div className={styles.mainContainer}>
        <div className={styles.titleContainer}>
          <div>Resultado Creado</div>
        </div>
    <Button onClick={()=>reset()}>Crear otro Resultado</Button> 
    </div>
    )
  }

  return(
      <Container>
      <div className={styles.mainContainer}>
        <h2 class="h1-responsive font-weight-bold text-center my-5">
            Añadir un resultado 
        </h2>
        <form onSubmit={handleSubmit}>
            <Select
            placeholder="Deporte"
            options = {sportOptions}
            onChange={handleSportSelect}>
            </Select>
            <br/>
            <Select
              placeholder="Partido"
              options = {matchOptions}
              onChange={handleMatchSelect}>
              </Select>
              <br/>
              <Select
              placeholder="Equipo Ganador"
              options = {teamsOptions}
              value= {teamsSelect}
              onChange={handleTeamsSelect}
              isMulti = {true}>
              </Select>
              {teamsOptions.map((element, index) => (
                <div key={element.value}>
                <div>{element.label}</div>
                <input id="numberInput"
                type="number"
                value={values[element.value] || ''}
                onChange={(event) => handleChange(element.value, event)}
                min="0" ></input>
                </div>
              ))}
            <br/>
            <label>
                <input
                type="checkbox"
                checked={isPlayedChecked}
                onChange={handlePlayedCheckboxChange}/>
                Jugado
            </label>
            <label>
                <input
                type="checkbox"
                checked={isClosedChecked}
                onChange={handleClosedCheckboxChange}/>
                Cerrado
            </label>
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
