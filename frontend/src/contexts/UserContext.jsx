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

    const [permissions, setPermissions] = useState(() =>
        localStorage.getItem("authTokens")
        ? JSON.parse(localStorage.getItem("permissions"))
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

        if (data.access) {
            setAuthTokens(data.access);
            setUser(jwt_decode(data.access));
            localStorage.setItem("authTokens", JSON.stringify(data.access));
            const permissions_response = await fetch("http://localhost:8000/api/token/permissions/", {
                method: "GET",
                mode: "cors",
                credentials: "include",
                headers: {
                    Authorization: `Bearer ${authTokens?.access}`},

            });
            if (permissions_response.status === 200) {
                const permissions_data = await permissions_response.json();
                setPermissions(permissions_data.permissions);
                console.log(permissions_data.permissions)
                localStorage.setItem("permissions", JSON.stringify(permissions_data.permissions));
            }
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
        localStorage.removeItem("permissions");
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
        permissions,
        setPermissions,
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