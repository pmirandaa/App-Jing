import axios from "axios";
import { API_URL } from "constants";
import { sleeper } from "utils";
import { Container, Form, Table } from "react-bootstrap";
import { useState, useEffect, componentDidMount } from "react";

import Cookies from "universal-cookie";

//instantiating Cookies class by creating cookies object
const cookies = new Cookies();

export default function Login() {
  const [session, setSession] = useState({username:"",password:"", isAuthenticated:false,error:""})

    function Loginpost() {
        const fetch = axios
        .post(`${API_URL}/login/`,{
          headers:{
            "X-CSRFToken": cookies.get("csrftoken")
          },
          body: JSON.stringify( {username: session.username, password:session.password})
        })
        .then(sleeper(500))
        .then((response) => {
          console.log(response.data);
          setSession({isAuthenticated: true, username: "", password: "", error: ""});
          
        })
        .finally(() => {
          //setIsLoading(false);
        });
    }

    // useEffect(() =>{
    //   getSession()
    // }) 

    // Get Session Method https://github.com/BekBrace/django-react-vite-auth/blob/main/frontend/src/App.jsx
    function getSession() {
      //// Make a GET request to the "/api/session/" URL with "same-origin" credentials
      axios.get(`${API_URL}/session/`)
      .then((res) => res.json()) //// Parse the response as JSON
      .then((data) => {
        console.log(data); // Log the response data to the console
        //// If the response indicates the user is authenticated
        if (data.isAuthenticated) {
          this.setSession({...session,isAuthenticated: true}); // Update the component's state
        } else {  // If the response indicates the user is not authenticated
          this.setSession({...session,isAuthenticated: false}); // Update the component's state
        }
      })}

    //Who Am I method
  function whoami(){
    axios.get("/api/whoami/", {
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "same-origin",
    })
    .then((res) => res.json())
    .then((data) => {
      console.log("You are logged in as: " + data.username);
    })
    .catch((err) => {
      console.log(err);
    });
  }

  function isResponseOk(response) {
    if (response.status >= 200 && response.status <= 299) {
      return response.json();
    } else {
      throw Error(response.statusText);
    }
  }

  return (
    <form id="loginform">
      <div>
      <label>Enter your Username:
        <input type="text" id="username" name="username" />
      </label>
      </div>
      <div>
      <label>Password:
        <input type="password" id="password" name="password" />
      </label>
      </div>
      <button  id="submit-btn" type="submit" onClick={Loginpost}> Login</button>
    </form>
    // <Container style={{ padding: "16px", position: "relative" }}>
    
    //     <Form name="hinchaForm" method="post">
    //     <InputWrapper>
    //     name="username"
        
    //     </InputWrapper>
    //     {/* <input type="text" name="Username" id="Username" maxlength="80" required> </input>
    //     <input type="hidden" name="Password" id="Password" maxlength="80" required> </input> */}

    //     </Form>

    // </Container>
  )
}
