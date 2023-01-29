import AuthContext from "contexts/UserContext";
import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import Container from "react-bootstrap/Container";
import { Link, NavLink } from "react-router-dom";
import { Nav } from "react-bootstrap";
import Navbar from "react-bootstrap/Navbar";
import styles from "components/navbar/NavBarSection.module.css";


function Option(value){
  const { user } = useContext(AuthContext);
  const { permissions } = useContext(AuthContext);
  const [isSportCoordinator, isEventCoordinator, isUniversityCoordinator, isTeamCoordinator, admin] = Object.entries(permissions);
  
  if (value.value === "Usuarios"){
    return (admin[1] || isEventCoordinator[1]) ? 
    <Nav.Link as={NavLink} to="/personas"> {value.value} </Nav.Link> :
    <></>
  }else if(value.value === "Equipos"){
    return (admin[1] || isTeamCoordinator[1]) ? 
    <Nav.Link as={NavLink} to="/equipos"> {value.value} </Nav.Link> :
    <></>}

  else if(value.value === "Deportes"){
    return (admin[1] || isSportCoordinator[1]) ?
    <Nav.Link as={NavLink} to="/personas"> {value.value} </Nav.Link> :
    <></>
  }
  else if(value.value === "Universidades"){
    return (admin[1] || isUniversityCoordinator[1]) ?
    <Nav.Link as={NavLink} to="/personas"> {value.value} </Nav.Link> :
    <></>
  }
  else if(value.value === "Organizaciones"){
    return (admin[1] || isUniversityCoordinator[1]) ?
    <Nav.Link as={NavLink} to="/personas"> {value.value} </Nav.Link> :
    <></>
  }
  else{
    return <></>
  }

};

function NavBarAdmin(){

    const navigate = useNavigate();

    return (
        <Navbar bg="light" expand="lg">
          <Container fluid>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Option value="Usuarios"/>
            <Option value="Equipos"/>
            <Option value="Deportes"/>
            <Option value="Universidades"/>
            <Option value="Organizaciones"/>
            
          </Container>
        </Navbar>
      );
}

export default NavBarAdmin;