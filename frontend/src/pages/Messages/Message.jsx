import { useContext, useState, useEffect } from "react";
import { EventContext } from "contexts/EventContext";
import { UserContext } from "contexts/UserContext";
import styles from "./Messages.module.scss";
import "./Messages.module.scss";

export default function Message({message}){
    const {user} = useContext(UserContext)

    return(
        <div className={user.name == message.sender_name ? (`${styles.message} ${styles.owner}`) : (styles.message)}>
            <div className={styles.messageInfo}>
            </div>
            <div className={styles.messageContent}>
            <span>{message.sender_name}</span>
                <p>{message.body}</p>
            </div>
        </div>
    )
}