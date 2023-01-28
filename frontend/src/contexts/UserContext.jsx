import React, {useEffect, useState} from "react";
import jwt_decode from "jwt-decode";
import { useNavigate } from "react-router-dom";
import { Buffer } from "buffer";

const AuthContext = React.createContext(); 

export default AuthContext;

export const AuthProvider = ({children}) => {
    const [authTokens, setAuthTokens] = useState(() =>
        localStorage.getItem("authTokens") 
        ? JSON.parse(localStorage.getItem("authTokens")) 
        : null
    );
    const [user, setUser] = useState(() => 
        localStorage.getItem("authTokens")
        ? jwt_decode(localStorage.getItem("authTokens"))
        : null
    );

    const [loading, setLoading] = useState(true);

    const navigate = useNavigate();
    
    const loginUser = async(username, password) => {

        console.log("Attemting to login: " + username + " " + password);
        //aqui se llama a la api para obtener el token de inicio de sesion
        const response = await fetch("http://localhost:8000/api/token/", {
            method: "POST",
            mode: "cors",
            credentials: "include",
            headers: {
                "Content-Type": "application/json",
                "Origin": "http://127.0.0.1:3000",
                "Accept": "application/json",
                "Authorization": "Basic" + Buffer.from(username + ":" + password).toString("base64")
            },
            body: JSON.stringify({
                username,
                password
            })
        });
        const data = await response.json();
        console.log(data);

        if (data.access) {
            setAuthTokens(data.access);
            setUser(jwt_decode(data.access));
            localStorage.setItem("authTokens", JSON.stringify(data.access));
            console.log("Logged in: " + user.username);
            navigate("/");
        } else {
            alert("Nombre de usuario o contraseña incorrectos");
        }
    };

    const registerUser = async(username, password, password2) => {
        const response = await fetch("http://127.0.0.1:8000/api/register/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username,
                password,
                password2
            })
        });

        if (response.status === 201) {
            alert("Usuario registrado correctamente");
            navigate("/login");
        } else {
            alert("Error al registrar usuario");
        }

    };

    const logoutUser = () => {
        setAuthTokens(null);
        setUser(null);
        localStorage.removeItem("authTokens");
        navigate("/");
    };

    useEffect(() => {
        if ( authTokens ) {
            setUser(jwt_decode(authTokens));
        }
        setLoading(false);
    }, [authTokens, loading]);

    const contextData = {
        authTokens,
        setAuthTokens,
        user,
        setUser,
        loginUser,
        registerUser, 
        logoutUser,
    };

    return(
        <AuthContext.Provider value={contextData}>
        {loading ? null : children}
      </AuthContext.Provider>
    );
    
}