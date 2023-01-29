import AuthContext from "contexts/UserContext";
import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import NavDropdown from "react-bootstrap/NavDropdown";
import { Link, NavLink } from "react-router-dom";
import Avatar from "components/image/Avatar";
import { Nav } from "react-bootstrap";
import styles from "components/navbar/NavBarSection.module.css";

function NavBarAvatar(){
    let { user } = useContext(AuthContext);
    const { logoutUser } = useContext(AuthContext);
    const { loginUser } = useContext(AuthContext);

    const navigate = useNavigate();

    const logoutHandleRequest = e => {
      e.preventDefault();
      logoutUser();
    }

    const loginHandleRequest = e => {
        e.preventDefault();
        navigate('/login');
    }


    //debería ponerse un botón más estético aquí
    return !user ? <Nav className={`${styles.section} ${styles.mid}`}>
                    <Nav.Link as = {NavLink} to="/login">
                        Iniciar Sesión
                    </Nav.Link> </Nav>:
                    <><Avatar /><NavDropdown title="Usuario" id="basic-nav-dropdown" align="end">
            <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
            <NavDropdown.Item href="#action/3.2">Another action</NavDropdown.Item>
            <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
            <NavDropdown.Divider />
            <NavDropdown.Item onClick = {logoutHandleRequest}>Cerrar sesión</NavDropdown.Item>
        </NavDropdown></>
                   
}



export default NavBarAvatar;