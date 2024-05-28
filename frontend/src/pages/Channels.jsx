
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
  import Cookies from "universal-cookie";
  import Table from "react-bootstrap/Table";
  import { Link } from "react-router-dom";
  
  const cookies = new Cookies();
  export default function Channels() {
    const { event } = useContext(EventContext);
    const { user } = useContext(UserContext);
    const [chats, setChats] = useState([]);
    const [id, setId]= useState(0)
  
  
    useEffect(() => {
      const fetch = axios
        .get(`${API_URL}/getpersonschats/`, {credentials: "same-origin",
        withCredentials:true, headers:{
          //'Content-Type': 'multipart/form-data',
          "X-CSRFToken": cookies.get("csrftoken") 
        }}).then((response) => {
          console.log(response)
          const object={}
          const lista = []
          response.data.detail.forEach(element => {
            //setMsg(msg => [...msg, element]);
            lista.push(element)
          });
          setChats(lista);
          setId(1)
        })
        .finally(() => {
          //setIsLoading(false);
        });
  
    }, [])  

    return (
      <section class="my-2 row">
        <div class="d-flex row w-100 justify-content-center">
          <h2 class="h1-responsive font-weight-bold text-center my-5">
            Canales
          </h2>
          
          <div style={{width:100}}>
          <Link to={`/createchat`}>
          <button   id="submit-btn" type="submit" > Nuevo canal</button>
          </Link>
          </div>
          
          {console.log(chats)}
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
          <Table striped variant="light" className="mt-4">
            <thead>
              <tr>
                <th class="th-sm">Nombre</th>
                <th class="th-sm">fecha</th>
                <th class="th-sm">mensajes</th>
              </tr>
            </thead>
            <tbody>
            {chats.map((e) => (
              <tr>
                <td><Link to={`/mensajes/${e.id}`} > {e.name}</Link></td>
                <td>[SENDER]</td>
                <td>
                  <p class="font-weight-bold mb-0">[]</p>
                  <hr class="mt-0 mb-2" />
                  <p class="ml-3 mb-1">[BODY]</p>
                </td>
              </tr>
        ))}
            </tbody>
          </Table>
        </div>
      </section>
    );
  }
  