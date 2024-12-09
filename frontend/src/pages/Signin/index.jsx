import {
  Button,
  Col,
  Container,
  Modal,
  Row,
  Stack
}from "react-bootstrap";
import axios from "axios";
import { API_URL } from "constants";
import { sleeper } from "utils";
import { useState, useEffect, useContext, useRef } from "react";
import { UserContext } from "contexts/UserContext";
import { EventContext } from "contexts/EventContext";
import styles from "./Login.module.css";
import Cookies from "universal-cookie";
import { Link } from "react-router-dom";
import Select from "react-select";
const cookies = new Cookies();

export default function Signin() {

  const [session, setSession] = useState({username:"",password:"", isAuthenticated:false,error:""})
  const [profile, setProfile] = useState({id:0,name:"",last_name:"",email:"",university:0, rut:"" ,error:"", roles:""})
  const [isLoading, setIsLoading] = useState(false);
  const [data, setData] = useState({name:"",last_name:"", rut:"" ,email:"",university:0, phone:"", ephone:""})

  const [universitySelect, setUniversitySelect] = useState([]);
  const [universityOptions, setUniversityOptions] = useState([]);

  const {user, setUser} = useContext(UserContext)
  const {event, setEvent} = useContext(EventContext)
  const profileRef = useRef({id:0,name:"",last_name:"",email:"",university:0, rut:"" ,error:"", roles:[]})
  const [show, setShow] = useState(false);
  const [dialogContent, setDialogContent] = useState({error:'', row:0, content:''});

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
    }, [])

  function handleClose(){
    setShow(false)
  };
  function handleShow(){
    setShow(true)
  };

  function handlePasswordChange(event) {
    setSession({...session,password: event.target.value});
  }

  function handleUserNameChange(event) {
    setSession({...session,username: event.target.value});
  }

  function handleNameChange(event) {
    setData({...data, name: event.target.value});
  }

  function handleLastNameChange(event) {
    setData({...data, last_name: event.target.value});
  }
  function handleRutChange(event) {
    setData({...data, rut: event.target.value});
  }

  function handleEmailChange(event) {
    setData({...data, email: event.target.value});
  }

  function handleUniversityChange(event) {
    setUniversitySelect(event.value)
    setData({...data, university: event.target.value});
  }
  
  function handlePhoneChange(event) {
    setData({...data, phone: event.target.value});
  }
  function handleEPhoneChange(event) {
    setData({...data, ephone: event.target.value});
  }

  async function asyncLoginpost(user, setUser,e) {
    setIsLoading(true);
    e.preventDefault();
    const fetch = axios
      .post(`${API_URL}/login/`,JSON.stringify( 
        {username: session.username, password:session.password}),{
        headers:{
          "X-CSRFToken": cookies.get("csrftoken")
        },
        credentials: "same-origin",
        withCredentials:true,
      })
      .then(sleeper(500))
      .then((response) => response.data)
      .then( (data)=> 
      {
        console.log("respuesta de login",data);
        setProfile({...profile,id:data.user.id, name: data.user.name ,last_name:data.user.last_name,email:data.user.email,university:data.user.university, rut:data.user.rut})
        profileRef.current={...profile,id:data.user.id, name: data.user.name ,last_name:data.user.last_name,email:data.user.email,university:data.user.university, rut:data.user.rut, roles:data.PER}
        setSession({...session,isAuthenticated: true, username: "", password: "", error: ""});
        saveUser(user,setUser)
        setIsLoading(false);
      })
  }

    function Signinpost(user, setUser, e) {
        setIsLoading(true);
        e.preventDefault();
        const fetch = axios
        .post(`${API_URL}/signin/`,JSON.stringify( 
          {username: session.username, password:session.password, name:data.name,last_name:data.last_name, rut:data.rut, email:data.email ,university:data.university, phone:data.phone, ephone:data.ephone}),{
          headers:{
            "X-CSRFToken": cookies.get("csrftoken")
          },
          credentials: "same-origin",
          withCredentials:true,
        })
        .then(sleeper(500))
        .then((response) => response.data)
        .then( (data)=> {
          if(data.detail=="Error"){
            setDialogContent({error:data.Error})
            handleShow()
          }
          else{
          console.log("respuesta de signin",data);
          setProfile({...profile,id:data.user.id, name: data.user.name ,last_name:data.user.last_name,email:data.user.email,university:data.user.university, rut:data.user.rut})
          profileRef.current={...profile,id:data.user.id, name: data.user.name ,last_name:data.user.last_name,email:data.user.email,university:data.user.university, rut:data.user.rut, roles:data.PER}
          setSession({...session,isAuthenticated: true, username: "", password: "", error: ""});
          saveUser(user,setUser)
          setIsLoading(false);
        }
        })
        .finally(() => {
          //setIsLoading(false);
        });
    }

    // Get Session Method https://github.com/BekBrace/django-react-vite-auth/blob/main/frontend/src/App.jsx
  function getSession() {
    //// Make a GET request to the "/api/session/" URL with "same-origin" credentials
    axios.get(`${API_URL}/session/`,{credentials: "same-origin",withCredentials:true,})
    //.then((res) => res.json()) //// Parse the response as JSON
    .then((data) => {
      console.log("get sessiondata",data); // Log the response data to the console
      console.log("get session data.data",data.data.isAuthenticated)
      //// If the response indicates the user is authenticated
      if (data.data.isAuthenticated) {
        setSession({...session,isAuthenticated: true}); // Update the component's state
        profileRef.current={...profile,id:data.data.user.id, name: data.data.user.name ,last_name:data.data.user.last_name,email:data.data.user.email,university:data.data.user.university, rut:data.data.user.rut, roles:data.data.PER}
        saveUser(user,setUser)
        //setIsLoading(false);
      } else {  // If the response indicates the user is not authenticated
        setSession({...session,isAuthenticated: false}); // Update the component's state
        //setIsLoading(false);
      }
    })
  }

  function saveUser(user, setUser){

    const roles = profileRef.current.roles
    const array=[]

    roles.forEach((obj) => {
      if (obj.event == event.id) {
        array.push(obj.role)
        
      }})
    setUser({id:profileRef.current.id, name: profileRef.current.name ,last_name:profileRef.current.last_name,email:profileRef.current.email,university:profileRef.current.university, rut:profileRef.current.rut, roles:profileRef.current.roles, isAuthenticated:true, actual_roles:array})
  }

  useEffect(() =>{
    getSession()
    
  },[]) 

    if(!session.isAuthenticated){
  return(
    <UserContext.Provider value={[user, setUser]}>
      <Container>
      {console.log("profile dentro del provider",profile)}
      {console.log("usuario dentro del provider",user)}
      <div className={styles.mainContainer}>
        <div className={styles.titleContainer}>
          <div>Sign in</div>
        </div>
        <br />
        <form onSubmit={(e)=>{Signinpost(user,setUser, e)}}>
          <div className={styles.inputContainer}>
            <input placeholder="Nombre de Usuario" className={styles.inputBox} type="text" id="username" name="username"  onChange={handleUserNameChange} />
          </div>
          <br />
          <div className={styles.inputContainer}>
            <input  placeholder="Contraseña" className={styles.inputBox} type="password" id="password" name="password"  onChange={handlePasswordChange} />
          </div>
          <br />
          <div className={styles.inputContainer}>
            <input  placeholder="Nombre" className={styles.inputBox} type="text" id="name" name="name" onChange={handleNameChange} />
          </div>
          <br />
          <div className={styles.inputContainer}>
            <input  placeholder="Apellido" className={styles.inputBox} type="text" id="last_name" name="last_name"  onChange={handleLastNameChange} />
          </div>
          <br/>
          <div className={styles.inputContainer}>
            <input  placeholder="Rut" className={styles.inputBox} type="text" id="rut" name="rut" onChange={handleRutChange} />
          </div>
          <br/>
          <div className={styles.inputContainer}>
            <input  placeholder="Email" className={styles.inputBox} type="text" id="email" name="email" onChange={handleEmailChange} />
          </div>
          <br/>
        <Select
            placeholder="Universidad"
            options = {universityOptions}
            onChange= {handleUniversityChange}>
        </Select>
          <br/>
          <div className={styles.inputContainer}>
            <input  placeholder="Teléfono" className={styles.inputBox} type="text" id="phone" name="phone"  onChange={handlePhoneChange} />
          </div>
          <br/>
          <div className={styles.inputContainer}>
            <input  placeholder="Teléfono de Emergencia" className={styles.inputBox} type="text" id="ephone" name="ephone" onChange={handleEPhoneChange} />
          </div>
          <br/>
          <div className={styles.buttonContainer} >
            <button className={styles.submitButton}   id="submit-btn" type="submit" > Registrar</button> 
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
        </Modal.Footer>
      </Modal>
      </Container>
    </UserContext.Provider>)
    }

return(
    <div className={styles.mainContainer}>
    <div className={styles.titleContainer}>
    <h1>Bienvenido {session.username}</h1>
    </div>
    <div>
      <Link to={`*`}>
      <button class="btn btn-primary" >Home</button>
      </Link>
    </div>
    
    {/*<p>{user.name}</p>
    <p>{user.email}</p>
    <p>{user.id}</p>
    <p>{user.last_name}</p>
    <p>{user.rut}</p>
<p>{user.university}</p>*/}
  </div>
  
)}