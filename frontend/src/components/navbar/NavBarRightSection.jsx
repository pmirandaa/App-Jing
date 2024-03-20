import Avatar from "components/image/Avatar";
import { EventContext } from "contexts/EventContext";
import { useContext } from "react";
import { EnvelopeFill, Mailbox } from "react-bootstrap-icons";
import Nav from "react-bootstrap/Nav";
import NavDropdown from "react-bootstrap/NavDropdown";
import { Link, NavLink } from "react-router-dom";

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

      <Avatar />
      <NavDropdown title="Usuario" id="basic-nav-dropdown" align="end">
        <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
        <NavDropdown.Item href="#action/3.2">Another action</NavDropdown.Item>
        <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
        <NavDropdown.Item as={Link} to="/login"> Login </NavDropdown.Item>
        <NavDropdown.Item as={Link} to="/signin"> Signin </NavDropdown.Item>
        <NavDropdown.Divider />
        <NavDropdown.Item href="#action/3.4">Separated link</NavDropdown.Item>
      </NavDropdown>
    </Nav>
  );
}
