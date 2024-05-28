
import {
  Button,
  Col,
  Container,
  Modal,
  Row,
  Stack
} from "react-bootstrap";
import { useContext, useState, useEffect, useRef } from "react";
import { EventContext } from "contexts/EventContext";
import { UserContext } from "contexts/UserContext";
import { sleeper } from "utils";
import axios from "axios";
import { API_URL } from "constants";
import Form from "react-bootstrap/Form";
import Select from "react-select";
import Cookies from "universal-cookie";
import { useLocation, useParams, useSearchParams } from 'react-router-dom';
import styles from "./Messages.module.scss";
import Chat from "./Chat";

const cookies = new Cookies();
export default function Messages() {
  const [searchParams, setSearchParams] = useSearchParams()
  const location=useLocation()
  const chatid= location.pathname
  const { event } = useContext(EventContext);
  const { user } = useContext(UserContext);
  const [msg, setMsg] = useState([]);
  const [chats, setChats] = useState([]);
  const a= useParams()
  const chatRef= useRef(null)

  useEffect(() => {
    console.log(chatid)
    console.log(a)
    
    const fetch = axios
      .get(`${API_URL}/messages/?chat=${a.chatid}`,{credentials: "same-origin",
      withCredentials:true, headers:{
        //'Content-Type': 'multipart/form-data',
        "X-CSRFToken": cookies.get("csrftoken") 
      }}) 
      .then((response) => {
        console.log(response)
        const object={}
        const lista = []
        response.data.results.forEach(element => {
          //setMsg(msg => [...msg, element]);
          lista.push(element)
        });
        setMsg(lista);
        getPersonsChats()
      })
      .finally(() => {
        //setIsLoading(false);
      });
  }, [])

  function addMessage(message){
    setMsg(msg =>[...msg, message] )
  }

  function getPersonsChats(){
    const fetch = axios.get(`${API_URL}/getpersonschats/`,  {credentials: "same-origin",
    withCredentials:true, headers:{
      //'Content-Type': 'multipart/form-data',
      "X-CSRFToken": cookies.get("csrftoken")
    }}).then((response) => { 
      console.log(response)
      console.log(response.data)
      setChats(chat => [...chat, response])
    } ) 
  }

  if(msg.length==0){
    return(
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

          </tbody>
          
        </table>
        <h3 class="h3-responsive font-weight-bold text-center my-5">
          Aún no has recibido mensajes en la aplicación.
        </h3>
      </div>
    </section>)
  }

  //cambiar el mensaje dependiendo si es del usuario o no

  return (
    <Container>
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
          {msg.map((e) => (
            <tr>
              <td>{e.date}</td>
              <td>{e.sender_name}</td>
              <td>
                <p class="font-weight-bold mb-0">{e.body}</p>
                <hr class="mt-0 mb-2" />
                <p class="ml-3 mb-1"></p>
              </td>
            </tr>
      ))}
          </tbody>
        </table>
          <Chat messages={msg} chat={a.chatid} addMessage={addMessage} ref={chatRef}/>        
        
      </div>
    </section>
    </Container>
  );
}
