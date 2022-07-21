import styles from "./App.module.css";
import { useState } from "react";
import {
  Routes,
  Route,
  Navigate,
  useLocation
} from "react-router-dom";

import { TransitionGroup, CSSTransition } from "react-transition-group";

import NavBar from "components/navbar/NavBar";
import { EventContext } from "contexts/EventContext";

import News from 'pages/News';
import Messages from 'pages/Messages';
import Info from 'pages/Info';
import Matches from 'pages/Matches';
import Teams from 'pages/Teams';
import Admin from 'pages/Admin';

function App() {
  const [event, setEvent] = useState(1);
  const location = useLocation();

  return (
    <EventContext.Provider value={{ event, setEvent }}>
      <div className={styles.root}>
        <NavBar />
        <TransitionGroup component={null} exit={false}>
          <CSSTransition key={location.pathname} classNames="fade" timeout={0}>
            <Routes location={location}>
              <Route index element={<News />} />
              <Route path="personas" element={<Info />} />
              <Route path="partidos" element={<Matches />} />
              <Route path="equipos" element={<Teams />} />
              <Route path="mensajes" element={<Messages />} />
              <Route path="administracion" element={<Admin />} />

              <Route path="/hola" element={<Teams />} />
              <Route path="*" element={<Navigate to="/" replace={true} />} />
            </Routes>
          </CSSTransition>
        </TransitionGroup>
      </div>
    </EventContext.Provider>
  );
}

export default App;
