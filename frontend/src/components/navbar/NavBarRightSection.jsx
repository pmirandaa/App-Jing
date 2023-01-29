
import { EventContext } from "contexts/EventContext";
import  AuthContext  from "contexts/UserContext";
import { useContext } from "react";
import { EnvelopeFill, Mailbox } from "react-bootstrap-icons";
import Nav from "react-bootstrap/Nav";
import NavDropdown from "react-bootstrap/NavDropdown";
import { Link, NavLink } from "react-router-dom";
import NavBarAvatar from "utils/AvatarInfo";

import styles from "./NavBarSection.module.css";

export default function NavBarRightSection() {
  const { event } = useContext(EventContext)

  return (
    <Nav className={`${styles.section} ${styles.right}`}>
      <Nav.Link as={NavLink} to="/">
        <EnvelopeFill size={20}/>
      </Nav.Link>
      <NavDropdown className={styles.eventSelector} title={`${event?.name}`} id="basic-nav-dropdown" align="end">
        <NavDropdown.Item as={Link} to="/eventos">Ver evento</NavDropdown.Item>
        <NavDropdown.Item as={Link} to="/eventos">Cambiar evento</NavDropdown.Item>
      </NavDropdown>

      <NavBarAvatar />
      
    </Nav>
  );
}
