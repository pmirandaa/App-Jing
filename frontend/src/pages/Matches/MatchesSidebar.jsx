import axios from "axios";
import { API_URL } from "constants";
import { EventContext } from "contexts/EventContext";
import { useContext, useEffect, useState } from "react";
import Form from "react-bootstrap/Form";
import Select from "react-select";
import { sleeper } from "utils";

export default function MatchesSidebar({ filters, setFilters }) {
  const { event } = useContext(EventContext);
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
    console.log("options display");
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
      .get(`${API_URL}/matches/filters/?event=${event.id}`)
      .then(sleeper(500))
      .then((response) => {
        setParticipantsOptions(response.data.participants ?? []);
        setSportOptions(response.data.sport ?? []);
        setLocationOptions(response.data.location ?? []);
        console.log(response.data.participants);
        console.log("participants display");
      })
      .finally(() => {
        //setIsLoading(false);
      });
  }, [event]);

  return (
    <div>
      <Form.Check
        name="my_matches"
        label="Mostrar solo mis partidos"
        onChange={handleCheckbox}
        checked={filters.my_matches}
      />

      <Form.Label htmlFor="participants">Participantes</Form.Label>
      <Select
        isMulti
        placeholder="Sin filtrar"
        name="participants"
        inputId="participants"
        options={participantsOptions}
        className="basic-multi-select"
        classNamePrefix="select"
        onChange={handleSelect}
        value={participantsOptions.filter((o) => {
          return Array.isArray(filters.participants)
            ? filters.participants.includes(o.value)
            : filters.participants === o.value;
        })}
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
