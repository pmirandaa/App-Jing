import { UserContext } from "contexts/UserContext";
import { useContext, useEffect, useState } from "react";
import { Container, Form, Table } from "react-bootstrap";
import axios from "axios";
import { API_URL, APP_URL } from "constants";
import AdminIndex from "pages/AdminIndex";

export default function Admin() {
    const { person, setPerson } = useContext(UserContext);
    const [admin, setAdmin] = useState([]);
    const fetchData = async() => {axios
        .get(`${APP_URL}/admin/`);
        console.log(fetchData);
    }
    console.log(person);

    if(!person) {
        return
    }
    return (
        AdminIndex()
    )
}