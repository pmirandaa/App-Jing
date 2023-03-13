import Nav from "react-bootstrap/Nav";
import { NavLink } from "react-router-dom";
import AuthContext from "contexts/UserContext";

import styles from "./NavBarSection.module.css";
import { useContext } from "react";

export default function NavBarMidSection() {
  const { permissions } = useContext(AuthContext);
  const [isSportCoordinator, isEventCoordinator, isUniversityCoordinator, isTeamCoordinator, admin] =
   permissions ? Object.entries(permissions).map(([key, value]) => value): [];
  
  return (
    <Nav className={`${styles.section} ${styles.mid}`}>
      <Nav.Link as={NavLink} to="/partidos">
        Partidos
      </Nav.Link>
      {/* <Nav.Link as={NavLink} to="/equipos">
        Equipos
      </Nav.Link>
      <Nav.Link as={NavLink} to="/personas">
        Personas
      </Nav.Link> */}
      <Nav.Link as={NavLink} to="/resultados">
        Resultados
      </Nav.Link>
      {(admin || isSportCoordinator || isEventCoordinator || isTeamCoordinator || isUniversityCoordinator)? <Nav.Link as={NavLink} to="/administracion">
        Administración
      </Nav.Link>
      :  <></>}

      
    </Nav>
  );
}
