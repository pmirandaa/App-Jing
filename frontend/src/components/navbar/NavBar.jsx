import { Link, NavLink } from "react-router-dom";

export default function NavBar() {
    return (
        <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
            <Link to="/" className="navbar-brand ml-10">
                <img src="" width="90" height="30" alt="Logo JING"/>
                <h5 style={{display: "inline-block", fontWeight: "bold"}}>JING</h5>
            </Link>
            <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent-555"
                aria-controls="navbarSupportedContent-555" aria-expanded="false" aria-label="Toggle navigation">
                <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse justify-content-between" id="navbarSupportedContent-555">
                <ul className="navbar-nav w-100 nav-fill">
                <NavLink to="/" className="nav-item">
                    <span className="nav-link">Noticias</span>
                </NavLink>
                <NavLink to="/personas" className="nav-item">
                    <span className="nav-link">Información general</span>
                </NavLink>
                {/* {% if person %} */}
                <NavLink to="/partidos" className="nav-item">
                    <span className="nav-link">Partidos</span>
                </NavLink>
                <NavLink to="/equipos" className="nav-item">
                    <span className="nav-link">Equipos</span>
                </NavLink>
                <NavLink to="/mensajes" className="nav-item">
                    <span className="nav-link">Mensajes (X)</span>
                </NavLink>
                {/* {% endif %} */}
                {/* {% if person.is_admin or person.is_organizer %} */}
                <NavLink to="/administracion" className="nav-item">
                    <span className="nav-link">Admin</span>
                </NavLink>
                {/* {% endif %} */}
                </ul>
                <ul className=" navbar-nav nav-flex-icons nav-fill">
                {/* {% if user.is_authenticated %} */}
                <li className="nav-item dropdown">
                  <a className="nav-link dropdown-toggle active" id="navbarDropdownMenuLink-4" data-toggle="dropdown"
                    aria-haspopup="true" aria-expanded="false">
                    <i className="fas fa-user"></i> [NOMBRE]
                    </a>
                    <div className="dropdown-menu dropdown-menu-right dropdown-info" aria-labelledby="navbarDropdownMenuLink-4">
                    {/* {% if not person or person.is_organizer or person.is_admin %} */}
                    <a className="dropdown-item" href="#" data-toggle="modal" data-target="#validationModal">Validar inscripción</a>
                    {/* {% endif %} */}
                    <a className="dropdown-item" href="{% url 'person:logout' %}">Cerrar Sesión</a>
                    </div>
                </li>
                {/* {% else %} */}
                <li className="nav-item">
                    <a className="btn btn-outline-white my-0" style={{width: "max-content"}} href="" data-toggle="modal"
                    data-target="#loginModal">Iniciar Sesión</a>
                </li>
                {/* {% endif %} */}
                </ul>
            </div>
        </nav>
      );
  }