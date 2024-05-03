
import {
  Button,
  Col,
  Container,
  Modal,
  Row,
  Stack
} from "react-bootstrap";
import { useContext, useState, useEffect } from "react";
import { EventContext } from "contexts/EventContext";
import { UserContext } from "contexts/UserContext";
import { sleeper } from "utils";
import axios from "axios";
import { API_URL } from "constants";
import Form from "react-bootstrap/Form";
import Select from "react-select";
import Cookies from "universal-cookie";

const cookies = new Cookies();
export default function Messages() {
  const { event } = useContext(EventContext);
  const [msg, setMsg] = useState([]);


  useEffect(() => {
    const fetch = axios
      .get(`${API_URL}/messages/`) 
      .then((response) => {
        const object={}
        const lista = []
        response.data.forEach(element => {
          lista.push({value: element.id ,label:element.name})
        });
        console.log(response.data)
        console.log(lista)
        setMsg(lista);
      })
      .finally(() => {
        console.log(msg)
        //setIsLoading(false);
      });

  }, [])

  return (
    <section class="my-2 row">
      <div class="d-flex row w-100 justify-content-center">
        <h2 class="h1-responsive font-weight-bold text-center my-5">
          Mensajes
        </h2>
        {/* {% if person.is_admin or person.is_organizer %} */}
        <a
          class="btn btn-danger btn-circle my-auto ml-5"
          data-toggle="modal"
          data-target=".new_message"
        >
          <i class="fas fa-paper-plane"></i>
        </a>
        {/* {% endif %} */}
      </div>
      <div class="w-100 mx-md-5 mx-4">
        {/* {% if messages %} */}
        <table
          class="table table-bordered table-hover"
          cellspacing="0"
          width="100%"
        >
          <thead>
            <tr>
              <th class="th-sm">Fecha</th>
              <th class="th-sm">Remitente</th>
              <th class="th-sm">Contenido</th>
            </tr>
          </thead>
          <tbody>
            {/* {% for message in messages %} */}
            <tr /* {% if message.is_read %}class="read-message"{% endif %} */>
              <td>[DATE]</td>
              <td>[SENDER]</td>
              <td>
                <p class="font-weight-bold mb-0">[SUBJECT]</p>
                <hr class="mt-0 mb-2" />
                <p class="ml-3 mb-1">[BODY]</p>
              </td>
            </tr>
            {/* {% endfor %} */}
          </tbody>
        </table>
        {/* {% else %} */}
        <h3 class="h3-responsive font-weight-bold text-center my-5">
          Aún no has recibido mensajes en la aplicación.
        </h3>
        {/* {% endif %} */}
      </div>
    </section>
  );
}
