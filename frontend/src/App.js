import styles from "./App.module.css";
import { useState } from "react";
import { Outlet, useLocation } from "react-router-dom";

import { TransitionGroup, CSSTransition } from "react-transition-group";

import NavBar from "components/navbar/NavBar";
import { EventContext } from "contexts/EventContext";

function App() {
  const [event, setEvent] = useState(1);
  const location = useLocation();  
  
  return (
    <EventContext.Provider value={{event, setEvent}}>
      <div className={styles.root}>
        <NavBar />
        <TransitionGroup component={null} exit={false}>
          <CSSTransition key={location.pathname} classNames="fade" timeout={0}>
            <Outlet />
          </CSSTransition>
        </TransitionGroup>
      </div>
    </EventContext.Provider>
  );
}

export default App;
