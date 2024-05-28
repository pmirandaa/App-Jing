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
import Message from "./MessagesContainer";
import Input from "./Input";
import styles from "./Messages.module.scss";
import MessagesContainer from "./MessagesContainer";

export default function Chat({messages, chat, addMessage}){


    return(
        <div className={styles.home}>
          <div className={styles.container}>
                <div className={styles.chat}>
                    <div className={styles.chatInfo}>
                        <span>Chat Info</span>
                    </div>
                    <MessagesContainer messages={messages} />
                    <Input chat={chat} addMessage={addMessage}/>  
                </div>
             </div>       
        </div>
    )
}