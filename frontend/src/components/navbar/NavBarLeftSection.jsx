import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import { HouseDoorFill, MapFill } from "react-bootstrap-icons";
import { NavLink } from "react-router-dom";

import styles from "./NavBarSection.module.css";

export default function NavBarLeftSection() {
  return (
    <Nav className={`${styles.section} ${styles.left}`}>
      <Navbar.Brand href="/">
        <img
          src="/img/JING%20llamas.png"
          width="90"
          height="30"
          alt="Logo JING"
        />
        JING
      </Navbar.Brand>
      <Nav.Link as={NavLink} to="/">
        <HouseDoorFill size={20} />
      </Nav.Link>
      <Nav.Link as={NavLink} to="/mapa">
        <MapFill size={20} />
      </Nav.Link>
    </Nav>
  );
}
