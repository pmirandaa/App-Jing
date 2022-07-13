import { Link, NavLink } from "react-router-dom";

import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import NavDropdown from "react-bootstrap/NavDropdown";
import { HouseDoorFill, MapFill } from "react-bootstrap-icons";
import NavBarLeftSection from "./NavBarLeftSection";
import NavBarMidSection from "./NavBarMidSection";
import NavBarRightSection from "./NavBarRightSection";

export default function NavBar() {
  return (
    <Navbar bg="light" expand="lg">
      <Container fluid>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <NavBarLeftSection/>
        <NavBarMidSection/>
        <NavBarRightSection/>
      </Container>
    </Navbar>
  );
}
