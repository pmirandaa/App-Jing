import Avatar from "components/image/Avatar";
import { EventContext } from "contexts/EventContext";
import { useContext } from "react";
import Nav from "react-bootstrap/Nav";
import NavDropdown from "react-bootstrap/NavDropdown";

import styles from "./NavBarSection.module.css";

export default function NavBarRightSection() {
  const { event, setEvent } = useContext(EventContext)
  console.log(event)

  return (
    <Nav className={`${styles.section} ${styles.right}`}>
      <NavDropdown className={styles.eventSelector} title={`Evento ${event}`} id="basic-nav-dropdown" align="end">
        <NavDropdown.Item onClick={() => setEvent(1)}>Evento 1</NavDropdown.Item>
        <NavDropdown.Item onClick={() => setEvent(2)}>Evento 2</NavDropdown.Item>
        <NavDropdown.Item onClick={() => setEvent(3)}>Evento 3</NavDropdown.Item>
      </NavDropdown>

      <Avatar />
      <NavDropdown title="Usuario" id="basic-nav-dropdown" align="end">
        <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
        <NavDropdown.Item href="#action/3.2">Another action</NavDropdown.Item>
        <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
        <NavDropdown.Divider />
        <NavDropdown.Item href="#action/3.4">Separated link</NavDropdown.Item>
      </NavDropdown>
    </Nav>
  );
}
