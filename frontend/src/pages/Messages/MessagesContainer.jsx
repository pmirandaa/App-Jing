import styles from "./Messages.module.scss";
import Message from "./Message";
import { useEffect, useRef } from "react";

export default function MessagesContainer({messages}){
    const chatRef= useRef(null)


    useEffect(() => {
        chatRef.current?.lastElementChild?.scrollIntoView()
    }, [messages])

    return(

        <div className={styles.messagesContainer} ref={chatRef}>
        {messages.map((message)=>(
            <Message message={message}/>
        ))}
        </div>
      
      
    )
}