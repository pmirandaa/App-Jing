import styles from "./App.module.css";
import { Outlet, useLocation } from "react-router-dom";

import { TransitionGroup, CSSTransition } from "react-transition-group";

import NavBar from "components/navbar/NavBar";

function App() {
  const location = useLocation();
  return (
    <div className={styles.root}>
      <NavBar />
      <TransitionGroup component={null} exit={false}>
        <CSSTransition key={location.pathname} classNames="fade" timeout={0}>
          <Outlet />
        </CSSTransition>
      </TransitionGroup>
    </div>
  );
}

export default App;
