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
import Alert from "components/alert/Alert";

function App() {

  const [event, _setEvent] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const location = useLocation();
  
  useEffect(() =>{
    const fetchInit = async () =>{
      setIsLoading(true);
      const response = await axios.get(`${API_URL}/events/?current=True`);
      const evento= response.data
      console.log(response.data[0].id)
      _setEvent({id:evento[0].id, name:evento[0].name})
      setIsLoading(false);
    };
    fetchInit();
    
    console.log("termina fetch")
  },[]);

  function setEvent(event) {
    console.log("SETEVENT")
    if (Number.isInteger(event)) { // si agrego un ! a la condicion, se carga el valor inicial del evennto, pero despues no se puede cambiar porque no se llega al elif de objecto
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

  if (isLoading){
    return <div>Loading...</div>
  }

  return (
    <EventContext.Provider value={{ event, setEvent }}>
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

                <Route path="/hola" element={<Teams />} />
                <Route path="*" element={<Navigate to="/" replace={true} />} />
              </Routes>
            </CSSTransition>
          </TransitionGroup>
        </div>
      </AlertProvider>
    </EventContext.Provider>
  );
}

export default App;
