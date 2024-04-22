import axios from "axios";
import { API_URL } from "constants";
import { EventContext } from "contexts/EventContext";
import { UserContext } from "contexts/UserContext";
import { useContext, useEffect, useState } from "react";
import Form from "react-bootstrap/Form";
import Select from "react-select";
import { sleeper, unaccent } from "utils";

import Cookies from "universal-cookie";
//instantiating Cookies class by creating cookies object
const cookies = new Cookies();

export default function AdminSidebar({ filters, setFilters }) {
  const { event } = useContext(EventContext);
  const { user } = useContext(UserContext);
  const [participantsOptions, setParticipantsOptions] = useState([]);
  const [sportOptions, setSportOptions] = useState([]);
  const [locationOptions, setLocationOptions] = useState([]);

  const playedOptions = [
    { value: 1, label: "Solo jugados" },
    { value: 0, label: "Solo no jugados" },
  ]
  const closedOptions = [
    { value: 1, label: "Solo cerrados" },
    { value: 0, label: "Solo abiertos" },
  ]

  const updateFilters = (name, value) => {
    let newFilters = { ...filters };
    if (value === null || (Array.isArray(value) && value.length === 0)) {
      delete newFilters[name];
    } else {
      newFilters[name] = value;
    }
    setFilters(newFilters);
  };

  const handleSelect = (options, action) => {
    console.log(options, action);
    if (Array.isArray(options)) {
      const result = [];
      options.forEach((option) => {
        result.push(option.value);
      });
      updateFilters(action.name, result);
    } else {
      updateFilters(action.name, options != null ? options.value : null);
    }
  };

  const handleCheckbox = (e) => {
    updateFilters(e.target.name, e.target.checked ? 1 : null);
  };

  useEffect(() => {
    if (!event) return;
    const fetch = axios
      .get(`${API_URL}/users/`,{ headers:{
        "X-CSRFToken": cookies.get("csrftoken")
      },
      credentials: "same-origin",
      withCredentials:true,
        
      })
      .then(sleeper(500))
      .then((response) => {
        setParticipantsOptions(response.data.participants ?? []);
        setSportOptions(response.data.sport ?? []);
        setLocationOptions(response.data.location ?? []);
        console.log(response.data.participants);
      })
      .finally(() => {
        //setIsLoading(false);
      });
  }, [event]);

  const handleText = (e) => {
    updateFilters(e.target.name, unaccent(e.target.value));
    };


  return (
    <div>
      <Form.Check // no implementado
        name="my_matches"
        label="Mostrar solo del evento actual"
        onChange={handleCheckbox}
        checked={filters.my_matches} 
      />

      <Form.Label htmlFor="username">Usuario</Form.Label>
      <Form.Control
        placeholder="Sin filtrar"
        name="username"
        onBlur={handleText}
        onKeyPress={(e) => {
          if (e.key === "Enter") handleText(e);
        }}
      />

      <Form.Label htmlFor="sport">Deporte</Form.Label>
      <Select
        isClearable
        placeholder="Sin filtrar"
        name="sport"
        inputId="sport"
        options={sportOptions}
        className="basic-multi-select"
        classNamePrefix="select"
        onChange={handleSelect}
        value={sportOptions.find((o) => o.value === filters.sport) ?? null}
      />

      <Form.Label htmlFor="location">Lugar</Form.Label>
      <Select
        isClearable
        placeholder="Sin filtrar"
        name="location"
        inputId="location"
        options={locationOptions}
        className="basic-multi-select"
        classNamePrefix="select"
        onChange={handleSelect}
        value={
          locationOptions.find((o) => o.value === filters.location) ?? null
        }
      />

      <Form.Label htmlFor="played">Partidos jugados</Form.Label>
      <Select
        isClearable
        placeholder="Sin filtrar"
        name="played"
        inputId="played"
        options={playedOptions}
        className="basic-multi-select"
        classNamePrefix="select"
        onChange={handleSelect}
        value={
          playedOptions.find((o) => o.value === filters.played) ?? null
        }
      />

      <Form.Label htmlFor="closed">Partidos cerrados</Form.Label>
      <Select
        isClearable
        placeholder="Sin filtrar"
        name="closed"
        inputId="closed"
        options={closedOptions}
        className="basic-multi-select"
        classNamePrefix="select"
        onChange={handleSelect}
        value={
          closedOptions.find((o) => o.value === filters.closed) ?? null
        }
      />
    </div>
  );
}