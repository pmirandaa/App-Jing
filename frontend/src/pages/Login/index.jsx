import axios from "axios";
import { API_URL } from "constants";
import { sleeper } from "utils";
import { useState, useEffect, useContext, useRef } from "react";
import { UserContext } from "contexts/UserContext";

import Cookies from "universal-cookie";

//instantiating Cookies class by creating cookies object
const cookies = new Cookies();

export default function Login() {
  const [session, setSession] = useState({username:"",password:"", isAuthenticated:false,error:""})
  const [profile, setProfile] = useState({id:0,name:"",last_name:"",email:"",university:0, rut:"" ,error:"", roles:""})

  const {user, setUser} = useContext(UserContext)
  const profileRef = useRef({id:0,name:"",last_name:"",email:"",university:0, rut:"" ,error:"", roles:[]})

  async function asyncLoginpost(user, setUser) {
    const fetch = axios
      .post(`${API_URL}/login/`,JSON.stringify( {username: session.username, password:session.password}),{
        headers:{
          "X-CSRFToken": cookies.get("csrftoken")
        },
        credentials: "same-origin",
        withCredentials:true,
      })
      .then(sleeper(500))
      .then((response) => response.data)
      .then( (data)=> 
      {
        console.log("respuesta de login",data);
        setProfile({...profile,id:data.user.id, name: data.user.name ,last_name:data.user.last_name,email:data.user.email,university:data.user.university, rut:data.user.rut})
        profileRef.current={...profile,id:data.user.id, name: data.user.name ,last_name:data.user.last_name,email:data.user.email,university:data.user.university, rut:data.user.rut, roles:data.PER}
        setSession({...session,isAuthenticated: true, username: "", password: "", error: ""});

        saveUser(user,setUser)
      })
  }

  function saveUser(user, setUser){
    setUser({id:profileRef.current.id, name: profileRef.current.name ,last_name:profileRef.current.last_name,email:profileRef.current.email,university:profileRef.current.university, rut:profileRef.current.rut, roles:profileRef.current.roles, isAuthenticated:true})

  }

  useEffect(() =>{
    getSession()
  },[]) 

    // Get Session Method https://github.com/BekBrace/django-react-vite-auth/blob/main/frontend/src/App.jsx
    function getSession() {
      //// Make a GET request to the "/api/session/" URL with "same-origin" credentials
      axios.get(`${API_URL}/session/`,{credentials: "same-origin",withCredentials:true,})
      //.then((res) => res.json()) //// Parse the response as JSON
      .then((data) => {
        console.log("get sessiondata",data); // Log the response data to the console
        console.log("get session data.data",data.data.isAuthenticated)
        //// If the response indicates the user is authenticated
        if (data.data.isAuthenticated) {
          setSession({...session,isAuthenticated: true}); // Update the component's state
          profileRef.current={...profile,id:data.data.user.id, name: data.data.user.name ,last_name:data.data.user.last_name,email:data.data.user.email,university:data.data.user.university, rut:data.data.user.rut, roles:data.data.PER}
          saveUser(user,setUser)
        } else {  // If the response indicates the user is not authenticated
          setSession({...session,isAuthenticated: false}); // Update the component's state
        }
      })}

  function isResponseOk(response) {
    if (response.status >= 200 && response.status <= 299) {
      return response.json();
    } else {
      throw Error(response.statusText);
    }
  }

   //Logout Method
   function logout(){
    axios.get(`${API_URL}/logout/`, {
      credentials: "same-origin",
      withCredentials:true,
    })
    //.then(this.isResponseOk)
    .then((response) => {
      console.log(response);
      console.log(response.data);
      setSession({...session,isAuthenticated: false});
      setUser({id:0,name:"",last_name:"",email:"",university:0, rut:"12" ,error:""})
      setProfile({id:0,name:"",last_name:"",email:"",university:0, rut:"" ,error:"", roles:""})
    })
    .catch((err) => {
      console.log(err);
    });
  };

  function handlePasswordChange(event) {
    setSession({...session,password: event.target.value});
  }

  function handleUserNameChange(event) {
    setSession({...session,username: event.target.value});
  }
  if(!session.isAuthenticated){
  return (
    <UserContext.Provider value={[user, setUser]}>
      {console.log("profile dentro del provider",profile)}
      {console.log("usuario dentro del provider",user)}

      <div>
      <label>Enter your Username:
        <input type="text" id="username" name="username" value={session.username} onChange={handleUserNameChange} />
      </label>
      </div>
      <div>
      <label>Password:
        <input type="password" id="password" name="password" value={session.password} onChange={handlePasswordChange} />
      </label>
      </div>
      <div>
      
      <button  id="submit-btn" type="submit" onClick={()=>{asyncLoginpost(user,setUser)}}> Login</button> 
      
        </div>
      </UserContext.Provider>
  )}

  return(
    <div>
      <h1>Bienvenido {session.username}</h1>
      <button  id="submit-btn" type="submit" onClick={logout}> Logout</button>
      
      <p>{user.name}</p>
      <p>{user.email}</p>
      <p>{user.id}</p>
      <p>{user.last_name}</p>
      <p>{user.rut}</p>
      <p>{user.university}</p>
    </div>
  
  )
}
