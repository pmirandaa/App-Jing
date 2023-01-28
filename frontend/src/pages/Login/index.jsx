import { useContext } from "react";
import AuthContext from "contexts/UserContext";

const LoginPage = () => {
    const { loginUser } = useContext(AuthContext);
    const handleRequest = e => {
        e.preventDefault();
        const username = e.target.username.value;
        const password = e.target.password.value;
        console.log(password);
        username.length > 0 && password.length > 0 && loginUser(username, password);
    };

    return (
        <section>
            <form onSubmit={handleRequest}>
            <h1>Login </h1>
        <hr />
        <label htmlFor="username">Usuario</label>
        <input type="text" id="username" placeholder="Ingrese Usuario" />
        <label htmlFor="password">Contraseña</label>
        <input type="password" id="password" placeholder="Ingrese Contraseña" />
        <button type="submit">Iniciar sesión</button>
            </form>
        </section>
    );
};

export default LoginPage;