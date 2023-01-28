import AuthContext from "contexts/UserContext";
import { useContext, useEffect, useState } from "react";
import { Container, Form, Table } from "react-bootstrap";
import axios from "axios";
import { API_URL, APP_URL } from "constants";
import AdminIndex from "pages/AdminIndex";

const Admin = () => {
    const { user, setUser } = useContext(AuthContext);
    const [admin, setAdmin] = useState([]);
    //const fetchData = axios
    //    .get(`${APP_URL}/admin/`, {withCredentials: true})
    //    .then((response) => {
    //        const res = response.data;
    //        console.log('response from admin: ',res);
    //    }); //Should be ${APP_URL}/admin/, {withCredentials: true} but it needs sessionid and csrftoken to work
    //    console.log('admin fetch data: ',fetchData);
    
    console.log('user data: ', user);

    if(!user) {
        return
    }
    return (
        AdminIndex()
    )
}
export default Admin;