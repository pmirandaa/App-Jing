import Nav from "react-bootstrap/Nav";
import { NavLink } from "react-router-dom";

import styles from "./NavBarSection.module.css";

export default function NavBarMidSection() {
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
    </Nav>
  );
}
