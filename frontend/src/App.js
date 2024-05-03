import styles from "./App.module.css";
import { useState, useEffect, componentDidMount } from "react";
import {
  Routes,
  Route,
  Navigate,
  useLocation
} from "react-router-dom";

import { TransitionGroup, CSSTransition } from "react-transition-group";
import { Provider as AlertProvider } from 'react-alert'

import { API_URL } from "constants";
import NavBar from "components/navbar/NavBar";
import { EventContext } from "contexts/EventContext";
import { UserContext } from "contexts/UserContext";

import News from 'pages/News';
import Messages from 'pages/Messages';
import Matches from 'pages/Matches';
import Teams from 'pages/Teams';
import Admin from 'pages/Admin';
import Persons from "pages/Persons";
import Results from "pages/Results";
import Events from "pages/Events";
import axios from "axios";
import Maps from "pages/Maps";
import Login from 'pages/Login';
import Signin from 'pages/Signin';
import DataLoad from 'pages/DataLoad';
import AdminUsers from 'pages/AdminUsers'
import Alert from "components/alert/Alert";

function App() {

  const [event, _setEvent] = useState({});
  const [user, _setUser] = useState({id:0,name:"",last_name:"",email:"",university:0, rut:"12" ,error:"", roles:[], actual_roles:[]})
  const [isLoading, setIsLoading] = useState(false);
  const location = useLocation();
  
  useEffect(() =>{
    const fetchInit = async () =>{
      setIsLoading(true);

      const response = await axios.get(`${API_URL}/events/?current=True`);
      const evento= response.data
      console.log(response.data[0].id)
      getSession()
      _setEvent({id:evento[0].id, name:evento[0].name})
      setIsLoading(false);
    };
    fetchInit();
    
    console.log("termina fetch")
  },[]);

  function setEvent(event) {
    console.log("SETEVENT")
    if (Number.isInteger(event)) { // si agrego un ! a la condicion, se carga el valor inicial del evento, pero despues no se puede cambiar porque no se llega al elif de objecto
      axios
        .get(`${API_URL}/events?/${event}/`) //si cambio la url no pasanada pues los cambios son realizados con el siguiente elif
        .then((response) => {
          const res = response.data;
          _setEvent({ id: res.id, name: res.name });
        })
    }
    else if (typeof event === 'object' && event.hasOwnProperty('id') && event.hasOwnProperty('name')) {
      _setEvent(event);
    }
    else if (event == {}) {
      axios
        .get(`${API_URL}/events/?current=True`)
        .then((response) => {
          console.log(response)
          const res = response.data;
          _setEvent({ id: res.id, name: res.name });
    })}
    else { _setEvent(null); }
  }

  //  Esta funcionalidad debe cambiarse a un paquete aparte con custom hooks
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
        
        //profileRef.current={...profile,id:data.data.user.id, name: data.data.user.name ,last_name:data.data.user.last_name,email:data.data.user.email,university:data.data.user.university, rut:data.data.user.rut, roles:data.data.PER}
        setUser({...user, id:data.data.user.id, name: data.data.user.name ,last_name:data.data.user.last_name,email:data.data.user.email,university:data.data.user.university, rut:data.data.user.rut, roles:data.data.PER, isAuthenticated:true})
        //functionGetRole()
      } else {  // If the response indicates the user is not authenticated
      }
    })}

   function functionGetRole() {
    const roles = user.roles
    const array=[]

    roles.forEach((obj) => {
      if (obj.event == event.id) {
        array.push(obj.role)
        
      }
      })
    setUser({...user, actual_roles:array})

   }


  function setUser(user){
    _setUser(user)
  }

  if (isLoading){
    return <div>Loading...</div>
  }

  return (
    <EventContext.Provider value={{ event, setEvent }}>
      <UserContext.Provider value={{ user, setUser }}>
      <AlertProvider template={Alert} timeout={10000} position="bottom center">
        <div className={styles.root}>
          <NavBar />
          <TransitionGroup component={null} exit={false}>
            <CSSTransition key={location.pathname} classNames="fade" timeout={0}>
              <Routes location={location}>
                <Route index element={<News />} />
                <Route path="personas" element={<Persons />} />
                <Route path="partidos" element={<Matches />} />
                <Route path="equipos" element={<Teams />} />
                <Route path="mensajes" element={<Messages />} />
                <Route path="administracion" element={<Admin />} />
                <Route path="resultados" element={<Results />} />
                <Route path="eventos" element={<Events />} />
                <Route path="mapa" element={<Maps />} />
                <Route path="login" element={<Login />} />
                <Route path="signin" element={<Signin />} />
                <Route path="adminUsers" element={<AdminUsers />} />
                <Route path="dataLoad" element={<DataLoad />} />
                <Route path="/hola" element={<Teams />} />
                <Route path="*" element={<Navigate to="/" replace={true} />} />
              </Routes>
            </CSSTransition>
          </TransitionGroup>
        </div>
      </AlertProvider>
      </UserContext.Provider>
    </EventContext.Provider>
  );
}

export default App;
