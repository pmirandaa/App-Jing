import AuthContext from "contexts/UserContext";
import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import NavDropdown from "react-bootstrap/NavDropdown";
import Avatar from "components/image/Avatar";

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


    
    return !user ? <form onSubmit={ loginHandleRequest }>
                    <button type="submit">Iniciar sesión</button>
                    </form> :
                    <><Avatar /><NavDropdown title="Usuario" id="basic-nav-dropdown" align="end">
            <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
            <NavDropdown.Item href="#action/3.2">Another action</NavDropdown.Item>
            <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
            <NavDropdown.Divider />
            <NavDropdown.Item href="#action/3.4">
                <form onSubmit={logoutHandleRequest}>
                    <button type="submit">Cerrar sesión</button>
                </form>
            </NavDropdown.Item>
        </NavDropdown></>
                   
}



export default NavBarAvatar;