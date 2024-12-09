import { useContext, useState, useEffect } from "react";
import axios from "axios";
import { API_URL } from "constants";
import Cookies from "universal-cookie";
import Message from "./Message";
import styles from "./Messages.module.scss";


const cookies = new Cookies();
export default function Input({chat, addMessage}){

  const [input, setInput]= useState("")
    
  function send(){
      const fd = new FormData();
      fd.append('message', input);
      fd.append('chat', chat);
      const fetch = axios.post(`${API_URL}/createnewmessage/`, fd, {
        credentials: "same-origin",
        withCredentials:true,
        headers:{
          'Content-Type': 'multipart/form-data',
          "X-CSRFToken": cookies.get("csrftoken")
        }
      })
      .then( (response) => {
        const message= response.data.message
        console.log(response)
        console.log(message)
        addMessage(message)
        console.log("message")
        console.log("listo")
      })
  }

  function handleInputChange(e){
    setInput(e.target.value)
    console.log(input)
  }

    return(
        <div className={styles.input}>
        <input type="text" placeholder="mensaje" onChange={handleInputChange} />
        <div className={styles.send}>
          <button onClick={send}>Send</button>
        </div>
      </div>
    )
}